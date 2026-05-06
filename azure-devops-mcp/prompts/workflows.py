from __future__ import annotations

from mcp.types import PromptMessage, TextContent

from server import mcp


@mcp.prompt()
def sprint_planning(sprint_name: str, sprint_iteration_path: str) -> list[PromptMessage]:
    """Kick off a structured sprint planning session for the given sprint."""
    return [PromptMessage(role="user", content=TextContent(type="text", text=f"""
Please conduct Sprint Planning for {sprint_name}.

Steps:
1. Load the current backlog: call list_work_items with state='New' and no iteration_path filter.
2. Identify all User Stories that are ready (have Acceptance Criteria and Story Points).
3. For each selected story, call move_work_item_to_sprint with iteration_path='{sprint_iteration_path}'.
4. Break each story into Tasks using create_work_item (type='Task', parent_id=<story_id>).
5. Write the sprint plan to the wiki using create_wiki_page at path /Sprints/{sprint_name}/Planning.
   Include: sprint goal, selected stories with IDs and story points, total capacity.
6. Report a summary of what was planned.
"""))]


@mcp.prompt()
def sprint_review(sprint_name: str, sprint_iteration_path: str) -> list[PromptMessage]:
    """Generate a sprint review and write it to the wiki."""
    return [PromptMessage(role="user", content=TextContent(type="text", text=f"""
Please conduct a Sprint Review for {sprint_name}.

Steps:
1. Call list_work_items with iteration_path='{sprint_iteration_path}' and state='Done' to get completed items.
2. Call list_work_items with iteration_path='{sprint_iteration_path}' and state='Active' to get incomplete items.
3. Calculate velocity (sum of story points from Done items).
4. Read the sprint planning wiki page at /Sprints/{sprint_name}/Planning to compare against the original plan.
5. Write the review to the wiki at /Sprints/{sprint_name}/Review. Include:
   - Delivered items (ID, title, story points)
   - Incomplete items and reason if known
   - Velocity vs planned capacity
   - Key observations
6. Report a summary.
"""))]


@mcp.prompt()
def generate_wiki_from_epic(epic_id: int) -> list[PromptMessage]:
    """Auto-generate wiki documentation from an Epic and its child hierarchy."""
    return [PromptMessage(role="user", content=TextContent(type="text", text=f"""
Generate wiki documentation from Epic #{epic_id} and its full hierarchy.

Steps:
1. Call get_work_item for Epic #{epic_id} to read its title and description.
2. Call get_work_item_children for Epic #{epic_id} to get its Features.
3. For each Feature, call get_work_item_children to get User Stories.
4. Write a wiki page at /Epics/Epic-{epic_id} summarizing:
   - Epic title and description
   - Feature list (ID, title, state, story points)
   - Story list per Feature (ID, title, acceptance criteria, state)
5. Report a summary of what was written.
"""))]
