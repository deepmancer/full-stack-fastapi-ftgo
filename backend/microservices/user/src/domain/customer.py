from typing import Any, Dict, List, Optional

from ftgo_utils.errors import ErrorCodes, BaseError

from domain import get_logger
from domain.assets import AddressDomain
from domain.user import User
from utils import handle_exception

class Customer(User):
    def __init__(
        self,
        user_id: str,
        role: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        hashed_password: str,
        gender: Optional[str] = None,
        email: Optional[str] = None,
        created_at: Optional[str] = None,
        verified_at: Optional[str] = None,
        last_login_time: Optional[str] = None,
        national_id: Optional[str] = None,
    ):
        super().__init__(
            user_id=user_id,
            role=role,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            hashed_password=hashed_password,
            gender=gender,
            email=email,
            created_at=created_at,
            verified_at=verified_at,
            last_login_time=last_login_time,
            national_id=national_id,
        )
        self.addresses: List[AddressDomain] = []

    async def load_private_attributes(self) -> None:
        try:
            self.addresses = await AddressDomain.load_user_addresses(self.user_id, raise_error_on_missing=False)
        except Exception as e:
            payload = {"user_id": self.user_id}
            get_logger().error(ErrorCodes.BATCH_LOAD_ADDRESS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.BATCH_LOAD_ADDRESS_ERROR, payload=payload)

    def get_addresses_info(self) -> List[Dict[str, Any]]:
        return [address.get_info() for address in self.addresses]

    async def get_address_info(self, address_id: str) -> Optional[Dict[str, Any]]:
        try:
            address = await self.get_address(address_id)
            if address:
                return address.get_info()
            raise BaseError(error_code=ErrorCodes.ADDRESS_NOT_FOUND_ERROR, payload={"address_id": address_id})
        except Exception as e:
            payload = {"user_id": self.user_id, "address_id": address_id}
            get_logger().error(ErrorCodes.GET_ADDRESS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.GET_ADDRESS_ERROR, payload=payload)

    async def get_address(self, address_id: str) -> Optional[AddressDomain]:
        try:
            address = next((addr for addr in self.addresses if addr.address_id == address_id), None)
            if address:
                return address
            return None
        except Exception as e:
            payload = {"user_id": self.user_id, "address_id": address_id}
            get_logger().error(ErrorCodes.ADDRESS_NOT_FOUND_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.ADDRESS_NOT_FOUND_ERROR, payload=payload)

    async def update_address_information(
        self,
        address_id: str,
        update_fields: Dict[str, Optional[str]],
    ) -> Dict[str, Any]:
        try:
            address = await self.get_address(address_id)
            if address:
                await address.update_information(**update_fields)
                self.addresses = await AddressDomain.load_user_addresses(self.user_id)
                return address.get_info()
            else:
                raise BaseError(error_code=ErrorCodes.ADDRESS_NOT_FOUND_ERROR, payload={"address_id": address_id})
        except Exception as e:
            payload = {"user_id": self.user_id, "address_id": address_id, "update_fields": update_fields}
            get_logger().error(ErrorCodes.UPDATE_ADDRESS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.UPDATE_ADDRESS_ERROR, payload=payload)

    async def add_address(
        self, latitude: float, longitude: float, address_line_1: str, address_line_2: str, city: str,
        postal_code: Optional[str] = None, country: Optional[str] = None,
    ) -> Dict[str, Any]:
        try:
            is_default = True if not self.addresses else False
            address = await AddressDomain.create_address(
                user_id=self.user_id,
                latitude=latitude,
                longitude=longitude,
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                city=city,
                is_default=is_default,
                postal_code=postal_code,
                country=country,
            )
            self.addresses.append(address)
            return address.get_info()
        except Exception as e:
            payload = {
                "user_id": self.user_id,
                "address_line_1": address_line_1,
                "address_line_2": address_line_2,
                "city": city,
                "latitude": latitude,
                "longitude": longitude,
            }
            get_logger().error(ErrorCodes.ADD_ADDRESS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.ADD_ADDRESS_ERROR, payload=payload)

    async def get_default_address_info(self) -> Optional[Dict[str, Any]]:
        try:
            default_address = next((address for address in self.addresses if address.is_default), None)
            if not default_address:
                raise BaseError(error_code=ErrorCodes.DEFAULT_ADDRESS_NOT_FOUND_ERROR, payload=dict(user_id=self.user_id))
            return default_address.get_info()
        except Exception as e:
            payload = {"user_id": self.user_id}
            get_logger().error(ErrorCodes.GET_ADDRESS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.GET_ADDRESS_ERROR, payload=payload)

    async def delete_address(self, address_id: str) -> bool:
        try:
            address = await self.get_address(address_id)
            if address:
                await address.delete()
                self.addresses = [addr for addr in self.addresses if addr.address_id != address_id]
                return True
            else:
                raise BaseError(error_code=ErrorCodes.ADDRESS_NOT_FOUND_ERROR, payload={"address_id": address_id})
        except Exception as e:
            payload = {"user_id": self.user_id, "address_id": address_id}
            get_logger().error(ErrorCodes.DELETE_ADDRESS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.DELETE_ADDRESS_ERROR, payload=payload)

    async def set_address_as_default(self, address_id: str) -> Dict[str, Any]:
        try:
            address = await self.get_address(address_id)
            if address and not address.is_default:
                default_address = next((addr for addr in self.addresses if addr.is_default), None)

                if default_address is not None and default_address.address_id != address_id:
                    await default_address.set_preferred_flag(set_default=False)
                await address.set_preferred_flag(set_default=True)
                self.addresses = await AddressDomain.load_user_addresses(self.user_id)
                return address.get_info()
            elif address.is_default:
                return address.get_info()
            else:
                raise BaseError(error_code=ErrorCodes.ADDRESS_NOT_FOUND_ERROR, payload={"address_id": address_id})

        except Exception as e:
            payload = {"user_id": self.user_id, "address_id": address_id}
            get_logger().error(ErrorCodes.DEFAULT_ADDRESS_DELETION_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.DEFAULT_ADDRESS_DELETION_ERROR, payload=payload)
