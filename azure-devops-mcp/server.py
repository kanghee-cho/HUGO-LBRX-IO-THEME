from mcp.server.fastmcp import FastMCP

from client.api import AzureDevOpsClient
from config import Settings

settings = Settings()

api = AzureDevOpsClient(
    org_url=settings.azure_devops_org_url,
    project=settings.azure_devops_project,
    pat=settings.azure_devops_pat,
    wiki_id=settings.azure_devops_wiki_id,
    timeout=settings.request_timeout,
)

mcp = FastMCP(
    name="azure-devops-mcp",
    instructions=(
        "This server provides access to Azure DevOps for an AI coding assistant. "
        "Use wiki tools to read and write project documentation. "
        "Use work item tools to manage Epics, Features, User Stories, Tasks, and Bugs — "
        "always read a work item before updating it, and set state to 'Active' when starting work. "
        "Use dashboard tools to inspect and configure project dashboards. "
        "Never set a work item state to 'Done' — that is reserved for the human developer."
    ),
)

# Register all primitives by importing their modules
import tools.wiki          # noqa: E402, F401
import tools.work_items    # noqa: E402, F401
import tools.sprints       # noqa: E402, F401
import tools.dashboard     # noqa: E402, F401
import resources.wiki      # noqa: E402, F401
import resources.work_items  # noqa: E402, F401
import prompts.workflows   # noqa: E402, F401
