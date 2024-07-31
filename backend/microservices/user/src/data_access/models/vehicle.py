from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from data_access.models.base import Base
from dto import VehicleDTO

class VehicleInfo(Base):
    __tablename__ = "vehicle_info"

    driver_id: Mapped[str] = mapped_column(String, ForeignKey("user_profile.id"), nullable=False)
    plate_number: Mapped[str] = mapped_column(String, nullable=False)
    license_number: Mapped[str] = mapped_column(String, nullable=False)

    driver: Mapped["Profile"] = relationship("Profile", back_populates="vehicle_info")

    @classmethod
    def from_dto(cls, dto: VehicleDTO) -> 'VehicleInfo':
        return cls(
            id=dto.vehicle_id,
            driver_id=dto.driver_id,
            plate_number=dto.plate_number,
            license_number=dto.license_number,
        )

    def to_dto(self) -> VehicleDTO:
        return VehicleDTO(
            vehicle_id=self.id,
            driver_id=self.driver_id,
            plate_number=self.plate_number,
            license_number=self.license_number,
            created_at=self.created_at,
        )
