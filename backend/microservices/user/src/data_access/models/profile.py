from typing import Optional, List
from sqlalchemy import String, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped

from ftgo_utils.enums import Gender, Roles
from ftgo_utils.utc_time import timezone as tz
from data_access.models.base import Base
from dto import ProfileDTO

class Profile(Base):
    __tablename__ = "user_profile"

    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    national_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    gender: Mapped[str] = mapped_column(String, nullable=True, default=Gender.UNKNOWN.value)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[str] = mapped_column(String, default=Roles.CUSTOMER.value, nullable=False)
    verified_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_login_time: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), nullable=True)

    addresses: Mapped[List["Address"]] = relationship(
        "Address", back_populates="profile", cascade="all, delete-orphan"
    )
    vehicle_info: Mapped[List["VehicleInfo"]] = relationship(
        "VehicleInfo", back_populates="driver", cascade="all, delete-orphan"
    )

    @classmethod
    def from_dto(cls, dto: ProfileDTO) -> 'Profile':
        return cls(
            id=dto.user_id,
            phone_number=dto.phone_number,
            hashed_password=dto.hashed_password,
            national_id=dto.national_id,
            first_name=dto.first_name,
            last_name=dto.last_name,
            gender=dto.gender,
            email=dto.email,
            role=dto.role,
            verified_at=dto.verified_at,
            last_login_time=dto.last_login_time,
        )

    def to_dto(self) -> ProfileDTO:
        return ProfileDTO(
            user_id=self.id,
            phone_number=self.phone_number,
            hashed_password=self.hashed_password,
            national_id=self.national_id,
            first_name=self.first_name,
            last_name=self.last_name,
            gender=self.gender,
            email=self.email,
            role=self.role,
            created_at=self.created_at,
            verified_at=self.verified_at,
            last_login_time=self.last_login_time,
        )
