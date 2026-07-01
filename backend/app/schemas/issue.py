from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import IssuePriority, IssueStatus
from app.schemas.user import UserResponse


class IssueCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    priority: IssuePriority = IssuePriority.medium
    assignee_id: int | None = None


class IssueUpdate(BaseModel):
    """Every field is optional — only the keys present in the request are changed."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: IssueStatus | None = None
    priority: IssuePriority | None = None
    assignee_id: int | None = None


class IssueResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: str | None
    status: IssueStatus
    priority: IssuePriority
    reporter: UserResponse
    assignee: UserResponse | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ----- AI "Enhance Issue Description" feature -----

class EnhanceRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)


class EnhanceResponse(BaseModel):
    enhanced_description: str
    provider: str
