from __future__ import annotations

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Wiki
# ---------------------------------------------------------------------------

class WikiPage(BaseModel):
    """A single Azure DevOps wiki page."""
    path: str
    content: str = ""
    url: str = ""
    remote_url: str = Field("", alias="remoteUrl")
    is_parent_page: bool = Field(False, alias="isParentPage")

    model_config = {"populate_by_name": True}


class WikiPageSummary(BaseModel):
    """Lightweight page reference returned by list operations."""
    path: str
    url: str = ""
    sub_pages: list[WikiPageSummary] = Field([], alias="subPages")

    model_config = {"populate_by_name": True}


class WikiInfo(BaseModel):
    """Metadata about a provisioned Azure DevOps wiki."""
    id: str
    name: str
    project_id: str = Field("", alias="projectId")
    type: str = ""
    url: str = ""

    model_config = {"populate_by_name": True}


# ---------------------------------------------------------------------------
# Work Items
# ---------------------------------------------------------------------------

class WorkItemFields(BaseModel):
    """Flattened view of commonly used Azure DevOps work item fields."""
    title: str = Field("", alias="System.Title")
    work_item_type: str = Field("", alias="System.WorkItemType")
    state: str = Field("", alias="System.State")
    description: str = Field("", alias="System.Description")
    acceptance_criteria: str = Field("", alias="Microsoft.VSTS.Common.AcceptanceCriteria")
    iteration_path: str = Field("", alias="System.IterationPath")
    area_path: str = Field("", alias="System.AreaPath")
    story_points: float | None = Field(None, alias="Microsoft.VSTS.Scheduling.StoryPoints")
    tags: str = Field("", alias="System.Tags")
    parent_id: int | None = Field(None, alias="System.Parent")
    assigned_to: dict | None = Field(None, alias="System.AssignedTo")
    created_date: str = Field("", alias="System.CreatedDate")
    changed_date: str = Field("", alias="System.ChangedDate")

    model_config = {"populate_by_name": True}

    @property
    def assigned_to_name(self) -> str:
        if self.assigned_to:
            return self.assigned_to.get("displayName", "")
        return ""


class WorkItemRelation(BaseModel):
    rel: str
    url: str
    attributes: dict = {}


class WorkItem(BaseModel):
    """A single Azure DevOps work item."""
    id: int
    rev: int = 0
    fields: WorkItemFields
    relations: list[WorkItemRelation] = []
    url: str = ""

    @property
    def child_ids(self) -> list[int]:
        """Return IDs of direct child work items."""
        child_rel = "System.LinkTypes.Hierarchy-Forward"
        return [
            int(r.url.rstrip("/").split("/")[-1])
            for r in self.relations
            if r.rel == child_rel
        ]


class WorkItemComment(BaseModel):
    id: int
    text: str
    created_by: dict = Field({}, alias="createdBy")
    created_date: str = Field("", alias="createdDate")

    model_config = {"populate_by_name": True}


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

class Widget(BaseModel):
    id: str = ""
    name: str
    type_id: str = Field("", alias="typeId")
    position: dict = {}
    size: dict = {}
    settings: str | None = None

    model_config = {"populate_by_name": True}


class Dashboard(BaseModel):
    id: str = ""
    name: str
    description: str = ""
    widgets: list[Widget] = []
    url: str = ""


# ---------------------------------------------------------------------------
# Sprint / Iteration
# ---------------------------------------------------------------------------

class IterationAttributes(BaseModel):
    start_date: str = Field("", alias="startDate")
    finish_date: str = Field("", alias="finishDate")
    time_frame: str = Field("", alias="timeFrame")  # past | current | future

    model_config = {"populate_by_name": True}


class Iteration(BaseModel):
    id: str
    name: str
    path: str
    attributes: IterationAttributes
    url: str = ""
