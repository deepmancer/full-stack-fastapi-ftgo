from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from uuid import uuid4
from enum import Enum
from sqlalchemy.orm import relationship, backref
from data_access.models.base import Base
from config.roles import RoleName

class Role(Base):
    __tablename__ = "role"

    id = Column(UUIDType(as_uuid=True), primary_key=True, default=uuid4)
    role_name = Column(String, default=RoleName.CUSTOMER.value, nullable=False)
    user_id = Column(UUIDType(as_uuid=True), ForeignKey('user_profile.id'), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="role")