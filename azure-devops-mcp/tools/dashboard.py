from __future__ import annotations

import json
import logging

from server import api, mcp
from exceptions import AzureDevOpsError, NotFoundError

logger = logging.getLogger(__name__)


@mcp.tool()
async def list_dashboards() -> str:
    """
    List all dashboards available in the Azure DevOps project.

    Use this to discover dashboard IDs before calling get_dashboard or add_query_widget.
    """
    try:
        dashboards = await api.list_dashboards()
        if not dashboards:
            return "No dashboards found in this project."
        rows = [{"id": d.id, "name": d.name, "description": d.description} for d in dashboards]
        return json.dumps(rows, indent=2, ensure_ascii=False)
    except AzureDevOpsError as e:
        return f"Error listing dashboards: {e}"


@mcp.tool()
async def get_dashboard(dashboard_id: str) -> str:
    """
    Get the details of a specific dashboard including its current widgets.

    Use this to inspect what information is already displayed on a dashboard
    before adding new widgets.

    Args:
        dashboard_id: Dashboard ID (obtain from list_dashboards).
    """
    try:
        dashboard = await api.get_dashboard(dashboard_id)
        result = {
            "id": dashboard.id,
            "name": dashboard.name,
            "description": dashboard.description,
            "widgets": [
                {"id": w.id, "name": w.name, "type": w.type_id}
                for w in dashboard.widgets
            ],
        }
        return json.dumps(result, indent=2, ensure_ascii=False)
    except NotFoundError:
        return f"Dashboard '{dashboard_id}' not found."
    except AzureDevOpsError as e:
        return f"Error fetching dashboard '{dashboard_id}': {e}"


@mcp.tool()
async def add_query_widget(
    dashboard_id: str,
    widget_name: str,
    query_id: str,
    row: int = 1,
    column: int = 1,
    row_span: int = 2,
    column_span: int = 3,
) -> str:
    """
    Add a work item query result widget to a dashboard.

    Use this to display the output of a saved Azure DevOps query (e.g., active bugs,
    sprint backlog, unassigned tasks) directly on a dashboard.

    Args:
        dashboard_id: Target dashboard ID (obtain from list_dashboards).
        widget_name: Display name for the widget as it will appear on the dashboard.
        query_id: ID of the saved Azure DevOps query to display.
        row: Grid row position (1-based).
        column: Grid column position (1-based).
        row_span: Height in grid rows (default 2).
        column_span: Width in grid columns (default 3).
    """
    widget_config = {
        "name": widget_name,
        "typeId": "Microsoft.VisualStudioOnline.Dashboards.QueryScalarWidget",
        "position": {"row": row, "column": column},
        "size": {"rowSpan": row_span, "columnSpan": column_span},
        "settings": json.dumps({"queryId": query_id, "queryScope": 1}),
    }

    try:
        widget = await api.add_widget(dashboard_id, widget_config)
        return json.dumps({
            "added": True,
            "widget_id": widget.id,
            "widget_name": widget.name,
            "dashboard_id": dashboard_id,
        }, indent=2, ensure_ascii=False)
    except NotFoundError:
        return f"Dashboard '{dashboard_id}' not found."
    except AzureDevOpsError as e:
        return f"Error adding widget to dashboard '{dashboard_id}': {e}"
