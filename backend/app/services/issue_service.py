"""Issue business logic: CRUD, search, and role-based field changes.

Authorization rules (from the spec):
  - Any project member may view and create issues, and search within the project.
  - The reporter may edit their own issue's title/description/priority.
  - Only a maintainer may change status or assignee, or delete an issue.
"""

from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.models.enums import IssuePriority, IssueStatus, MemberRole
from app.models.issue import Issue
from app.models.user import User
from app.repositories.issue_repository import IssueRepository
from app.schemas.issue import IssueCreate, IssueUpdate
from app.services.project_service import ProjectService


class IssueService:
    def __init__(self, db: Session):
        self.issues = IssueRepository(db)
        self.projects = ProjectService(db)

    def create_issue(self, project_id: int, data: IssueCreate, reporter: User) -> Issue:
        self.projects.require_member(project_id, reporter)
        if data.assignee_id is not None:
            self._ensure_assignee_is_member(project_id, data.assignee_id)

        return self.issues.create(
            project_id=project_id,
            title=data.title,
            description=data.description,
            priority=data.priority,
            assignee_id=data.assignee_id,
            reporter_id=reporter.id,
        )

    def list_issues(
        self,
        project_id: int,
        actor: User,
        *,
        q: str | None,
        status: IssueStatus | None,
        priority: IssuePriority | None,
        assignee_id: int | None,
        sort: str,
        page: int,
        page_size: int,
    ) -> tuple[list[Issue], int]:
        self.projects.require_member(project_id, actor)
        return self.issues.search(
            project_id,
            q=q,
            status=status,
            priority=priority,
            assignee_id=assignee_id,
            sort=sort,
            page=page,
            page_size=page_size,
        )

    def get_issue(self, issue_id: int, actor: User) -> Issue:
        issue = self._get_or_404(issue_id)
        self.projects.require_member(issue.project_id, actor)
        return issue

    def update_issue(self, issue_id: int, data: IssueUpdate, actor: User) -> Issue:
        issue = self._get_or_404(issue_id)
        member = self.projects.require_member(issue.project_id, actor)
        is_maintainer = member.role == MemberRole.maintainer

        changes = data.model_dump(exclude_unset=True)
        maintainer_only = {"status", "assignee_id"}.intersection(changes)
        reporter_fields = {"title", "description", "priority"}.intersection(changes)

        # Only maintainers may touch status/assignee.
        if maintainer_only and not is_maintainer:
            raise AppError(403, "not_maintainer", "Only a maintainer can change status or assignee.")

        # Descriptive fields can be edited by the reporter or any maintainer.
        if reporter_fields and issue.reporter_id != actor.id and not is_maintainer:
            raise AppError(403, "not_allowed", "Only the reporter or a maintainer can edit this issue.")

        if "assignee_id" in changes and changes["assignee_id"] is not None:
            self._ensure_assignee_is_member(issue.project_id, changes["assignee_id"])

        for field, value in changes.items():
            setattr(issue, field, value)

        return self.issues.save(issue)

    def delete_issue(self, issue_id: int, actor: User) -> None:
        issue = self._get_or_404(issue_id)
        self.projects.require_maintainer(issue.project_id, actor)
        self.issues.delete(issue)

    # ----- helpers -----

    def _get_or_404(self, issue_id: int) -> Issue:
        issue = self.issues.get_by_id(issue_id)
        if issue is None:
            raise AppError(404, "issue_not_found", "Issue does not exist.")
        return issue

    def _ensure_assignee_is_member(self, project_id: int, assignee_id: int) -> None:
        if self.projects.projects.get_member(project_id, assignee_id) is None:
            raise AppError(400, "invalid_assignee", "Assignee must be a member of the project.")
