"""Project business logic: creation, membership, and access checks.

The membership helpers here (`require_member`, `require_maintainer`) are reused by
the issue and comment services, so authorization stays in one place.
"""

from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.models.enums import MemberRole
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.user import User
from app.repositories.project_repository import ProjectRepository
from app.repositories.user_repository import UserRepository
from app.schemas.project import AddMemberRequest, ProjectCreate


class ProjectService:
    def __init__(self, db: Session):
        self.projects = ProjectRepository(db)
        self.users = UserRepository(db)

    def create_project(self, data: ProjectCreate, creator: User) -> Project:
        """Create a project; the creator automatically becomes its maintainer."""
        key = data.key.upper()
        if self.projects.get_by_key(key):
            raise AppError(409, "key_taken", f"Project key '{key}' is already in use.")

        project = self.projects.create(name=data.name, key=key, description=data.description)
        self.projects.add_member(project.id, creator.id, MemberRole.maintainer)
        return project

    def list_my_projects(self, user: User) -> list[Project]:
        return self.projects.list_for_user(user.id)

    def add_member(self, project_id: int, data: AddMemberRequest, actor: User) -> ProjectMember:
        """Add a user (looked up by email) to a project. Maintainers only."""
        self.require_maintainer(project_id, actor)

        user = self.users.get_by_email(data.email)
        if user is None:
            raise AppError(404, "user_not_found", "No user found with that email.")

        if self.projects.get_member(project_id, user.id):
            raise AppError(409, "already_member", "User is already a member of this project.")

        return self.projects.add_member(project_id, user.id, data.role)

    def list_members(self, project_id: int, actor: User) -> list[ProjectMember]:
        self.require_member(project_id, actor)
        return self.projects.list_members(project_id)

    # ----- access helpers (shared with other services) -----

    def get_project_or_404(self, project_id: int) -> Project:
        project = self.projects.get_by_id(project_id)
        if project is None:
            raise AppError(404, "project_not_found", "Project does not exist.")
        return project

    def require_member(self, project_id: int, user: User) -> ProjectMember:
        """Ensure the user belongs to the project; return their membership."""
        self.get_project_or_404(project_id)
        member = self.projects.get_member(project_id, user.id)
        if member is None:
            raise AppError(403, "not_a_member", "You are not a member of this project.")
        return member

    def require_maintainer(self, project_id: int, user: User) -> ProjectMember:
        """Ensure the user is a maintainer of the project."""
        member = self.require_member(project_id, user)
        if member.role != MemberRole.maintainer:
            raise AppError(403, "not_maintainer", "This action requires the maintainer role.")
        return member
