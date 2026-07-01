from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.enums import IssuePriority, IssueStatus
from app.models.user import User
from app.schemas.common import Page
from app.schemas.issue import (
    EnhanceRequest,
    EnhanceResponse,
    IssueCreate,
    IssueResponse,
    IssueUpdate,
)
from app.services.ai_service import AIService
from app.services.issue_service import IssueService

router = APIRouter(tags=["issues"])


# --- AI enhance: declared before /issues/{issue_id} so it is not shadowed ---
@router.post("/issues/enhance", response_model=EnhanceResponse)
def enhance_description(
    data: EnhanceRequest,
    _: User = Depends(get_current_user),
):
    """Bonus AI feature: turn a rough title/description into a structured report."""
    return AIService().enhance_description(data.title, data.description)


# --- project-scoped issue endpoints ---
@router.get("/projects/{project_id}/issues", response_model=Page[IssueResponse])
def list_issues(
    project_id: int,
    q: str | None = Query(default=None, description="Text search in the issue title"),
    status: IssueStatus | None = None,
    priority: IssuePriority | None = None,
    assignee: int | None = Query(default=None, description="Filter by assignee user id"),
    sort: str = Query(default="created_at", pattern="^(created_at|priority|status)$"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items, total = IssueService(db).list_issues(
        project_id,
        current_user,
        q=q,
        status=status,
        priority=priority,
        assignee_id=assignee,
        sort=sort,
        page=page,
        page_size=page_size,
    )
    return Page(items=items, total=total, page=page, page_size=page_size)


@router.post(
    "/projects/{project_id}/issues",
    response_model=IssueResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_issue(
    project_id: int,
    data: IssueCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return IssueService(db).create_issue(project_id, data, current_user)


# --- issue-scoped endpoints ---
@router.get("/issues/{issue_id}", response_model=IssueResponse)
def get_issue(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return IssueService(db).get_issue(issue_id, current_user)


@router.patch("/issues/{issue_id}", response_model=IssueResponse)
def update_issue(
    issue_id: int,
    data: IssueUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return IssueService(db).update_issue(issue_id, data, current_user)


@router.delete("/issues/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    IssueService(db).delete_issue(issue_id, current_user)
