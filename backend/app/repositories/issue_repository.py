"""Database access for issues, including the filter/search/sort/paginate query."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.enums import IssuePriority, IssueStatus
from app.models.issue import Issue

# Whitelist of sortable columns -> the actual model attribute.
# Keeping this explicit prevents arbitrary/unsafe sort input.
_SORT_COLUMNS = {
    "created_at": Issue.created_at,
    "priority": Issue.priority,
    "status": Issue.status,
}


class IssueRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, issue_id: int) -> Issue | None:
        return self.db.get(Issue, issue_id)

    def create(self, **fields) -> Issue:
        issue = Issue(**fields)
        self.db.add(issue)
        self.db.commit()
        self.db.refresh(issue)
        return issue

    def save(self, issue: Issue) -> Issue:
        self.db.add(issue)
        self.db.commit()
        self.db.refresh(issue)
        return issue

    def delete(self, issue: Issue) -> None:
        self.db.delete(issue)
        self.db.commit()

    def search(
        self,
        project_id: int,
        *,
        q: str | None = None,
        status: IssueStatus | None = None,
        priority: IssuePriority | None = None,
        assignee_id: int | None = None,
        sort: str = "created_at",
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Issue], int]:
        """Return a page of issues plus the total count matching the filters."""
        conditions = [Issue.project_id == project_id]
        if q:
            conditions.append(Issue.title.ilike(f"%{q}%"))
        if status is not None:
            conditions.append(Issue.status == status)
        if priority is not None:
            conditions.append(Issue.priority == priority)
        if assignee_id is not None:
            conditions.append(Issue.assignee_id == assignee_id)

        total = self.db.scalar(select(func.count()).select_from(Issue).where(*conditions)) or 0

        sort_column = _SORT_COLUMNS.get(sort, Issue.created_at)
        stmt = (
            select(Issue)
            .where(*conditions)
            .order_by(sort_column.desc(), Issue.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        return list(self.db.scalars(stmt)), total
