"""Database tables. Names follow the ERD in the SRS (Section 7.4).

Every user belongs to exactly one organization (org_id), which is what
enforces data isolation (NFR3).
"""
import enum
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Role(str, enum.Enum):
    admin = "admin"                      # System Administrator
    manager = "manager"                  # Administrator / Manager
    store_officer = "store_officer"      # Procurement / Store Officer
    finance = "finance"                  # Finance / Accounts Staff
    department_head = "department_head"  # added after elicitation (FR2)


class OrgType(str, enum.Enum):
    educational_institution = "educational_institution"  # initial release only


class Organization(Base):
    __tablename__ = "organizations"

    org_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    type: Mapped[OrgType] = mapped_column(
        Enum(OrgType, native_enum=False, length=40), default=OrgType.educational_institution
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    users: Mapped[list["User"]] = relationship(back_populates="organization")


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.org_id"), index=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))  # bcrypt hash, never the password
    role: Mapped[Role] = mapped_column(Enum(Role, native_enum=False, length=30))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    organization: Mapped[Organization] = relationship(back_populates="users")
