from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from uuid import uuid4
from app.data_access.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUIDType(as_uuid=True), primary_key=True, default=uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    email_verified = Column(Boolean, default=False)
    phone_number_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
