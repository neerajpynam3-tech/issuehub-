"""Database access for projects and their membership rows."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import MemberRole
from app.models.project import Project
from app.models.project_member import ProjectMember


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, project_id: int) -> Project | None:
        return self.db.get(Project, project_id)

    def get_by_key(self, key: str) -> Project | None:
        return self.db.scalar(select(Project).where(Project.key == key))

    def create(self, name: str, key: str, description: str | None) -> Project:
        project = Project(name=name, key=key, description=description)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def list_for_user(self, user_id: int) -> list[Project]:
        """Projects the user is a member of, newest first."""
        stmt = (
            select(Project)
            .join(ProjectMember, ProjectMember.project_id == Project.id)
            .where(ProjectMember.user_id == user_id)
            .order_by(Project.created_at.desc())
        )
        return list(self.db.scalars(stmt))

    # ----- membership -----

    def get_member(self, project_id: int, user_id: int) -> ProjectMember | None:
        stmt = select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id,
        )
        return self.db.scalar(stmt)

    def list_members(self, project_id: int) -> list[ProjectMember]:
        stmt = select(ProjectMember).where(ProjectMember.project_id == project_id)
        return list(self.db.scalars(stmt))

    def add_member(self, project_id: int, user_id: int, role: MemberRole) -> ProjectMember:
        member = ProjectMember(project_id=project_id, user_id=user_id, role=role)
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member
