"""Profile and admin-only user management (FR2)."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_roles
from app.models import Role, User
from app.schemas import UserCreate, UserOut
from app.security import hash_password

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/me", response_model=UserOut)
def read_me(current: User = Depends(get_current_user)):
    return current


@router.post("", response_model=UserOut, status_code=201)
def create_user(
    data: UserCreate,
    admin: User = Depends(require_roles(Role.admin)),
    db: Session = Depends(get_db),
):
    """Admin creates a staff account. The account is ALWAYS placed in the admin's own organization."""
    if db.scalar(select(User).where(User.email == data.email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already in use")
    user = User(
        org_id=admin.org_id,
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role,
    )
    db.add(user)
    db.commit()
    return user


@router.get("", response_model=list[UserOut])
def list_users(admin: User = Depends(require_roles(Role.admin)), db: Session = Depends(get_db)):
    """Lists only users of the admin's own organization (data isolation, NFR3)."""
    return db.scalars(select(User).where(User.org_id == admin.org_id).order_by(User.user_id)).all()
