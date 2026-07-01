from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.project import (
    AddMemberRequest,
    MemberResponse,
    ProjectCreate,
    ProjectResponse,
)
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


def _to_response(project, role) -> ProjectResponse:
    """Attach the caller's role so the frontend can show maintainer controls."""
    response = ProjectResponse.model_validate(project)
    response.my_role = role
    return response


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProjectService(db)
    project = service.create_project(data, current_user)
    member = service.projects.get_member(project.id, current_user.id)
    return _to_response(project, member.role if member else None)


@router.get("", response_model=list[ProjectResponse])
def list_my_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProjectService(db)
    projects = service.list_my_projects(current_user)
    result = []
    for project in projects:
        member = service.projects.get_member(project.id, current_user.id)
        result.append(_to_response(project, member.role if member else None))
    return result


@router.get("/{project_id}/members", response_model=list[MemberResponse])
def list_members(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ProjectService(db).list_members(project_id, current_user)


@router.post(
    "/{project_id}/members",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_member(
    project_id: int,
    data: AddMemberRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ProjectService(db).add_member(project_id, data, current_user)
