from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, func
from uuid import uuid4
from enum import Enum
from sqlalchemy.orm import relationship, backref
from data_access.models.base import Base
from config.enums import RoleName
from config.timezone import tz

class Role(Base):
    __tablename__ = "user_role"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("user_account.id"), nullable=False)
    role_name = Column(String, default=RoleName.CUSTOMER.value, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now().astimezone(tz))
    updated_at = Column(DateTime(timezone=True), server_default=func.now().astimezone(tz), onupdate=func.now().astimezone(tz))

    account = relationship("Account", back_populates="role")
