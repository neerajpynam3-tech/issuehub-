"""Shared FastAPI dependencies (mainly resolving the current user)."""

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.errors import AppError
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository

# `auto_error=False` lets us raise our own structured 401 instead of FastAPI's default.
_bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise AppError(401, "not_authenticated", "Missing authentication token.")

    user_id = decode_access_token(credentials.credentials)
    if user_id is None:
        raise AppError(401, "invalid_token", "Token is invalid or expired.")

    user = UserRepository(db).get_by_id(int(user_id))
    if user is None:
        raise AppError(401, "user_not_found", "The token's user no longer exists.")

    return user
