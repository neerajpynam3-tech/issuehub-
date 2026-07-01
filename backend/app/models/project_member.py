from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import MemberRole


class ProjectMember(Base):
    """Join table linking users to projects, carrying their role in that project."""

    __tablename__ = "project_members"
    __table_args__ = (UniqueConstraint("project_id", "user_id", name="uq_project_user"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[MemberRole] = mapped_column(
        SAEnum(MemberRole, name="member_role"), default=MemberRole.member, nullable=False
    )

    project: Mapped["Project"] = relationship(back_populates="members")  # noqa: F821
    user: Mapped["User"] = relationship(back_populates="memberships")  # noqa: F821
