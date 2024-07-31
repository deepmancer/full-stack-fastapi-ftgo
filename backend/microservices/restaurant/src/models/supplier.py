from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ftgo_utils.enums import Gender, Roles
from ftgo_utils.uuid_gen import uuid4

from models.base import Base

class Supplier(Base):
    __tablename__ = "supplier_profile"

    id = Column(String, primary_key=True, default=lambda: uuid4())
    owner_user_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    address = Column(String, nullable=False)
    address_lat = Column(Float, nullable=False)
    address_lng = Column(Float, nullable=False)
    restaurant_licence_id = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    menu = relationship("MenuItem", back_populates="supplier", cascade="all, delete-orphan")

