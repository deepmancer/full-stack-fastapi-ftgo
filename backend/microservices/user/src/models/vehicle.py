from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from ftgo_utils.uuid import uuid4

from models.base import Base

class VehicleInfo(Base):
    __tablename__ = "vehicle_info"

    id = Column(String, primary_key=True, default=lambda: uuid4())
    driver_id = Column(String, ForeignKey("user_profile.id"), nullable=False)
    plate_number = Column(String, nullable=False)
    license_number = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    driver = relationship("Profile", back_populates="vehicle_info")
