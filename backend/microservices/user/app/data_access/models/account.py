from uuid import uuid4
from data_access.models.base import Base
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.timezone import tz

class Account(Base):
    __tablename__ = "user_account"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    phone_number = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    national_id = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    gender = Column(String, nullable=True, default="male")

    created_at = Column(DateTime(timezone=True), server_default=func.now().astimezone(tz))
    updated_at = Column(DateTime(timezone=True), server_default=func.now().astimezone(tz), onupdate=func.now().astimezone(tz))
    verified_at = Column(DateTime(timezone=True), nullable=True)

    addresses = relationship("Address", back_populates="account", cascade="all, delete-orphan")
    role = relationship("Role", uselist=False, back_populates="account")
