from __future__ import annotations

import json
import logging

from server import api, mcp
from exceptions import AzureDevOpsError, NotFoundError

logger = logging.getLogger(__name__)


@mcp.tool()
async def get_current_sprint() -> str:
    """
    Return the current sprint (iteration) for the team.

    Use this at the start of a session to identify the active sprint name and
    iteration path, which can then be passed to list_work_items or move_work_item_to_sprint.
    """
    try:
        iteration = await api.get_current_iteration()
        return json.dumps({
            "id": iteration.id,
            "name": iteration.name,
            "path": iteration.path,
            "start_date": iteration.attributes.start_date,
            "finish_date": iteration.attributes.finish_date,
            "time_frame": iteration.attributes.time_frame,
        }, indent=2, ensure_ascii=False)
    except NotFoundError:
        return "No current sprint found. The team may not have an active iteration configured."
    except AzureDevOpsError as e:
        return f"Error fetching current sprint: {e}"


@mcp.tool()
async def list_sprints() -> str:
    """
    List all sprints (iterations) defined in the project.

    Use this to discover available sprint names and iteration paths before
    calling move_work_item_to_sprint or filtering work items by sprint.
    """
    try:
        iterations = await api.list_iterations()
        if not iterations:
            return "No sprints (iterations) found in this project."
        rows = [
            {
                "id": i.id,
                "name": i.name,
                "path": i.path,
                "start_date": i.attributes.start_date,
                "finish_date": i.attributes.finish_date,
                "time_frame": i.attributes.time_frame,
            }
            for i in iterations
        ]
        return json.dumps(rows, indent=2, ensure_ascii=False)
    except AzureDevOpsError as e:
        return f"Error listing sprints: {e}"
