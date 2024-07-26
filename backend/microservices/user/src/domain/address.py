from audioop import add
from typing import Optional, List, Dict, Any

from ftgo_utils.errors import BaseError, ErrorCodes
from ftgo_utils.utc_time import timezone as tz

from backend.gateway.src.services import user
from domain import get_logger
from data_access.repository import DatabaseRepository
from models.address import Address
from utils.exception import handle_exception


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
        updated_at: Optional[str],
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
        self.updated_at = updated_at

    @staticmethod
    async def load(
        user_id: str,
        address_id: str,
        raise_error_on_missing: bool = True,
    ) -> Optional["AddressDomain"]:
        try:
            address_schema = await DatabaseRepository.fetch_by_query(Address, query={"id": address_id}, one_or_none=True)
            if not address_schema:
                if raise_error_on_missing:
                    raise BaseError(ErrorCodes.ADDRESS_NOT_FOUND_ERROR, payload={"user_id": user_id, "address_id": address_id})
                return None
            
            address = AddressDomain._from_schema(address_schema)
            if address.user_id != user_id:
                raise BaseError(
                    ErrorCodes.ADDRESS_PERMISSION_DENIED_ERROR,
                    payload={"user_id": user_id, "address_id": address_id},
                )
            return address
        except Exception as e:
            payload = {"address_id": address_id}
            get_logger().error(ErrorCodes.LOAD_ADDRESS_ERROR, payload=payload)
            handle_exception(e=e, error_code=ErrorCodes.LOAD_ADDRESS_ERROR, payload=payload)

    @staticmethod
    async def load_user_addresses(user_id: str, raise_error_on_missing: bool = True) -> Optional[List["AddressDomain"]]:
        try:
            addresses = await DatabaseRepository.fetch_by_query(Address, query={"user_id": user_id})
            if not addresses:
                if raise_error_on_missing:
                    raise BaseError(ErrorCodes.ADDRESS_NOT_FOUND_ERROR, payload={"user_id": user_id})
                return None
            return [AddressDomain._from_schema(address) for address in addresses]
        except Exception as e:
            payload = {"user_id": user_id}
            get_logger().error(ErrorCodes.BATCH_LOAD_ADDRESS_ERROR, payload=payload)
            handle_exception(e=e, error_code=ErrorCodes.BATCH_LOAD_ADDRESS_ERROR, payload=payload)

    @staticmethod
    async def add_address(
        user_id: str, latitude: float, longitude: float, address_line_1: str, address_line_2: str,
        city: str, postal_code: Optional[str] = None, country: Optional[str] = None,
    ) -> Optional["AddressDomain"]:
        try:
            new_address = Address(
                user_id=user_id,
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                city=city,
                latitude=latitude,
                longitude=longitude,
                postal_code=postal_code,
                country=country,
            )
            new_address = await DatabaseRepository.insert(new_address)
            return AddressDomain._from_schema(new_address)
        except Exception as e:
            payload = {
                "user_id": user_id,
                "address_line_1": address_line_1,
                "address_line_2": address_line_2,
                "city": city,
                "latitude": latitude,
                "longitude": longitude,
            }
            get_logger().error(ErrorCodes.ADD_ADDRESS_ERROR, payload=payload)
            handle_exception(e=e, error_code=ErrorCodes.ADD_ADDRESS_ERROR, payload=payload)

    async def delete(self) -> bool:
        try:
            await DatabaseRepository.delete_by_query(Address, query={"id": self.address_id})
            return True
        except Exception as e:
            payload = {"address_id": self.address_id}
            get_logger().error(ErrorCodes.DELETE_ADDRESS_ERROR, payload=payload)
            handle_exception(e=e, error_code=ErrorCodes.DELETE_ADDRESS_ERROR, payload=payload)

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
            updated_address = await DatabaseRepository.update_by_query(Address, query={"id": self.address_id}, update_fields=update_fields)
            self._update_from_schema(updated_address)
            return update_fields
        except Exception as e:
            payload = {
                "user_id": self.user_id,
                "address_id": self.address_id,
                "update_fields": update_fields,
            }
            get_logger().error(ErrorCodes.UPDATE_ADDRESS_ERROR, payload=payload)
            handle_exception(e=e, error_code=ErrorCodes.UPDATE_ADDRESS_ERROR, payload=payload)

    async def set_as_default(self) -> bool:
        try:
            await DatabaseRepository.update_by_query(Address, query={"id": self.address_id}, update_fields={"is_default": True})
            self.is_default = True
            return True
        except Exception as e:
            payload = {
                "address_id": self.address_id,
                "user_id": self.user_id,
                "is_default": self.is_default,
            }
            get_logger().error(ErrorCodes.SET_ADDRESS_AS_DEFAULT_ERROR, payload=payload)
            handle_exception(e=e, error_code=ErrorCodes.SET_ADDRESS_AS_DEFAULT_ERROR, payload=payload)

    async def unset_as_default(self) -> bool:
        try:
            await DatabaseRepository.update_by_query(Address, query={"id": self.address_id}, update_fields={"is_default": False})
            self.is_default = False
            return True
        except Exception as e:
            payload = {
                "address_id": self.address_id,
                "user_id": self.user_id,
                "is_default": self.is_default,
            }
            get_logger().error(ErrorCodes.UNSET_ADDRESS_AS_DEFAULT_ERROR, payload=payload)
            handle_exception(e=e, error_code=ErrorCodes.UNSET_ADDRESS_AS_DEFAULT_ERROR, payload=payload)

    def get_info(self) -> Dict[str, Any]:
        return {
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

    @staticmethod
    def _from_schema(address: Address) -> "AddressDomain":
        return AddressDomain(
            address_id=str(address.id),
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
            updated_at=address.updated_at.astimezone(tz) if address.updated_at else None,
        )

    def _update_from_schema(self, address: Address):
        address_domain = AddressDomain._from_schema(address)
        if not address_domain:
            return

        self.latitude = address_domain.latitude
        self.longitude = address_domain.longitude
        self.address_line_1 = address_domain.address_line_1
        self.address_line_2 = address_domain.address_line_2
        self.city = address_domain.city
        self.postal_code = address_domain.postal_code
        self.country = address_domain.country
        self.is_default = address_domain.is_default
