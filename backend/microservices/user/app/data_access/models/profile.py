from uuid import uuid4
from data_access.models.base import Base
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.timezone import tz
from config.enums import Gender, Roles

class Profile(Base):
    __tablename__ = "user_profile"

    id = Column(String, primary_key=True, default=lambda: str(uuid4().hex()))
    phone_number = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    national_id = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    gender = Column(String, nullable=True, default=Gender.UNKNOWN.value)
    role = Column(String, default=Roles.CUSTOMER.value, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    verified_at = Column(DateTime(timezone=True), nullable=True)

    addresses = relationship("Address", back_populates="profile", cascade="all, delete-orphan")
