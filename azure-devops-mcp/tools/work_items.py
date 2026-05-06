from __future__ import annotations

import json
import logging

from server import api, mcp
from exceptions import AzureDevOpsError, NotFoundError

logger = logging.getLogger(__name__)

# Valid work item types in this project
VALID_TYPES = {"Epic", "Feature", "User Story", "Task", "Bug"}

# Fields updated when changing state
STATE_FIELD = "System.State"


def _format_work_item(item_data: dict) -> str:
    """Serialize a WorkItem to a readable JSON string."""
    return json.dumps(item_data, indent=2, ensure_ascii=False)


@mcp.tool()
async def get_work_item(item_id: int) -> str:
    """
    Get full details of a single work item by ID.

    Use this before starting work on any task to read title, state, acceptance criteria,
    story points, sprint assignment, and parent/child relationships.

    Args:
        item_id: Integer ID of the work item (e.g., 42).
    """
    try:
        item = await api.get_work_item(item_id)
        return json.dumps({
            "id": item.id,
            "type": item.fields.work_item_type,
            "title": item.fields.title,
            "state": item.fields.state,
            "story_points": item.fields.story_points,
            "iteration": item.fields.iteration_path,
            "area": item.fields.area_path,
            "assigned_to": item.fields.assigned_to_name,
            "tags": item.fields.tags,
            "description": item.fields.description,
            "acceptance_criteria": item.fields.acceptance_criteria,
            "parent_id": item.fields.parent_id,
            "child_ids": item.child_ids,
        }, indent=2, ensure_ascii=False)
    except NotFoundError:
        return f"Work item #{item_id} not found."
    except AzureDevOpsError as e:
        return f"Error fetching work item #{item_id}: {e}"


@mcp.tool()
async def list_work_items(
    work_item_type: str | None = None,
    state: str | None = None,
    iteration_path: str | None = None,
    assigned_to: str | None = None,
    top: int = 30,
) -> str:
    """
    Query work items using WIQL with optional filters.

    Use this at the start of a session to check the sprint backlog, find active tasks,
    or identify all Epics/Features in progress.

    Args:
        work_item_type: Filter by type — 'Epic', 'Feature', 'User Story', 'Task', 'Bug'. Omit for all.
        state: Filter by state — 'New', 'Active', 'Resolved', 'Done', 'Closed'. Omit for all.
        iteration_path: Filter by sprint path. Example: 'MyProject\\Sprint 1'. Omit for all sprints.
        assigned_to: Filter by assignee display name or email. Use '@Me' for current user. Omit for all.
        top: Maximum number of results (default 30, max 200).
    """
    conditions = ["[System.TeamProject] = @project"]
    if work_item_type:
        conditions.append(f"[System.WorkItemType] = '{work_item_type}'")
    if state:
        conditions.append(f"[System.State] = '{state}'")
    if iteration_path:
        conditions.append(f"[System.IterationPath] = '{iteration_path}'")
    if assigned_to:
        conditions.append(f"[System.AssignedTo] = '{assigned_to}'")

    where = " AND ".join(conditions)
    wiql = f"SELECT [System.Id] FROM WorkItems WHERE {where} ORDER BY [System.ChangedDate] DESC"

    try:
        ids = await api.query_work_items(wiql)
        if not ids:
            return "No work items found matching the given filters."

        ids = ids[:top]
        items = await api.get_work_items_batch(ids)

        rows = []
        for item in items:
            rows.append({
                "id": item.id,
                "type": item.fields.work_item_type,
                "title": item.fields.title,
                "state": item.fields.state,
                "story_points": item.fields.story_points,
                "assigned_to": item.fields.assigned_to_name,
                "iteration": item.fields.iteration_path,
            })
        return json.dumps(rows, indent=2, ensure_ascii=False)
    except AzureDevOpsError as e:
        return f"Error querying work items: {e}"


@mcp.tool()
async def get_work_item_children(parent_id: int) -> str:
    """
    Get the direct children of a work item.

    Use this to list all Features under an Epic, all Stories under a Feature,
    or all Tasks/Bugs under a User Story.

    Args:
        parent_id: ID of the parent work item.
    """
    try:
        parent = await api.get_work_item(parent_id)
        child_ids = parent.child_ids
        if not child_ids:
            return f"Work item #{parent_id} ('{parent.fields.title}') has no children."

        children = await api.get_work_items_batch(child_ids)
        rows = [{"id": c.id, "type": c.fields.work_item_type, "title": c.fields.title,
                 "state": c.fields.state, "story_points": c.fields.story_points} for c in children]
        return json.dumps({"parent_id": parent_id, "parent_title": parent.fields.title,
                           "children": rows}, indent=2, ensure_ascii=False)
    except NotFoundError:
        return f"Work item #{parent_id} not found."
    except AzureDevOpsError as e:
        return f"Error fetching children of #{parent_id}: {e}"


