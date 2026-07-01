"""Authentication business logic: signup and login."""

from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, SignupRequest


class AuthService:
    def __init__(self, db: Session):
        self.users = UserRepository(db)

    def signup(self, data: SignupRequest) -> User:
        """Register a new user, rejecting duplicate emails."""
        if self.users.get_by_email(data.email):
            raise AppError(409, "email_taken", "An account with this email already exists.")

        return self.users.create(
            name=data.name,
            email=data.email,
            password_hash=hash_password(data.password),
        )

    def login(self, data: LoginRequest) -> str:
        """Verify credentials and return a signed access token."""
        user = self.users.get_by_email(data.email)
        # Same error whether the email or password is wrong, to avoid leaking which.
        if user is None or not verify_password(data.password, user.password_hash):
            raise AppError(401, "invalid_credentials", "Incorrect email or password.")

        return create_access_token(user.id)
