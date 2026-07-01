"""Database access for issue comments."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.comment import Comment


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_for_issue(self, issue_id: int) -> list[Comment]:
        """Comments on an issue, oldest first so the thread reads top to bottom."""
        stmt = (
            select(Comment)
            .where(Comment.issue_id == issue_id)
            .order_by(Comment.created_at.asc())
        )
        return list(self.db.scalars(stmt))

    def create(self, issue_id: int, author_id: int, body: str) -> Comment:
        comment = Comment(issue_id=issue_id, author_id=author_id, body=body)
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment
