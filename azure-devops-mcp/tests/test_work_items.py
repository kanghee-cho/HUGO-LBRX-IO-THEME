import pytest
from unittest.mock import patch, MagicMock
from exceptions import AzureDevOpsError, NotFoundError
from tools.work_items import (
    get_work_item, list_work_items, create_work_item, update_work_item,
    add_work_item_comment, move_work_item_to_sprint,
)
from client.api import AzureDevOpsClient, _MARKDOWN_FIELDS
from client.models import WorkItemComment


@pytest.mark.asyncio
async def test_get_work_item_returns_fields(mock_api, sample_work_item):
    mock_api.get_work_item.return_value = sample_work_item
    result = await get_work_item(42)
    assert '"id": 42' in result
    assert "Setup CI pipeline" in result
    assert "Active" in result


@pytest.mark.asyncio
async def test_get_work_item_not_found(mock_api):
    mock_api.get_work_item.side_effect = NotFoundError("not found")
    result = await get_work_item(999)
    assert "#999" in result
    assert "not found" in result.lower()


@pytest.mark.asyncio
async def test_create_work_item_invalid_type(mock_api):
    result = await create_work_item("InvalidType", "Some title")
    assert "Invalid work_item_type" in result
    mock_api.create_work_item.assert_not_called()


@pytest.mark.asyncio
async def test_create_work_item_success(mock_api, sample_work_item):
    mock_api.create_work_item.return_value = sample_work_item
    result = await create_work_item("User Story", "Setup CI pipeline", story_points=5)
    assert '"created": true' in result.lower()
    assert '"id": 42' in result


@pytest.mark.asyncio
async def test_update_work_item_no_fields(mock_api):
    result = await update_work_item(42)
    assert "No fields provided" in result
    mock_api.update_work_item.assert_not_called()


@pytest.mark.asyncio
async def test_update_work_item_state(mock_api, sample_work_item):
    mock_api.update_work_item.return_value = sample_work_item
    result = await update_work_item(42, state="Resolved")
    assert '"updated": true' in result.lower()


@pytest.mark.asyncio
async def test_add_comment_success(mock_api):
    mock_api.add_work_item_comment.return_value = WorkItemComment(id=1, text="done")
    result = await add_work_item_comment(42, "Implementation complete.")
    assert "Comment added" in result
    assert "#42" in result


@pytest.mark.asyncio
async def test_move_to_sprint(mock_api, sample_work_item):
    mock_api.update_work_item.return_value = sample_work_item
    result = await move_work_item_to_sprint(42, "MyProject\\Sprint 2")
    assert "#42" in result


# ------------------------------------------------------------------
# _field_ops unit tests — Markdown format hint
# ------------------------------------------------------------------

def test_field_ops_plain_field_no_format_hint():
    ops = AzureDevOpsClient._field_ops("System.Title", "Hello")
    assert len(ops) == 1
    assert ops[0] == {"op": "add", "path": "/fields/System.Title", "value": "Hello"}


def test_field_ops_description_adds_markdown_hint():
    ops = AzureDevOpsClient._field_ops("System.Description", "## Title\n\n- item  \n- item2")
    assert len(ops) == 2
    assert ops[0]["path"] == "/fields/System.Description"
    assert ops[1] == {
        "op": "add",
        "path": "/multilineFieldsFormat/System.Description",
        "value": "Markdown",
    }


def test_field_ops_acceptance_criteria_adds_markdown_hint():
    ops = AzureDevOpsClient._field_ops(
        "Microsoft.VSTS.Common.AcceptanceCriteria", "- [ ] Done", op="replace"
    )
    assert len(ops) == 2
    assert ops[0]["op"] == "replace"
    assert ops[1]["op"] == "add"
    assert ops[1]["path"] == "/multilineFieldsFormat/Microsoft.VSTS.Common.AcceptanceCriteria"


def test_field_ops_repro_steps_adds_markdown_hint():
    ops = AzureDevOpsClient._field_ops("Microsoft.VSTS.TCM.ReproSteps", "1. Step one\n2. Step two")
    assert len(ops) == 2
    assert ops[0]["path"] == "/fields/Microsoft.VSTS.TCM.ReproSteps"
    assert ops[1] == {
        "op": "add",
        "path": "/multilineFieldsFormat/Microsoft.VSTS.TCM.ReproSteps",
        "value": "Markdown",
    }


def test_field_ops_non_string_value_no_markdown_hint():
    ops = AzureDevOpsClient._field_ops("System.Description", None)
    assert len(ops) == 1


def test_markdown_fields_constant():
    assert "System.Description" in _MARKDOWN_FIELDS
    assert "Microsoft.VSTS.Common.AcceptanceCriteria" in _MARKDOWN_FIELDS
    assert "Microsoft.VSTS.TCM.ReproSteps" in _MARKDOWN_FIELDS
    assert "System.Title" not in _MARKDOWN_FIELDS


# ------------------------------------------------------------------
# _normalize_md — literal \n escape handling
# ------------------------------------------------------------------

def test_normalize_md_converts_literal_backslash_n():
    result = AzureDevOpsClient._normalize_md("Line one\\nLine two")
    assert result == "Line one\nLine two"


def test_normalize_md_converts_literal_backslash_t():
    result = AzureDevOpsClient._normalize_md("Col1\\tCol2")
    assert result == "Col1\tCol2"


def test_normalize_md_real_newline_unchanged():
    result = AzureDevOpsClient._normalize_md("Line one\nLine two")
    assert result == "Line one\nLine two"


def test_normalize_md_empty_string():
    assert AzureDevOpsClient._normalize_md("") == ""


def test_field_ops_normalizes_literal_newlines_in_markdown_field():
    ops = AzureDevOpsClient._field_ops("System.Description", "First\\n\\nSecond")
    assert ops[0]["value"] == "First\n\nSecond"


def test_field_ops_does_not_normalize_plain_fields():
    # Non-markdown fields must pass the value through unchanged
    ops = AzureDevOpsClient._field_ops("System.Title", "Hello\\nWorld")
    assert ops[0]["value"] == "Hello\\nWorld"
