"""Request/response models with input validation (Pydantic)."""
import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models import OrgType, Role


def _check_password(v: str) -> str:
    if len(v) < 8:
        raise ValueError("Password must be at least 8 characters")
    if len(v.encode("utf-8")) > 72:  # bcrypt only uses the first 72 bytes
        raise ValueError("Password must be at most 72 bytes")
    if not re.search(r"[a-z]", v):
        raise ValueError("Password must contain a lowercase letter")
    if not re.search(r"[A-Z]", v):
        raise ValueError("Password must contain an uppercase letter")
    if not re.search(r"\d", v):
        raise ValueError("Password must contain a digit")
    return v


def _clean_name(v: str) -> str:
    v = " ".join(v.split())
    if len(v) < 2:
        raise ValueError("Must be at least 2 characters")
    return v


class OrganizationRegister(BaseModel):
    org_name: str = Field(max_length=150)
    org_type: OrgType = OrgType.educational_institution
    admin_name: str = Field(max_length=100)
    email: EmailStr
    password: str

    _clean = field_validator("org_name", "admin_name")(_clean_name)

    @field_validator("email")
    @classmethod
    def lower_email(cls, v: str) -> str:
        return v.lower()

    @field_validator("password")
    @classmethod
    def strong_password(cls, v: str) -> str:
        return _check_password(v)


class UserCreate(BaseModel):
    name: str = Field(max_length=100)
    email: EmailStr
    password: str
    role: Role

    _clean = field_validator("name")(_clean_name)

    @field_validator("email")
    @classmethod
    def lower_email(cls, v: str) -> str:
        return v.lower()

    @field_validator("password")
    @classmethod
    def strong_password(cls, v: str) -> str:
        return _check_password(v)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(max_length=200)

    @field_validator("email")
    @classmethod
    def lower_email(cls, v: str) -> str:
        return v.lower()


class OrganizationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    org_id: int
    name: str
    type: OrgType
    created_at: datetime


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    org_id: int
    name: str
    email: EmailStr
    role: Role
    is_active: bool
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class RegisterResponse(BaseModel):
    organization: OrganizationOut
    admin: UserOut
