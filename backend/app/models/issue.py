from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import IssuePriority, IssueStatus


class Issue(Base):
    __tablename__ = "issues"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[IssueStatus] = mapped_column(
        SAEnum(IssueStatus, name="issue_status"), default=IssueStatus.open, nullable=False
    )
    priority: Mapped[IssuePriority] = mapped_column(
        SAEnum(IssuePriority, name="issue_priority"), default=IssuePriority.medium, nullable=False
    )
    reporter_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    assignee_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    project: Mapped["Project"] = relationship(back_populates="issues")  # noqa: F821
    reporter: Mapped["User"] = relationship(foreign_keys=[reporter_id])  # noqa: F821
    assignee: Mapped["User | None"] = relationship(foreign_keys=[assignee_id])  # noqa: F821
    comments: Mapped[list["Comment"]] = relationship(  # noqa: F821
        back_populates="issue", cascade="all, delete-orphan"
    )
