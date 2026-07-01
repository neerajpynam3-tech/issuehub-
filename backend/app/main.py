"""FastAPI application entrypoint.

Wires together configuration, CORS, error handling, and all routers under /api.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.errors import register_error_handlers
from app.routers import auth, comments, issues, projects, users
from app.utils.logging import configure_logging

configure_logging()
logger = logging.getLogger("issuehub")

app = FastAPI(
    title="IssueHub API",
    version="1.0.0",
    description="A lightweight bug tracker: projects, issues, comments, and role-based access.",
)

# CORS so the React dev server can call the API from another origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_error_handlers(app)

# All routes are served under the /api prefix to match the API contract.
api_prefix = "/api"
app.include_router(auth.router, prefix=api_prefix)
app.include_router(users.router, prefix=api_prefix)
app.include_router(projects.router, prefix=api_prefix)
app.include_router(issues.router, prefix=api_prefix)
app.include_router(comments.router, prefix=api_prefix)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
