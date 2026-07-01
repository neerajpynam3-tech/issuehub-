from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.user import UserResponse


class CommentCreate(BaseModel):
    body: str = Field(min_length=1, max_length=5000)


class CommentResponse(BaseModel):
    id: int
    issue_id: int
    body: str
    author: UserResponse
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
