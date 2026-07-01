"""Comment business logic: list and add comments on an issue."""

from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.models.comment import Comment
from app.models.user import User
from app.repositories.comment_repository import CommentRepository
from app.repositories.issue_repository import IssueRepository
from app.services.project_service import ProjectService


class CommentService:
    def __init__(self, db: Session):
        self.comments = CommentRepository(db)
        self.issues = IssueRepository(db)
        self.projects = ProjectService(db)

    def list_comments(self, issue_id: int, actor: User) -> list[Comment]:
        issue = self._get_issue_or_404(issue_id)
        self.projects.require_member(issue.project_id, actor)
        return self.comments.list_for_issue(issue_id)

    def add_comment(self, issue_id: int, body: str, author: User) -> Comment:
        """Any project member may comment on an issue."""
        issue = self._get_issue_or_404(issue_id)
        self.projects.require_member(issue.project_id, author)
        return self.comments.create(issue_id=issue_id, author_id=author.id, body=body)

    def _get_issue_or_404(self, issue_id: int):
        issue = self.issues.get_by_id(issue_id)
        if issue is None:
            raise AppError(404, "issue_not_found", "Issue does not exist.")
        return issue
