"""Importing the models here ensures Alembic and SQLAlchemy see every table."""

from app.models.comment import Comment
from app.models.issue import Issue
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.user import User

__all__ = ["User", "Project", "ProjectMember", "Issue", "Comment"]
