# IssueHub

A small bug tracker: create projects, file issues, comment, assign owners, and track
status. Email/password auth with two roles, member and maintainer.

FastAPI + Postgres on the backend, React (Vite) on the frontend, JWT auth.

## Live demo

https://issuehub-frontend-up9e.onrender.com

Seeded logins:

- `alice@example.com` / `password123` (maintainer)
- `bob@example.com` / `password123` (member)

It's on Render's free tier, so the first request after it's been idle can take 30-50s to
wake up.

## Run locally

Needs Python 3.11+ and Node 18+. The backend reads `DATABASE_URL`, so any Postgres works.
Easiest is a free [Neon](https://neon.tech) database (no Docker). Copy its connection
string in the psycopg2 form, e.g. `postgresql+psycopg2://user:pass@host/db?sslmode=require`.

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # set DATABASE_URL
alembic upgrade head              # run migrations
python -m scripts.seed            # optional demo data
uvicorn app.main:app --reload     # http://localhost:8000, docs at /docs
```

Frontend:

```bash
cd frontend
npm install
cp .env.example .env              # VITE_API_URL defaults to http://localhost:8000/api
npm run dev                       # http://localhost:5173
```

No Neon? `docker compose up -d db` runs Postgres locally; then point `DATABASE_URL` at
`postgresql+psycopg2://issuehub:issuehub@localhost:5432/issuehub` (use `DB_HOST_PORT=5433`
in a root `.env` if 5432 is taken).

## Tests

```bash
cd backend && pytest
```

They run on an in-memory SQLite DB (`conftest.py` overrides `get_db`), so you don't need
Postgres. They cover signup/login, project membership and scoping, issue CRUD and search,
and the role rules (a plain member can't change an issue's status, etc.).

## Env vars

Backend (`backend/.env`): `DATABASE_URL`, `JWT_SECRET`, `JWT_EXPIRE_MINUTES` (default
1440), `CORS_ORIGINS` (default `http://localhost:5173`), `AI_PROVIDER` (`mock`).

Frontend (`frontend/.env`): `VITE_API_URL` (default `http://localhost:8000/api`).

## Structure

The backend is layered. Routers parse the request and call a service; services hold the
business rules and the authorization checks; repositories run the queries. Pydantic
schemas validate input and shape responses so the ORM models don't leak into the API. The
shared stuff (config, db session, security, current-user dependency, error handler) is in
`app/core`.

```
backend/app/   core, models, schemas, repositories, services, routers
frontend/src/  services, context, pages, components
```

Data model: `users`, `projects`, and a `project_members` join table that carries the role
(member or maintainer). An issue belongs to a project and has a reporter, an optional
assignee, a status (open / in_progress / resolved / closed) and a priority (low / medium /
high / critical). Comments belong to an issue. Status, priority and role are stored as
real Postgres enums, and deleting a project or issue cascades to its children.

## API

Everything is under `/api`, and Swagger is at `/docs`. Main routes:

```
Auth       POST /auth/signup   POST /auth/login   GET /me
Projects   GET|POST /projects   GET|POST /projects/{id}/members
           GET|POST /projects/{id}/issues   (?q, status, priority, assignee, sort, page)
Issues     GET|PATCH|DELETE /issues/{id}
           GET|POST /issues/{id}/comments
           POST /issues/enhance   (bonus AI)
```

Errors come back as `{"error": {"code", "message", "details"}}`. A few things differ from
the sample contract in the brief: the issue list is paginated (`{items, total, page,
page_size}`), the `assignee` filter takes a user id, and login returns `{access_token,
token_type}`.

## Auth and roles

Passwords are hashed with bcrypt. Login returns a JWT whose subject is the user id; the
frontend keeps it in localStorage and an axios interceptor attaches it to every request
(and sends you to /login on a 401). The services enforce the rules:

- any member of a project can view and create issues, and comment
- the reporter can edit their own issue's title, description and priority
- only a maintainer can change status or assignee, delete issues, or add members

Those maintainer-only controls are hidden in the UI for everyone else too, so the backend
check is just the backstop.

## AI feature (bonus)

`POST /api/issues/enhance` takes a rough title and description and returns a more
structured writeup (summary, steps to reproduce, expected vs. actual). The "AI Enhance"
button in the new-issue dialog uses it. It lives behind `app/services/ai_service.py` as a
mock; a real Gemini or OpenAI call would be one more branch there reading `AI_API_KEY`.
Nothing needs a key to run the project.

## Trade-offs and next steps

FastAPI mainly for the request validation and the automatic API docs. The
router/service/repository split is a few more files but keeps each part small and puts all
the auth in one place. JWT in localStorage is simple and matches the contract; for
something with real data I'd switch to an httpOnly cookie with CSRF. Plain CSS since I
didn't want a UI framework for an app this size.

With more time: token refresh and logout revocation, rate limiting on the auth routes, a
real AI provider, some frontend tests, a fuller member-management UI (right now you can
only add by email), and search across descriptions and comments instead of just titles.

## Deploy

Both halves run on Render with the database on Neon, all driven by env vars. Quickest is
Render's Blueprint (New + > Blueprint, pick this repo, `render.yaml` creates both
services), then set the secrets: the backend needs `DATABASE_URL`, `JWT_SECRET`, and
`AI_PROVIDER=mock`; the frontend needs `VITE_API_URL = <backend-url>/api`. Deploy the
backend first, then the frontend, then set the backend's `CORS_ORIGINS` to the frontend
URL. This deployment: backend `https://issuehub-backend-choi.onrender.com`, frontend
`https://issuehub-frontend-up9e.onrender.com`.
