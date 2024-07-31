from typing import Optional
from datetime import datetime
from sqlalchemy import String, DateTime, Float
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql import func

from data_access.models.base import Base
from dto import DriverLocationDTO
from ftgo_utils.uuid_gen import uuid4

class DriverLocation(Base):
    __tablename__ = "driver_location"

    driver_id: Mapped[str] = mapped_column(String, nullable=False)

    latitude: Mapped[float] = mapped_column(Float(precision=32), nullable=False)
    longitude: Mapped[float] = mapped_column(Float(precision=32), nullable=False)

    accuracy: Mapped[Optional[float]] = mapped_column(Float(precision=32), nullable=True)
    speed: Mapped[Optional[float]] = mapped_column(Float(precision=32), nullable=True)
    bearing: Mapped[Optional[float]] = mapped_column(Float(precision=32), nullable=True)

    timestamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)

    @classmethod
    def from_dto(cls, dto: 'DriverLocationDTO') -> 'DriverLocation':
        return cls(
            id=dto.location_id,
            driver_id=dto.driver_id,
            latitude=dto.latitude,
            longitude=dto.longitude,
            accuracy=dto.accuracy,
            speed=dto.speed,
            bearing=dto.bearing,
            timestamp=dto.timestamp if isinstance(dto.timestamp, datetime) else datetime.fromtimestamp(dto.timestamp),
        )

    def to_dto(self) -> 'DriverLocationDTO':
        return DriverLocationDTO(
            location_id=self.id,
            driver_id=self.driver_id,
            latitude=self.latitude,
            longitude=self.longitude,
            accuracy=self.accuracy,
            speed=self.speed,
            bearing=self.bearing,
            timestamp=self.timestamp,
            created_at=self.created_at,
        )
