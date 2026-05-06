from __future__ import annotations

from server import api, mcp
from exceptions import AzureDevOpsError, NotFoundError


@mcp.resource("wiki://{page_path}")
async def wiki_page_resource(page_path: str) -> str:
    """
    Load a wiki page into the AI context as a resource.

    URI format: wiki://Architecture/API/work-items
    The page_path should not start with a leading slash when used as a URI.
    """
    try:
        page = await api.get_wiki_page(f"/{page_path}")
        return page.content
    except NotFoundError:
        return f"Wiki page '/{page_path}' does not exist."
    except AzureDevOpsError as e:
        return f"Error reading wiki page: {e}"
