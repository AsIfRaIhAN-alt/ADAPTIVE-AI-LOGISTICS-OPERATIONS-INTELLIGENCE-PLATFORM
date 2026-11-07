# AI Procurement Decision-Support System: Backend (Stage 1: Authentication)

FastAPI + SQLAlchemy backend. This stage covers FR1 (organization registration) and FR2 (role-based accounts).

## Setup
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # Windows: copy .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(48))"   # paste the output as SECRET_KEY in .env
uvicorn app.main:app --reload
```
Open http://localhost:8000/docs for the interactive API (Swagger).
Tables are created automatically on startup. For PostgreSQL, set `DATABASE_URL` in `.env`.

## Run tests
```bash
pytest -q
```

## Endpoints
| Method | Path | Access | Purpose |
|---|---|---|---|
| POST | /api/auth/register-organization | public | Create organization + first admin (FR1) |
| POST | /api/auth/login | public | Login (JSON), returns JWT |
| POST | /api/auth/token | public | Same, form-encoded (Swagger "Authorize") |
| GET | /api/users/me | any logged-in user | Own profile |
| POST | /api/users | admin | Create staff account in own organization |
| GET | /api/users | admin | List users of own organization |

## Security decisions (be ready to explain these)
- Passwords hashed with **bcrypt** (salted, slow); only the hash is stored.
- **No hardcoded secrets**: `SECRET_KEY` comes from `.env`; app won't start without it.
- Input validated with **Pydantic** (email format, password strength, name length, role enum).
- Login returns the **same error** for wrong password and unknown email, with a dummy hash check to equalize timing.
- JWT carries user id, org id, role and expiry; every request re-loads the user, so deactivated users are blocked.
- **Data isolation (NFR3)**: staff are always created in the admin's `org_id`; queries filter by `org_id`.
- Role checks via the reusable `require_roles(...)` dependency.

## Project layout
```
app/
  config.py      settings from environment
  database.py    engine + session
  models.py      Organization, User tables (SRS ERD)
  schemas.py     request/response validation
  security.py    bcrypt + JWT
  deps.py        get_current_user, require_roles
  routers/       auth.py, users.py
  main.py        app entry point
tests/           pytest suite (14 tests)
```
# ADAPTIVE-AI-LOGISTICS-OPERATIONS-INTELLIGENCE-PLATFORM
