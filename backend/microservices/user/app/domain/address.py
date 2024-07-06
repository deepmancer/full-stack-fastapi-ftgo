from typing import Optional, List
from data_access.repository.user import UserRepository
from data_access.models.address import Address
from config.timezone import tz
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
        address = await UserRepository.load_address_by_id(address_id)
        if not address:
            raise "Address not found"

        return AddressDomain._from_address(address)

    @staticmethod
    async def add_address(
        user_id: str, address_line_1: str, address_line_2: str, city: str, postal_code: str = None, country: str = None,
    ) -> "AddressDomain":
        new_address = await UserRepository.add_address(user_id, address_line_1, address_line_2, city, postal_code, country)
        return AddressDomain._from_address(new_address)

    @staticmethod
    async def delete_address(address_id: str) -> bool:
        await UserRepository.delete_address(address_id)

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

    async def modify_fields(self, update_data) -> str:
        new_address = await UserRepository.update_address(self.address_id, update_data)
        for key in update_data.keys():
            value = getattr(new_address, key)
            setattr(self, key, value)

    async def set_as_default(self) -> bool:
        await UserRepository.update_address(self.address_id, {"is_default": True})
        self.is_default = True

    async def unset_as_default(self) -> bool:
        await UserRepository.update_address(self.address_id, {"is_default": False})
        self.is_default = False

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
