from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentResponse
from app.services.comment_service import CommentService

router = APIRouter(tags=["comments"])


@router.get("/issues/{issue_id}/comments", response_model=list[CommentResponse])
def list_comments(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return CommentService(db).list_comments(issue_id, current_user)


@router.post(
    "/issues/{issue_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_comment(
    issue_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return CommentService(db).add_comment(issue_id, data.body, current_user)
