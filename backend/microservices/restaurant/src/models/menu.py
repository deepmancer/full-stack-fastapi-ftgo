from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, func, Float, Integer
from sqlalchemy.orm import relationship

from ftgo_utils.uuid_gen import uuid4

from models.base import Base

class MenuItem(Base):
    __tablename__ = "menu_item"

    item_id = Column(String, primary_key=True, default=lambda: uuid4())
    restaurant_id = Column(String, ForeignKey("supplier_profile.id"), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False, default=0)
    description = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    supplier = relationship("Supplier", back_populates="menu")
