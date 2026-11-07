# ADAPTIVE-AI-LOGISTICS-OPERATIONS-INTELLIGENCE-PLATFORM
For our SE331 capstone project (Team ACE). The system will help schools
and universities decide what to buy, how much, and when to buy or take random decisions. Right now only the
login part is finished: organizations can register, users can log in, and
different roles get different permissions.

## What works so far
- Register an organization (it gets its first admin account).
- Log in with email and password.
- The admin can create staff accounts (manager, store officer, finance, department head).
- Every user only sees data from their own organization.

## How to run it (Windows)
1. To run it at first we Open the backend folder in VS Code and open a terminal.
2. To Create the environment: `python -m venv .venv`
3. To Install the packages: `.venv\Scripts\python.exe -m pip install -r requirements.txt`
4. To Copy the settings file: `copy .env.example .env`
5. To Make a secret key with
   `.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(48))"`
   and paste it after `SECRET_KEY=` in `.env`
6. To Start the server: `.venv\Scripts\python.exe -m uvicorn app.main:app --reload`
7. To Open the server http://localhost:8000/docs to try the API

To run the tests: `.venv\Scripts\python.exe -m pytest -q`

## Endpoints
| Method | Path | Who can use it |
|---|---|---|
| POST | /api/auth/register-organization | anyone |
| POST | /api/auth/login | anyone |
| GET | /api/users/me | any logged-in user |
| POST | /api/users | admin only |
| GET | /api/users | admin only |

## How it is built
- We saved the passwords in bcrypt hashes, never as plain text.
- The secret key is only in `.env`, the key is not included in code, and `.env` is not uploaded to GitHub.
- Every inputs are checked throughly (valid email, strong password, allowed roles).
- A log in attempt with wrong username or password will error.
- To protect the confidentiality and integrity one organization cant see the data of another organization.

## Team
- Md Asif Raihan (241-35-340): backend API, database, authentication, budget module.
- Md Abu Musha Rony (241-35-273): AI models and evaluation.
- Md Mostahid Islam Riad (241-35-398): frontend, testing, documentation.