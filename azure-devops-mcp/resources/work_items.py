from __future__ import annotations

import json

from server import api, mcp
from exceptions import AzureDevOpsError, NotFoundError


@mcp.resource("workitem://{item_id}")
async def work_item_resource(item_id: str) -> str:
    """
    Load a work item's full details into the AI context as a resource.

    URI format: workitem://42
    """
    try:
        item = await api.get_work_item(int(item_id))
        return json.dumps({
            "id": item.id,
            "type": item.fields.work_item_type,
            "title": item.fields.title,
            "state": item.fields.state,
            "story_points": item.fields.story_points,
            "iteration": item.fields.iteration_path,
            "description": item.fields.description,
            "acceptance_criteria": item.fields.acceptance_criteria,
            "parent_id": item.fields.parent_id,
            "child_ids": item.child_ids,
        }, indent=2, ensure_ascii=False)
    except NotFoundError:
        return f"Work item #{item_id} not found."
    except (ValueError, AzureDevOpsError) as e:
        return f"Error loading work item #{item_id}: {e}"


@mcp.resource("sprint://current")
async def current_sprint_resource() -> str:
    """
    Load the current sprint metadata into the AI context.

    URI format: sprint://current
    Returns the sprint name, start date, finish date, and active work item IDs.
    """
    try:
        iteration = await api.get_current_iteration()
        ids = await api.query_work_items(
            f"SELECT [System.Id] FROM WorkItems "
            f"WHERE [System.IterationPath] = '{iteration.path}' "
            f"AND [System.State] <> 'Done' AND [System.State] <> 'Closed'"
        )
        return json.dumps({
            "name": iteration.name,
            "path": iteration.path,
            "start_date": iteration.attributes.start_date,
            "finish_date": iteration.attributes.finish_date,
            "time_frame": iteration.attributes.time_frame,
            "active_work_item_ids": ids,
        }, indent=2, ensure_ascii=False)
    except AzureDevOpsError as e:
        return f"Error loading current sprint: {e}"
