from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.enums import MemberRole
from app.schemas.user import UserResponse


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    key: str = Field(min_length=2, max_length=10, pattern=r"^[A-Za-z0-9]+$")
    description: str | None = Field(default=None, max_length=1000)


class ProjectResponse(BaseModel):
    id: int
    name: str
    key: str
    description: str | None
    created_at: datetime
    # The caller's role in this project, handy for the frontend to show/hide controls.
    my_role: MemberRole | None = None

    model_config = ConfigDict(from_attributes=True)


class AddMemberRequest(BaseModel):
    email: EmailStr
    role: MemberRole = MemberRole.member


class MemberResponse(BaseModel):
    user: UserResponse
    role: MemberRole

    model_config = ConfigDict(from_attributes=True)
