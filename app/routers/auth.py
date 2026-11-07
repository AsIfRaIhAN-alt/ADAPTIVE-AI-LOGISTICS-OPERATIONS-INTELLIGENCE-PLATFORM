"""Organization registration and login."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Organization, Role, User
from app.schemas import LoginRequest, OrganizationRegister, RegisterResponse, TokenResponse
from app.security import DUMMY_HASH, create_access_token, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register-organization", response_model=RegisterResponse, status_code=201)
def register_organization(data: OrganizationRegister, db: Session = Depends(get_db)):
    """FR1: create an organization and its first administrator (UC-01)."""
    if db.scalar(select(Organization).where(func.lower(Organization.name) == data.org_name.lower())):
        raise HTTPException(status.HTTP_409_CONFLICT, "Organization already registered")
    if db.scalar(select(User).where(User.email == data.email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already in use")

    org = Organization(name=data.org_name, type=data.org_type)
    admin = User(
        organization=org,
        name=data.admin_name,
        email=data.email,
        password_hash=hash_password(data.password),
        role=Role.admin,
    )
    db.add_all([org, admin])
    try:
        db.commit()
    except IntegrityError:  # race condition: someone registered the same name/email first
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "Organization or email already registered")
    return RegisterResponse(organization=org, admin=admin)


def _authenticate(db: Session, email: str, password: str) -> User:
    user = db.scalar(select(User).where(User.email == email.lower()))
    # Always run one bcrypt check so timing is similar whether or not the email exists.
    password_ok = verify_password(password, user.password_hash if user else DUMMY_HASH)
    if not user or not password_ok or not user.is_active:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """Login with a JSON body (used by the React frontend)."""
    user = _authenticate(db, data.email, data.password)
    token = create_access_token(user.user_id, user.org_id, user.role.value)
    return TokenResponse(access_token=token, user=user)


@router.post("/token", response_model=TokenResponse)
def token(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Same login but form-encoded; this is what the Swagger 'Authorize' button uses.
    Put your email in the 'username' field."""
    user = _authenticate(db, form.username, form.password)
    access = create_access_token(user.user_id, user.org_id, user.role.value)
    return TokenResponse(access_token=access, user=user)
