from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, func
from uuid import uuid4
from enum import Enum
from sqlalchemy.orm import relationship, backref
from data_access.models.base import Base
from config.roles import RoleName

class Role(Base):
    __tablename__ = "role"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("user_profile.id"), nullable=False)
    role_name = Column(String, default=RoleName.CUSTOMER.value, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="role")