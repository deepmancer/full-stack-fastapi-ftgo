from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from uuid import uuid4
from sqlalchemy.orm import relationship
from data_access.models.base import Base

class UserAddress(Base):
    __tablename__ = "user_address"

    id = Column(UUIDType(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUIDType(as_uuid=True), ForeignKey("user_profile.id"), nullable=False)
    address_line_1 = Column(String, nullable=False)
    address_line_2 = Column(String, nullable=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    country = Column(String, nullable=False)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="addresses")
