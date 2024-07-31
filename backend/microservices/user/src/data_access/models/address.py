from typing import Optional
from sqlalchemy import Float, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, mapped_column, Mapped

from data_access.models.base import Base
from dto import AddressDTO

class Address(Base):
    __tablename__ = "customer_address"

    user_id: Mapped[str] = mapped_column(String, ForeignKey("user_profile.id"), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    address_line_1: Mapped[str] = mapped_column(Text, nullable=False)
    address_line_2: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(Text, nullable=False)
    postal_code: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    country: Mapped[str] = mapped_column(Text, nullable=True, default="IR")
    is_default: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=False)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="addresses")

    @classmethod
    def from_dto(cls, dto: AddressDTO) -> 'Address':
        return cls(
            id=dto.address_id,
            user_id=dto.user_id,
            latitude=dto.latitude,
            longitude=dto.longitude,
            address_line_1=dto.address_line_1,
            address_line_2=dto.address_line_2,
            city=dto.city,
            postal_code=dto.postal_code,
            country=dto.country,
            is_default=dto.is_default,
        )

    def to_dto(self) -> AddressDTO:
        return AddressDTO(
            address_id=self.id,
            user_id=self.user_id,
            latitude=self.latitude,
            longitude=self.longitude,
            address_line_1=self.address_line_1,
            address_line_2=self.address_line_2,
            city=self.city,
            postal_code=self.postal_code,
            country=self.country,
            is_default=self.is_default,
            created_at=self.created_at,
        )