@mcp.tool()
async def create_work_item(
    work_item_type: str,
    title: str,
    description: str = "",
    acceptance_criteria: str = "",
    story_points: float | None = None,
    iteration_path: str = "",
    area_path: str = "",
    parent_id: int | None = None,
    tags: str = "",
) -> str:
    """
    Create a new work item (Epic, Feature, User Story, Task, or Bug).

    Use this to add new items to the backlog, break down Epics into Features,
    or create Tasks under a User Story. Link to a parent by providing parent_id.

    Args:
        work_item_type: One of 'Epic', 'Feature', 'User Story', 'Task', 'Bug'.
        title: Short, descriptive title of the work item.
        description: Detailed description in Markdown format.
        acceptance_criteria: Definition of done in Markdown format (for User Stories).
        story_points: Effort estimate as a number (e.g., 3, 5, 8).
        iteration_path: Sprint to assign to. Example: 'MyProject\\Sprint 1'.
        area_path: Area classification. Example: 'MyProject\\Backend'.
        parent_id: ID of the parent work item to link under.
        tags: Semicolon-separated tags. Example: 'api; backend'.
    """
    if work_item_type not in VALID_TYPES:
        return f"Invalid work_item_type '{work_item_type}'. Must be one of: {', '.join(sorted(VALID_TYPES))}"

    try:
        item = await api.create_work_item(
            work_item_type=work_item_type,
            title=title,
            description=description,
            acceptance_criteria=acceptance_criteria,
            story_points=story_points,
            iteration_path=iteration_path,
            area_path=area_path,
            parent_id=parent_id,
            tags=tags,
        )
        return json.dumps({
            "created": True,
            "id": item.id,
            "type": item.fields.work_item_type,
            "title": item.fields.title,
            "state": item.fields.state,
        }, indent=2, ensure_ascii=False)
    except AzureDevOpsError as e:
        return f"Error creating work item: {e}"


@mcp.tool()
async def update_work_item(
    item_id: int,
    title: str | None = None,
    state: str | None = None,
    story_points: float | None = None,
    iteration_path: str | None = None,
    area_path: str | None = None,
    description: str | None = None,
    acceptance_criteria: str | None = None,
    tags: str | None = None,
) -> str:
    """
    Update fields on an existing work item.

    Use this to change the state (e.g., New → Active → Resolved),
    assign story points, move to a sprint, or update the title/description.
    Only provide the fields you want to change — omitted fields are unchanged.

    Args:
        item_id: ID of the work item to update.
        title: New title.
        state: New state — 'New', 'Active', 'Resolved', 'Done', 'Closed'.
        story_points: New story point estimate.
        iteration_path: New sprint/iteration path.
        area_path: New area path.
        description: New description in Markdown format. Use \\n\\n for paragraph breaks, two trailing spaces + \\n for line/item breaks.
        acceptance_criteria: New acceptance criteria in Markdown format.
        tags: New semicolon-separated tags (replaces existing tags).
    """
    field_map = {
        "System.Title": title,
        "System.State": state,
        "Microsoft.VSTS.Scheduling.StoryPoints": story_points,
        "System.IterationPath": iteration_path,
        "System.AreaPath": area_path,
        "System.Description": description,
        "Microsoft.VSTS.Common.AcceptanceCriteria": acceptance_criteria,
        "System.Tags": tags,
    }
    fields = {k: v for k, v in field_map.items() if v is not None}
    if not fields:
        return "No fields provided to update. Specify at least one field."

    try:
        item = await api.update_work_item(item_id, fields)
        return json.dumps({
            "updated": True,
            "id": item.id,
            "title": item.fields.title,
            "state": item.fields.state,
        }, indent=2, ensure_ascii=False)
    except NotFoundError:
        return f"Work item #{item_id} not found."
    except AzureDevOpsError as e:
        return f"Error updating work item #{item_id}: {e}"


@mcp.tool()
async def add_work_item_comment(item_id: int, text: str) -> str:
    """
    Add a comment to a work item.

    Use this after completing a significant step to document what was done,
    record a blocker, or leave a note for reviewers.

    Args:
        item_id: ID of the work item to comment on.
        text: Comment text (plain text or HTML).
    """
    try:
        comment = await api.add_work_item_comment(item_id, text)
        return f"Comment added to work item #{item_id} (comment ID: {comment.id})."
    except NotFoundError:
        return f"Work item #{item_id} not found."
    except AzureDevOpsError as e:
        return f"Error adding comment to #{item_id}: {e}"


@mcp.tool()
async def move_work_item_to_sprint(item_id: int, iteration_path: str) -> str:
    """
    Assign a work item to a specific sprint (iteration).

    Use this during sprint planning to move backlog items into the current or
    an upcoming sprint.

    Args:
        item_id: ID of the work item to move.
        iteration_path: Full iteration path. Example: 'MyProject\\Sprint 2'.
    """
    try:
        item = await api.update_work_item(item_id, {"System.IterationPath": iteration_path})
        return f"Work item #{item_id} ('{item.fields.title}') moved to '{item.fields.iteration_path}'."
    except NotFoundError:
        return f"Work item #{item_id} not found."
    except AzureDevOpsError as e:
        return f"Error moving work item #{item_id}: {e}"
