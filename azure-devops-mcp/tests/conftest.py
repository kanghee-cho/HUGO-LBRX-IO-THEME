import pytest
from unittest.mock import AsyncMock, MagicMock

from client.models import WorkItem, WorkItemFields, WikiInfo, WikiPage


@pytest.fixture
def mock_api(monkeypatch):
    """Replace the global api instance in all tool/resource modules with a mock."""
    mock = AsyncMock()
    monkeypatch.setattr("tools.wiki.api", mock)
    monkeypatch.setattr("tools.work_items.api", mock)
    monkeypatch.setattr("tools.dashboard.api", mock)
    monkeypatch.setattr("resources.wiki.api", mock)
    monkeypatch.setattr("resources.work_items.api", mock)
    return mock


@pytest.fixture
def sample_work_item() -> WorkItem:
    return WorkItem(
        id=42,
        rev=1,
        fields=WorkItemFields(**{
            "System.Title": "Setup CI pipeline",
            "System.WorkItemType": "User Story",
            "System.State": "Active",
            "System.IterationPath": "MyProject\\Sprint 1",
            "System.AreaPath": "MyProject",
            "Microsoft.VSTS.Scheduling.StoryPoints": 5.0,
        }),
        relations=[],
        url="https://dev.azure.com/org/project/_apis/wit/workitems/42",
    )


@pytest.fixture
def sample_wiki_page() -> WikiPage:
    return WikiPage(
        path="/Architecture/API",
        content="# API Architecture\n\nContent here.",
        url="https://dev.azure.com/org/project/_apis/wiki/wikis/wiki/pages",
    )


@pytest.fixture
def sample_wiki_info() -> WikiInfo:
    return WikiInfo(
        id="abc123",
        name="MyProject.wiki",
        projectId="f02aa0d2-0000-0000-0000-000000000000",
        type="projectWiki",
        url="https://dev.azure.com/org/project/_apis/wiki/wikis/abc123",
    )
