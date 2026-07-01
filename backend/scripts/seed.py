"""Seed the database with demo data.

Run after migrations:  python -m scripts.seed

Creates two users, two projects, a set of issues, and a few comments so the UI
has something to show. Safe to run repeatedly — it skips seeding if the demo
users already exist.
"""

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.comment import Comment
from app.models.enums import IssuePriority, IssueStatus, MemberRole
from app.models.issue import Issue
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.user import User

DEMO_PASSWORD = "password123"

ISSUES = [
    ("Login page returns 500", "Submitting the login form crashes the server.", IssueStatus.open, IssuePriority.critical),
    ("Slow dashboard load", "Dashboard takes 8s to render with many issues.", IssueStatus.in_progress, IssuePriority.high),
    ("Typo on signup button", "Button says 'Sigup' instead of 'Sign up'.", IssueStatus.open, IssuePriority.low),
    ("Email validation missing", "Invalid emails are accepted at signup.", IssueStatus.open, IssuePriority.medium),
    ("Logout does not clear token", "Token persists after logout.", IssueStatus.resolved, IssuePriority.high),
    ("Pagination off by one", "Last page shows duplicate items.", IssueStatus.open, IssuePriority.medium),
    ("Mobile layout broken", "Sidebar overlaps content on small screens.", IssueStatus.in_progress, IssuePriority.medium),
    ("Cannot assign issue", "Assignee dropdown is empty.", IssueStatus.open, IssuePriority.high),
    ("Search ignores case", "Search for 'Login' misses 'login'.", IssueStatus.closed, IssuePriority.low),
    ("Comment timestamps wrong", "Times shown in UTC, not local.", IssueStatus.open, IssuePriority.low),
    ("Add dark mode", "Users want a dark theme option.", IssueStatus.open, IssuePriority.low),
    ("Rate limit the API", "No protection against brute-force login.", IssueStatus.open, IssuePriority.high),
]


def seed() -> None:
    db = SessionLocal()
    try:
        if db.query(User).filter_by(email="alice@example.com").first():
            print("Demo data already present — skipping.")
            return

        alice = User(name="Alice Maintainer", email="alice@example.com", password_hash=hash_password(DEMO_PASSWORD))
        bob = User(name="Bob Member", email="bob@example.com", password_hash=hash_password(DEMO_PASSWORD))
        db.add_all([alice, bob])
        db.flush()

        web = Project(name="Web App", key="WEB", description="Customer-facing web application")
        api = Project(name="Public API", key="API", description="REST API service")
        db.add_all([web, api])
        db.flush()

        # Alice maintains both projects; Bob is a member of the web project.
        db.add_all([
            ProjectMember(project_id=web.id, user_id=alice.id, role=MemberRole.maintainer),
            ProjectMember(project_id=api.id, user_id=alice.id, role=MemberRole.maintainer),
            ProjectMember(project_id=web.id, user_id=bob.id, role=MemberRole.member),
        ])
        db.flush()

        for index, (title, description, status, priority) in enumerate(ISSUES):
            # Spread issues across the two projects; Bob reports the web ones.
            project = web if index % 2 == 0 else api
            reporter = bob if project is web else alice
            assignee = alice if priority in (IssuePriority.high, IssuePriority.critical) else None
            db.add(Issue(
                project_id=project.id,
                title=title,
                description=description,
                status=status,
                priority=priority,
                reporter_id=reporter.id,
                assignee_id=assignee.id if assignee else None,
            ))
        db.flush()

        first_issue = db.query(Issue).first()
        db.add_all([
            Comment(issue_id=first_issue.id, author_id=alice.id, body="Looking into this now."),
            Comment(issue_id=first_issue.id, author_id=bob.id, body="Thanks, it's blocking users."),
        ])

        db.commit()
        print("Seeded demo data.")
        print(f"  Login with: alice@example.com / {DEMO_PASSWORD} (maintainer)")
        print(f"           or bob@example.com / {DEMO_PASSWORD} (member)")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
