"""Enums shared by the models and schemas."""

from enum import Enum


class IssueStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"


class IssuePriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class MemberRole(str, Enum):
    member = "member"
    maintainer = "maintainer"
