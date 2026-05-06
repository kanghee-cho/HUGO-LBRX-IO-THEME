from __future__ import annotations

import base64
import json
import logging

import httpx

from client.models import Dashboard, Iteration, Widget, WikiInfo, WikiPage, WikiPageSummary, WorkItem, WorkItemComment
from exceptions import AuthenticationError, AzureDevOpsError, NotFoundError

logger = logging.getLogger(__name__)

API_VERSION = "7.1"

# Fields that support Markdown rendering via the multilineFieldsFormat hint
_MARKDOWN_FIELDS: frozenset[str] = frozenset({
    "System.Description",
    "Microsoft.VSTS.Common.AcceptanceCriteria",
    "Microsoft.VSTS.TCM.ReproSteps",
})


class AzureDevOpsClient:
    """HTTP client for the Azure DevOps REST API."""

    def __init__(self, org_url: str, project: str, pat: str, wiki_id: str, timeout: int = 30) -> None:
        token = base64.b64encode(f":{pat}".encode()).decode()
        self._org_url = org_url.rstrip("/")
        self._project = project
        self._base = f"{self._org_url}/{project}"
        self._wiki_id = wiki_id
        self._wiki_provisioned: bool = False
        self._http = httpx.AsyncClient(
            headers={
                "Authorization": f"Basic {token}",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )

    async def __aenter__(self) -> AzureDevOpsClient:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self._http.aclose()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _url(self, path: str) -> str:
        return f"{self._base}/_apis/{path}"

    def _org_api_url(self, path: str) -> str:
        """Build an org-level API URL (not project-scoped). Used for wiki provisioning."""
        return f"{self._org_url}/_apis/{path}"

    def _params(self, extra: dict | None = None) -> dict:
        p = {"api-version": API_VERSION}
        if extra:
            p.update(extra)
        return p

    @staticmethod
    def _normalize_md(text: str) -> str:
        """Normalize Markdown text for Azure DevOps.

        Converts literal two-character escape sequences (``\\n``, ``\\t``) into
        their actual control characters so they render correctly in Azure DevOps
        rather than appearing as raw backslash-letter text.
        """
        return text.replace("\\n", "\n").replace("\\t", "\t")

    @staticmethod
    def _field_ops(field: str, value: object, op: str = "add") -> list[dict]:
        """Build PATCH ops for a single field.

        For multiline fields (Description, AcceptanceCriteria, ReproSteps),
        appends a ``multilineFieldsFormat`` op so Azure DevOps renders the
        content as Markdown instead of plain text, and normalizes any literal
        ``\\n`` escape sequences to real newlines.
        """
        if field in _MARKDOWN_FIELDS and isinstance(value, str):
            value = AzureDevOpsClient._normalize_md(value)
            ops: list[dict] = [{"op": op, "path": f"/fields/{field}", "value": value}]
            ops.append({"op": "add", "path": f"/multilineFieldsFormat/{field}", "value": "Markdown"})
        else:
            ops = [{"op": op, "path": f"/fields/{field}", "value": value}]
        return ops

    async def _get(self, path: str, params: dict | None = None) -> dict:
        url = self._url(path)
        resp = await self._http.get(url, params=self._params(params))
        return self._handle(resp)

    async def _post(self, path: str, body: dict, params: dict | None = None) -> dict:
        url = self._url(path)
        resp = await self._http.post(url, json=body, params=self._params(params))
        return self._handle(resp)

    async def _patch(self, path: str, body: list | dict, content_type: str = "application/json",
                     params: dict | None = None) -> dict:
        url = self._url(path)
        headers = {"Content-Type": content_type}
        resp = await self._http.patch(url, content=json.dumps(body), headers=headers,
                                      params=self._params(params))
        return self._handle(resp)

    async def _put(self, path: str, body: dict, params: dict | None = None) -> dict:
        url = self._url(path)
        resp = await self._http.put(url, json=body, params=self._params(params))
        return self._handle(resp)

    def _handle(self, resp: httpx.Response) -> dict:
        if resp.status_code == 401:
            raise AuthenticationError("PAT is invalid or lacks required permissions.")
        if resp.status_code == 403:
            raise AuthenticationError("PAT lacks permissions for this operation.")
        if resp.status_code == 404:
            raise NotFoundError(f"Resource not found: {resp.url}")
        if not resp.is_success:
            raise AzureDevOpsError(f"HTTP {resp.status_code}: {resp.text[:400]}")
        return resp.json() if resp.content else {}

    # ------------------------------------------------------------------
    # Wiki — provisioning + CRUD
    # ------------------------------------------------------------------

    async def _ensure_wiki(self) -> None:
        """Lazily provision the project wiki if it does not yet exist.

        Checks once per client lifetime. On first call, queries the list of
        wikis for the project. If the configured wiki_id is not found, creates
        a new ``projectWiki`` and updates ``self._wiki_id`` to the actual name
        returned by the API.
        """
        if self._wiki_provisioned:
            return

        # List all wikis for this project
        url = self._org_api_url("wiki/wikis")
        resp = await self._http.get(url, params={"api-version": API_VERSION, "projectId": self._project})
        data = self._handle(resp)
        wikis: list[dict] = data.get("value", [])

        # Check whether the configured wiki already exists
        existing = next(
            (w for w in wikis if w.get("name") == self._wiki_id or w.get("id") == self._wiki_id),
            None,
        )
        if existing:
            self._wiki_id = existing["name"]
            self._wiki_provisioned = True
            logger.info("Wiki '%s' already exists — provisioning skipped.", self._wiki_id)
            return

        # Wiki not found — provision it
        logger.info("Wiki '%s' not found. Provisioning a new projectWiki…", self._wiki_id)
        project_id = await self._get_project_id()
        create_url = self._org_api_url("wiki/wikis")
        create_resp = await self._http.post(
            create_url,
            json={"type": "projectWiki", "name": self._wiki_id, "projectId": project_id},
            params={"api-version": API_VERSION},
        )
        created = self._handle(create_resp)
        self._wiki_id = created.get("name", self._wiki_id)
        self._wiki_provisioned = True
        logger.info("Wiki provisioned successfully: '%s'.", self._wiki_id)

    async def _get_project_id(self) -> str:
        """Return the GUID of the current project."""
        url = f"{self._org_url}/_apis/projects/{self._project}"
        resp = await self._http.get(url, params={"api-version": API_VERSION})
        data = self._handle(resp)
        return str(data["id"])

    async def list_wikis(self) -> list[WikiInfo]:
        """Return all wikis provisioned for this project."""
        url = self._org_api_url("wiki/wikis")
        resp = await self._http.get(url, params={"api-version": API_VERSION, "projectId": self._project})
        data = self._handle(resp)
        return [WikiInfo.model_validate(w) for w in data.get("value", [])]

    async def get_wiki_page(self, page_path: str, include_content: bool = True) -> WikiPage:
        """Read a wiki page by path."""
        await self._ensure_wiki()
        params: dict = {"path": page_path}
        if include_content:
            params["includeContent"] = "true"
        data = await self._get(f"wiki/wikis/{self._wiki_id}/pages", params)
        return WikiPage.model_validate(data)

    async def list_wiki_pages(self, path: str = "/", depth: int = 2) -> list[WikiPageSummary]:
        """List wiki pages under a path (recursive up to depth)."""
        await self._ensure_wiki()
        params = {"path": path, "recursionLevel": str(depth)}
        data = await self._get(f"wiki/wikis/{self._wiki_id}/pages", params)
        return [WikiPageSummary.model_validate(p) for p in data.get("subPages", [])]

    async def create_wiki_page(self, page_path: str, content: str) -> WikiPage:
        """Create a new wiki page. Auto-provisions the wiki if it does not yet exist."""
        await self._ensure_wiki()
        body = {"content": content}
        params = {"path": page_path}
        data = await self._put(f"wiki/wikis/{self._wiki_id}/pages", body, params)
        return WikiPage.model_validate(data)

    async def update_wiki_page(self, page_path: str, content: str, version: str) -> WikiPage:
        """Update a wiki page. Requires the current ETag version."""
        await self._ensure_wiki()
        body = {"content": content}
        params = {"path": page_path}
        url = self._url(f"wiki/wikis/{self._wiki_id}/pages")
        resp = await self._http.put(
            url,
            json=body,
            params=self._params(params),
            headers={"If-Match": version},
        )
        return WikiPage.model_validate(self._handle(resp))

    async def get_wiki_page_version(self, page_path: str) -> str:
        """Return the ETag of the current wiki page version (needed for updates)."""
        await self._ensure_wiki()
        params = {"path": page_path}
        url = self._url(f"wiki/wikis/{self._wiki_id}/pages")
        resp = await self._http.get(url, params=self._params(params))
        self._handle(resp)
        return resp.headers.get("ETag", "")

    # ------------------------------------------------------------------
    # Work Items
    # ------------------------------------------------------------------

    async def get_work_item(self, item_id: int) -> WorkItem:
        """Get a single work item by ID with all fields and relations."""
        data = await self._get(f"wit/workitems/{item_id}", {"$expand": "relations"})
        return WorkItem.model_validate(data)

    async def get_work_items_batch(self, ids: list[int]) -> list[WorkItem]:
        """Batch-fetch work items by IDs (max 200 per call)."""
        if not ids:
            return []
        csv = ",".join(str(i) for i in ids[:200])
        data = await self._get("wit/workitems", {"ids": csv, "$expand": "relations"})
        return [WorkItem.model_validate(item) for item in data.get("value", [])]

    async def query_work_items(self, wiql: str) -> list[int]:
        """Run a WIQL query and return matching work item IDs."""
        data = await self._post("wit/wiql", {"query": wiql})
        return [item["id"] for item in data.get("workItems", [])]

    async def create_work_item(
        self,
        work_item_type: str,
        title: str,
        description: str = "",
        acceptance_criteria: str = "",
        story_points: float | None = None,
        iteration_path: str = "",
        area_path: str = "",
        parent_id: int | None = None,
        tags: str = "",
    ) -> WorkItem:
        """Create a new work item of the given type."""
        ops: list[dict] = [
            {"op": "add", "path": "/fields/System.Title", "value": title},
        ]
        if description:
            ops.extend(self._field_ops("System.Description", description))
        if acceptance_criteria:
            ops.extend(self._field_ops("Microsoft.VSTS.Common.AcceptanceCriteria", acceptance_criteria))
        if story_points is not None:
            ops.append({"op": "add", "path": "/fields/Microsoft.VSTS.Scheduling.StoryPoints",
                        "value": story_points})
        if iteration_path:
            ops.append({"op": "add", "path": "/fields/System.IterationPath", "value": iteration_path})
        if area_path:
            ops.append({"op": "add", "path": "/fields/System.AreaPath", "value": area_path})
        if tags:
            ops.append({"op": "add", "path": "/fields/System.Tags", "value": tags})
        if parent_id is not None:
            parent_url = f"{self._base}/_apis/wit/workitems/{parent_id}"
            ops.append({"op": "add", "path": "/relations/-",
                        "value": {"rel": "System.LinkTypes.Hierarchy-Reverse", "url": parent_url}})

        data = await self._patch(
            f"wit/workitems/${work_item_type}",
            ops,
            content_type="application/json-patch+json",
        )
        return WorkItem.model_validate(data)

    async def update_work_item(self, item_id: int, fields: dict[str, object]) -> WorkItem:
        """Update arbitrary fields on a work item.

        Args:
            item_id: Work item ID.
            fields: Mapping of field reference name → new value.
                    e.g., {"System.State": "Active", "Microsoft.VSTS.Scheduling.StoryPoints": 5}
        """
        ops: list[dict] = []
        for k, v in fields.items():
            ops.extend(self._field_ops(k, v, op="replace"))
        data = await self._patch(
            f"wit/workitems/{item_id}",
            ops,
            content_type="application/json-patch+json",
        )
        return WorkItem.model_validate(data)

    async def add_work_item_comment(self, item_id: int, text: str) -> WorkItemComment:
        """Add a comment to a work item."""
        data = await self._post(f"wit/workitems/{item_id}/comments", {"text": text})
        return WorkItemComment.model_validate(data)

    # ------------------------------------------------------------------
    # Iterations (Sprints)
    # ------------------------------------------------------------------

    async def get_current_iteration(self) -> Iteration:
        """Return the current sprint iteration for the team."""
        data = await self._get("work/teamsettings/iterations", {"$timeframe": "current"})
        values = data.get("value", [])
        if not values:
            raise NotFoundError("No current iteration found.")
        return Iteration.model_validate(values[0])

    async def list_iterations(self) -> list[Iteration]:
        """List all iterations (sprints) defined in the project."""
        data = await self._get("work/teamsettings/iterations")
        return [Iteration.model_validate(i) for i in data.get("value", [])]

    # ------------------------------------------------------------------
    # Dashboards
    # ------------------------------------------------------------------

    async def list_dashboards(self) -> list[Dashboard]:
        """List all dashboards in the project."""
        data = await self._get("dashboard/dashboards")
        return [Dashboard.model_validate(d) for d in data.get("dashboardEntries", [])]

    async def get_dashboard(self, dashboard_id: str) -> Dashboard:
        """Get a dashboard and its widgets by ID."""
        data = await self._get(f"dashboard/dashboards/{dashboard_id}")
        return Dashboard.model_validate(data)

    async def add_widget(self, dashboard_id: str, widget: dict) -> Widget:
        """Add a widget to a dashboard."""
        data = await self._post(f"dashboard/dashboards/{dashboard_id}/widgets", widget)
        return Widget.model_validate(data)
