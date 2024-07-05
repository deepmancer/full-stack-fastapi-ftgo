from sqlalchemy import Column, String, Boolean, DateTime, func
from uuid import uuid4
from sqlalchemy.orm import relationship
from data_access.models.base import Base


class User(Base):
    __tablename__ = "user_profile"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    gender = Column(String, nullable=True, default="male")
    email = Column(String, unique=True, nullable=True, default=None)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_verified = Column(Boolean, default=False)
    
    addresses = relationship("UserAddress", back_populates="user", cascade="all, delete-orphan")
    role = relationship("Role", uselist=False, back_populates="user")
