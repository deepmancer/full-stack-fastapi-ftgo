from uuid import uuid4
from data_access.models.base import Base
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class DriverLocation(Base):
    __tablename__ = "driver_location"

    id = Column(String, primary_key=True, default=lambda: uuid4().hex)
    driver_id = Column(String, ForeignKey("user_profile.id"), nullable=False)

    latitude = Column(Float(precision=32), nullable=False)
    latitude = Column(Float(precision=32), nullable=False)

    accuracy = Column(Float(precision=32), nullable=True)
    speed = Column(Float(precision=32), nullable=True)
    bearing = Column(Float(precision=32), nullable=True)

    timestamp = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
