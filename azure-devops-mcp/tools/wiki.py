from __future__ import annotations

import logging

from server import api, mcp
from exceptions import AzureDevOpsError, NotFoundError

logger = logging.getLogger(__name__)


@mcp.tool()
async def read_wiki_page(page_path: str) -> str:
    """
    Read the full content of a wiki page and load it into context.

    Use this to retrieve existing documentation, architecture notes, sprint records,
    or any other content stored in the Azure DevOps wiki before creating or updating pages.

    Args:
        page_path: Wiki page path starting with /. Example: /Architecture/API or /Sprints/Sprint-1/Planning
    """
    try:
        page = await api.get_wiki_page(page_path)
        return f"# {page.path}\n\n{page.content}"
    except NotFoundError:
        return f"Wiki page '{page_path}' does not exist."
    except AzureDevOpsError as e:
        return f"Error reading wiki page '{page_path}': {e}"


@mcp.tool()
async def list_wiki_pages(path: str = "/", depth: int = 2) -> str:
    """
    List wiki pages under a given path.

    Use this to discover what documentation already exists before creating new pages,
    or to understand the wiki structure before navigating to a specific page.

    Args:
        path: Root path to list from. Defaults to / (all pages).
        depth: How many levels deep to recurse (1 = direct children only, 2 = grandchildren, etc.).
    """
    try:
        pages = await api.list_wiki_pages(path, depth)
        if not pages:
            return f"No pages found under '{path}'."
        lines = [f"Wiki pages under '{path}':"]
        for page in pages:
            lines.append(f"  - {page.path}")
        return "\n".join(lines)
    except NotFoundError:
        return f"Path '{path}' does not exist in the wiki."
    except AzureDevOpsError as e:
        return f"Error listing wiki pages: {e}"


@mcp.tool()
async def create_wiki_page(page_path: str, content: str) -> str:
    """
    Create a new wiki page at the given path with the provided Markdown content.

    Use this when a wiki page does not yet exist. Always call list_wiki_pages or
    read_wiki_page first to confirm the page does not already exist.

    Args:
        page_path: Full path for the new page. Example: /Sprints/Sprint-3/Planning
        content: Full Markdown content to write to the page.
    """
    try:
        page = await api.create_wiki_page(page_path, content)
        return f"Wiki page created successfully: {page.path}"
    except AzureDevOpsError as e:
        return f"Error creating wiki page '{page_path}': {e}"


@mcp.tool()
async def update_wiki_page(page_path: str, content: str) -> str:
    """
    Update the content of an existing wiki page.

    Use this to append sprint review notes, update architecture decisions, or
    revise any existing wiki documentation. The page must already exist.
    Always call read_wiki_page first to review current content before updating.

    Args:
        page_path: Path of the page to update. Example: /Architecture/Decisions/2025-auth
        content: New full Markdown content that will replace the current page content.
    """
    try:
        version = await api.get_wiki_page_version(page_path)
        page = await api.update_wiki_page(page_path, content, version)
        return f"Wiki page updated successfully: {page.path}"
    except NotFoundError:
        return f"Wiki page '{page_path}' does not exist. Use create_wiki_page instead."
    except AzureDevOpsError as e:
        return f"Error updating wiki page '{page_path}': {e}"
