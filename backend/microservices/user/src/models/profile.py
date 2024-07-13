from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ftgo_utils.enums import Gender, Roles
from ftgo_utils.uuid_gen import uuid4

from models.base import Base

class Profile(Base):
    __tablename__ = "user_profile"

    id = Column(String, primary_key=True, default=lambda: uuid4())
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
    last_login_time = Column(DateTime(timezone=True), nullable=True)

    addresses = relationship("Address", back_populates="profile", cascade="all, delete-orphan")
    vehicle_info = relationship("VehicleInfo", back_populates="driver", cascade="all, delete-orphan")
