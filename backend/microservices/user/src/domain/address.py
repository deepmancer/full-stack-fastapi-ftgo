from typing import Optional, List, Dict, Any

from ftgo_utils.time import timezone as tz

from data_access.repository import DatabaseRepository
from models.address import Address

class AddressDomain:
    def __init__(
        self,
        address_id: str,
        user_id: str,
        address_line_1: str,
        address_line_2: Optional[str],
        city: str,
        postal_code: Optional[str],
        country: str,
        is_default: bool,
        created_at: str,
        updated_at: Optional[str],
    ):
        self.address_id = address_id
        self.user_id = user_id
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.postal_code = postal_code
        self.country = country
        self.is_default = is_default
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    async def load(address_id: str) -> "AddressDomain":
        address = await DatabaseRepository.fetch_by_query(Address, query={"id": address_id}, one_or_none=True)
        if not address:
            return None

        return AddressDomain._from_address(address)

    @staticmethod
    async def add_address(
        user_id: str, address_line_1: str, address_line_2: str, city: str, postal_code: str = None, country: str = None,
    ) -> "AddressDomain":
        new_address = Address(
            user_id=user_id,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            postal_code=postal_code,
            country=country,
        )
        new_address = await DatabaseRepository.insert(new_address)
        return AddressDomain._from_address(new_address)

    @staticmethod
    async def delete_address(address_id: str) -> bool:
        await DatabaseRepository.delete_by_query(Address, query={"id": address_id})

    @staticmethod
    def _from_address(address: Address) -> "AddressDomain":
        return AddressDomain(
            address_id=str(address.id),
            user_id=str(address.user_id),
            address_line_1=address.address_line_1,
            address_line_2=address.address_line_2,
            city=address.city,
            postal_code=address.postal_code,
            country=address.country,
            is_default=bool(address.is_default),
            created_at=address.created_at.astimezone(tz) if address.created_at else None,
            updated_at=address.updated_at.astimezone(tz) if address.updated_at else None,
        )

    async def set_as_default(self) -> bool:
        await DatabaseRepository.update_by_query(Address, query={"id": self.address_id}, update_fields={"is_default": True})
        self.is_default = True

    async def unset_as_default(self) -> bool:
        await DatabaseRepository.update_by_query(Address, query={"id": self.address_id}, update_fields={"is_default": False})
        self.is_default = False

    def get_info(self) -> Dict[str, Any]:
        return dict(
            is_default=self.is_default,
            address_line_1=self.address_line_1,
            address_line_2=self.address_line_2,
            city=self.city,
            postal_code=self.postal_code,
            country=self.country,
        )

    def to_dict(self):
        return {
            "address_id": self.address_id,
            "user_id": self.user_id,
            "address_line_1": self.address_line_1,
            "address_line_2": self.address_line_2,
            "city": self.city,
            "postal_code": self.postal_code,
            "country": self.country,
            "is_default": self.is_default,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
