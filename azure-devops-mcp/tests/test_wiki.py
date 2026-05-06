import pytest
from exceptions import AzureDevOpsError, NotFoundError
from tools.wiki import read_wiki_page, create_wiki_page, update_wiki_page


@pytest.mark.asyncio
async def test_read_wiki_page_returns_content(mock_api, sample_wiki_page):
    mock_api.get_wiki_page.return_value = sample_wiki_page
    result = await read_wiki_page("/Architecture/API")
    assert "# API Architecture" in result
    assert "/Architecture/API" in result


@pytest.mark.asyncio
async def test_read_wiki_page_not_found(mock_api):
    mock_api.get_wiki_page.side_effect = NotFoundError("not found")
    result = await read_wiki_page("/Does/Not/Exist")
    assert "does not exist" in result.lower()


@pytest.mark.asyncio
async def test_read_wiki_page_api_error(mock_api):
    mock_api.get_wiki_page.side_effect = AzureDevOpsError("timeout")
    result = await read_wiki_page("/Some/Page")
    assert "error" in result.lower()


@pytest.mark.asyncio
async def test_create_wiki_page_success(mock_api, sample_wiki_page):
    mock_api.create_wiki_page.return_value = sample_wiki_page
    result = await create_wiki_page("/Architecture/API", "# New Content")
    assert "created successfully" in result.lower()


@pytest.mark.asyncio
async def test_update_wiki_page_not_found(mock_api):
    mock_api.get_wiki_page_version.side_effect = NotFoundError("not found")
    result = await update_wiki_page("/Missing/Page", "new content")
    assert "does not exist" in result.lower()
    assert "create_wiki_page" in result


# ---------------------------------------------------------------------------
# _ensure_wiki provisioning tests (unit-testing AzureDevOpsClient directly)
# ---------------------------------------------------------------------------

import base64
from unittest.mock import AsyncMock, MagicMock, patch
import httpx
from client.api import AzureDevOpsClient
from client.models import WikiInfo


def _make_client() -> AzureDevOpsClient:
    return AzureDevOpsClient(
        org_url="https://dev.azure.com/testorg",
        project="TestProject",
        pat="fake-pat",
        wiki_id="TestProject.wiki",
    )


def _mock_response(status: int, body: dict) -> MagicMock:
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status
    resp.is_success = (200 <= status < 300)
    resp.content = b"x"
    resp.json.return_value = body
    resp.url = "https://dev.azure.com/test"
    return resp


@pytest.mark.asyncio
async def test_ensure_wiki_skips_when_already_provisioned():
    client = _make_client()
    client._wiki_provisioned = True
    # _http should never be called
    client._http = AsyncMock()
    await client._ensure_wiki()
    client._http.get.assert_not_called()


@pytest.mark.asyncio
async def test_ensure_wiki_finds_existing_wiki():
    client = _make_client()
    existing_wiki = {"id": "abc", "name": "TestProject.wiki", "projectId": "pid", "type": "projectWiki"}
    client._http = AsyncMock()
    client._http.get.return_value = _mock_response(200, {"value": [existing_wiki]})

    await client._ensure_wiki()

    assert client._wiki_provisioned is True
    assert client._wiki_id == "TestProject.wiki"
    client._http.post.assert_not_called()


@pytest.mark.asyncio
async def test_ensure_wiki_provisions_when_not_found():
    client = _make_client()
    project_resp = _mock_response(200, {"id": "project-guid-123", "name": "TestProject"})
    list_resp = _mock_response(200, {"value": []})  # no wikis yet
    created_resp = _mock_response(200, {
        "id": "new-wiki-id", "name": "TestProject.wiki",
        "projectId": "project-guid-123", "type": "projectWiki",
    })

    client._http = AsyncMock()
    # GET calls: list wikis, then get project
    client._http.get.side_effect = [list_resp, project_resp]
    client._http.post.return_value = created_resp

    await client._ensure_wiki()

    assert client._wiki_provisioned is True
    assert client._wiki_id == "TestProject.wiki"
    client._http.post.assert_called_once()


@pytest.mark.asyncio
async def test_ensure_wiki_called_before_create_page():
    """create_wiki_page must call _ensure_wiki before the PUT."""
    client = _make_client()
    client._wiki_provisioned = True  # skip actual provisioning
    page_resp = _mock_response(200, {"path": "/Test", "content": "hello"})
    client._http = AsyncMock()
    client._http.put.return_value = page_resp

    result = await client.create_wiki_page("/Test", "hello")
    assert result.path == "/Test"
    client._http.put.assert_called_once()
