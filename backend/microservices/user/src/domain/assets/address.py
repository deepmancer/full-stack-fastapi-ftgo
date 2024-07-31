from typing import Any, Dict, List, Optional

from ftgo_utils import uuid_gen
from ftgo_utils.errors import BaseError, ErrorCodes
from ftgo_utils.utc_time import timezone as tz

from data_access.repository import DatabaseRepository
from domain import get_logger
from dto import AddressDTO
from utils import handle_exception


class AddressDomain:
    def __init__(
        self,
        address_id: str,
        user_id: str,
        latitude: float,
        longitude: float,
        address_line_1: str,
        address_line_2: Optional[str],
        city: str,
        postal_code: Optional[str],
        country: str,
        is_default: bool,
        created_at: str,
    ):
        self.address_id = address_id
        self.user_id = user_id
        self.latitude = latitude
        self.longitude = longitude
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.postal_code = postal_code
        self.country = country
        self.is_default = is_default
        self.created_at = created_at

    @staticmethod
    async def load(
        user_id: str,
        address_id: str,
        raise_error_on_missing: bool = True,
    ) -> Optional["AddressDomain"]:
        try:
            address_schema = await DatabaseRepository.fetch(AddressDTO, query={"id": address_id}, one_or_none=True)
            if not address_schema:
                if raise_error_on_missing:
                    raise BaseError(ErrorCodes.ADDRESS_NOT_FOUND_ERROR, payload={"user_id": user_id, "address_id": address_id})
                return None
            
            address = AddressDomain.from_dto(address_schema)
            if address.user_id != user_id:
                raise BaseError(
                    ErrorCodes.ADDRESS_PERMISSION_DENIED_ERROR,
                    payload={"user_id": user_id, "address_id": address_id},
                )
            return address
        except Exception as e:
            payload = {"address_id": address_id, "user_id": user_id}
            get_logger().error(ErrorCodes.LOAD_ADDRESS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.LOAD_ADDRESS_ERROR, payload=payload)

    @staticmethod
    async def load_user_addresses(user_id: str, raise_error_on_missing: bool = True) -> Optional[List["AddressDomain"]]:
        try:
            addresses = await DatabaseRepository.fetch(AddressDTO, query={"user_id": user_id})
            if not addresses:
                if raise_error_on_missing:
                    raise BaseError(ErrorCodes.ADDRESS_NOT_FOUND_ERROR, payload={"user_id": user_id})
                return []
            return [AddressDomain.from_dto(address) for address in addresses]
        except Exception as e:
            payload = {"user_id": user_id}
            get_logger().error(ErrorCodes.BATCH_LOAD_ADDRESS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.BATCH_LOAD_ADDRESS_ERROR, payload=payload)

    @staticmethod
    async def create_address(
        user_id: str, latitude: float, longitude: float, address_line_1: str, address_line_2: Optional[str],
        city: str, postal_code: Optional[str] = None, country: Optional[str] = None, is_default: bool = False,
    ) -> Optional["AddressDomain"]:
        try:
            address_id = uuid_gen.uuid4()
            new_address = AddressDTO(
                address_id=address_id,
                user_id=user_id,
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                city=city,
                latitude=latitude,
                longitude=longitude,
                is_default=is_default,
                postal_code=postal_code,
                country=country,
            )
            new_address = await DatabaseRepository.insert(new_address)
            return AddressDomain.from_dto(new_address)
        except Exception as e:
            payload = {
                "user_id": user_id,
                "address_line_1": address_line_1,
                "address_line_2": address_line_2,
                "city": city,
                "latitude": latitude,
                "longitude": longitude,
            }
            get_logger().error(ErrorCodes.ADD_ADDRESS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.ADD_ADDRESS_ERROR, payload=payload)

    async def delete(self) -> bool:
        try:
            await DatabaseRepository.delete(AddressDTO, query={"id": self.address_id})
            return True
        except Exception as e:
            payload = {"address_id": self.address_id}
            get_logger().error(ErrorCodes.DELETE_ADDRESS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.DELETE_ADDRESS_ERROR, payload=payload)

    async def update_information(
        self,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        address_line_1: Optional[str] = None,
        address_line_2: Optional[str] = None,
        city: Optional[str] = None,
        postal_code: Optional[str] = None,
        country: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        update_fields = {}
        if address_line_1:
            update_fields["address_line_1"] = address_line_1
        if address_line_2:
            update_fields["address_line_2"] = address_line_2
        if city:
            update_fields["city"] = city
        if latitude is not None:
            update_fields["latitude"] = latitude
        if longitude is not None:
            update_fields["longitude"] = longitude
        if postal_code:
            update_fields["postal_code"] = postal_code
        if country:
            update_fields["country"] = country

        try:
            updated_address = await DatabaseRepository.update(AddressDTO, query={"id": self.address_id}, update_fields=update_fields)
            self.update_from_dto(updated_address)
            return self.get_info()
        except Exception as e:
            payload = {
                "user_id": self.user_id,
                "address_id": self.address_id,
                "update_fields": update_fields,
            }
            get_logger().error(ErrorCodes.UPDATE_ADDRESS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.UPDATE_ADDRESS_ERROR, payload=payload)

    async def set_preferred_flag(self, set_default: bool) -> bool:
        try:
            await DatabaseRepository.update(AddressDTO, query={"id": self.address_id}, update_fields={"is_default": set_default})
            self.is_default = set_default
            return True
        except Exception as e:
            payload = {
                "address_id": self.address_id,
                "user_id": self.user_id,
                "is_default": self.is_default,
                "set_default": set_default,
            }
            error_code = ErrorCodes.SET_ADDRESS_AS_DEFAULT_ERROR if set_default else ErrorCodes.UNSET_ADDRESS_AS_DEFAULT_ERROR
            get_logger().error(error_code.value, payload=payload)
            await handle_exception(e=e, error_code=error_code, payload=payload)

    def get_info(self) -> Dict[str, Any]:
        info = {
            "address_id": self.address_id,
            "user_id": self.user_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "is_default": self.is_default,
            "address_line_1": self.address_line_1,
            "address_line_2": self.address_line_2,
            "city": self.city,
            "postal_code": self.postal_code,
            "country": self.country,
        }
        return {k: v for k, v in info.items() if v is not None}

    @staticmethod
    def from_dto(address: AddressDTO) -> "AddressDomain":
        return AddressDomain(
            address_id=str(address.address_id),
            user_id=str(address.user_id),
            latitude=float(address.latitude),
            longitude=float(address.longitude),
            address_line_1=address.address_line_1,
            address_line_2=address.address_line_2,
            city=address.city,
            postal_code=address.postal_code,
            country=address.country,
            is_default=bool(address.is_default),
            created_at=address.created_at.astimezone(tz) if address.created_at else None,
        )

    def update_from_dto(self, address: AddressDTO) -> None:
        self.latitude = address.latitude
        self.longitude = address.longitude
        self.address_line_1 = address.address_line_1
        self.address_line_2 = address.address_line_2
        self.city = address.city
        self.postal_code = address.postal_code
        self.country = address.country
        self.is_default = address.is_default
        self.created_at = address.created_at.astimezone(tz) if address.created_at else None

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, AddressDomain) and self.address_id == other.address_id