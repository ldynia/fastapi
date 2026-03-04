from datetime import datetime, timezone
import uuid

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True, index=True)
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), nullable=False, unique=True, index=True)
    first_name: str
    last_name: str
    email: str
    password: str
    is_active: bool = True
    is_admin: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
