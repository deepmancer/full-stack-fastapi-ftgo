import asyncio
from typing import Any, Dict, List, Optional

from ftgo_utils.errors import ErrorCodes, BaseError
import ftgo_utils as utils

from data_access.repository import CacheRepository, DatabaseRepository
from domain.address import AddressDomain
from domain.authentication import Authenticator
from domain import get_logger
from models import Address, Profile, VehicleInfo
from utils import handle_exception


class UserDomain:
    def __init__(
        self,
        user_id: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        role: str,
        hashed_password: str,
        gender: Optional[str],
        created_at: str,
        updated_at: Optional[str],
        verified_at: Optional[str],
        national_id: Optional[str] = None,
    ):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.hashed_password = hashed_password
        self.gender = gender
        self.created_at = created_at
        self.updated_at = updated_at
        self.verified_at = verified_at
        self.role = role
        self.national_id = national_id

    @staticmethod
    async def load(
        user_id: Optional[str] = None,
        phone_number: Optional[str] = None,
        role: Optional[str] = None,
        validate_verified: bool = True,
        raise_error_on_missing: bool = True,
        **kwargs,
    ) -> Optional["UserDomain"]:
        query_dict = {}
        if user_id:
            query_dict["id"] = user_id
        if phone_number:
            query_dict["phone_number"] = phone_number
        if role:
            query_dict["role"] = role
        try:
            user_profile = await DatabaseRepository.fetch_by_query(Profile, query=query_dict, one_or_none=True)
            if not user_profile:
                if raise_error_on_missing:
                    raise BaseError(error_code=ErrorCodes.USER_NOT_FOUND_ERROR, payload=query_dict)
                return None

            user = UserDomain._from_schema(user_profile)
            if validate_verified and not user.is_verified():
                raise BaseError(error_code=ErrorCodes.USER_NOT_VERIFIED_ERROR, payload=dict(user_id=user.user_id))

            return user
        except Exception as e:
            payload = dict(query=query_dict)
            get_logger().error(ErrorCodes.USER_LOAD_ACCOUNT_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.USER_LOAD_ACCOUNT_ERROR, payload=payload)

    @staticmethod
    async def register(
        first_name: str,
        last_name: str,
        phone_number: str,
        password: str,
        role: str,
        national_id: Optional[str] = None,
        **kwargs,
    ):
        try:
            current_records = await DatabaseRepository.fetch_by_query(Profile, query={"phone_number": phone_number, "role": role})
            if current_records:
                raise BaseError(error_code=ErrorCodes.ACCOUNT_EXISTS_ERROR, payload=dict(phone_number=phone_number, role=role))

            if role != utils.enums.Roles.CUSTOMER.value and national_id is None:
                raise BaseError(error_code=ErrorCodes.MISSING_NATIONAL_ID_ERROR, payload=dict(role=role))

            user_id = utils.uuid_gen.uuid4()
            hashed_password = utils.hash_utils.hash_value(password)

            new_profile = Profile(
                id=user_id,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                hashed_password=hashed_password,
                role=role,
                national_id=national_id,
            )
            new_profile = await DatabaseRepository.insert(new_profile)

            user = UserDomain._from_schema(new_profile)
            auth_code = await user.generate_auth_code()

            get_logger().info(f"User with user_id: {user_id} and phone_number: {phone_number} was created successfully")
            return user_id, auth_code
        except Exception as e:
            payload = dict(phone_number=phone_number, role=role)
            get_logger().error(ErrorCodes.USER_REGISTRATION_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.USER_REGISTRATION_ERROR, payload=payload)
        
    @staticmethod
    async def verify_account(user_id: str, auth_code: str) -> Optional["UserDomain"]:
        try:
            user = await UserDomain.load(user_id=user_id, validate_verified=False)

            if user.is_verified():
                raise BaseError(error_code=ErrorCodes.USER_ALREADY_VERIFIED_ERROR, payload=dict(user_id=user.user_id))

            if not Authenticator.verify_auth_code(auth_code):
                raise BaseError(error_code=ErrorCodes.INVALID_AUTHENTICATION_CODE_ERROR, payload=dict(user_id=user.user_id, auth_code=auth_code))

            stored_auth_code = await user.fetch_auth_code()

            if stored_auth_code and stored_auth_code == auth_code:
                verified_profile = (await DatabaseRepository.update_by_query(
                    Profile, query={"id": user_id}, update_fields={"verified_at": utils.utc_time.now()}
                ))[0]
                user.verified_at = verified_profile.verified_at
                user.updated_at = verified_profile.updated_at
            else:
                raise BaseError(
                    error_code=ErrorCodes.WRONG_AUTHENTICATION_CODE_ERROR,
                    payload=dict(user_id=user.user_id, auth_code=auth_code, stored_auth_code=stored_auth_code),
                )
            return user
        except Exception as e:
            payload = dict(user_id=user_id, auth_code=auth_code)
            get_logger().error(ErrorCodes.USER_VERIFICATION_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.USER_VERIFICATION_ERROR, payload=payload)

    @staticmethod
    async def resend_auth_code(user_id: str) -> str:
        try:
            user = await UserDomain.load(user_id=user_id, validate_verified=False)
            if user.is_verified():
                raise BaseError(error_code=ErrorCodes.USER_ALREADY_VERIFIED_ERROR, payload=dict(user_id=user_id))
            current_auth_code = await user.fetch_auth_code()
            if current_auth_code and Authenticator.verify_auth_code(current_auth_code):
                get_logger().info("Resending an existing auth code", payload=dict(user_id=user_id, auth_code=current_auth_code))
                return current_auth_code
            auth_code = await user.generate_auth_code()
            return auth_code
        except Exception as e:
            payload = dict(user_id=user_id)
            get_logger().error(ErrorCodes.RESENDING_AUTHENTICATION_CODE_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.RESENDING_AUTHENTICATION_CODE_ERROR, payload=payload)

    @staticmethod
    async def login(
        password: str,
        role: str,
        user_id: Optional[str] = None,
        phone_number: Optional[str] = None,
    ) -> Optional["UserDomain"]:
        try:
            user = await UserDomain.load(phone_number=phone_number, role=role, user_id=user_id)
            if not utils.hash_utils.verify(password, user.hashed_password):
                raise BaseError(
                    error_code=ErrorCodes.WRONG_PASSWORD_ERROR,
                    payload=dict(user_id=user.user_id, password=password),
                )
            user_schema = (await DatabaseRepository.update_by_query(Profile, query={"id": user.user_id}, update_fields={"last_login_time": utils.utc_time.now()}))[0]
            user = UserDomain._from_schema(user_schema)
            return user
        except Exception as e:
            payload = dict(user_id=user_id, phone_number=phone_number, password=password, role=role)
            get_logger().error(ErrorCodes.USER_LOGIN_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.USER_LOGIN_ERROR, payload=payload)

    async def logout(self):
        try:
            await CacheRepository.delete(self.user_id)
        except Exception as e:
            payload = dict(user_id=self.user_id)
            get_logger().error(ErrorCodes.USER_LOGOUT_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.USER_LOGOUT_ERROR, payload=payload)

    async def delete_account(self):
        try:
            await DatabaseRepository.delete_by_query(Profile, query={"id": self.user_id})
            await CacheRepository.delete(self.user_id)
        except Exception as e:
            payload = dict(user_id=self.user_id)
            get_logger().error(ErrorCodes.USER_DELETE_ACCOUNT_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.USER_DELETE_ACCOUNT_ERROR, payload=payload)

    async def update_profile_information(self, update_fields: Dict[str, Optional[str]]):
        try:
            first_name = update_fields.get("first_name")
            last_name = update_fields.get("last_name")
            new_fields = {}
            if first_name:
                new_fields["first_name"] = first_name
            if last_name:
                new_fields["last_name"] = last_name

            if not new_fields:
                return

            updated_profile = await DatabaseRepository.update_by_query(
                Profile,
                query={"id": self.user_id},
                update_fields=new_fields,
            )
            self._update_from_schema(updated_profile[0])
        except Exception as e:
            payload = dict(user_id=self.user_id, update_fields=update_fields)
            get_logger().error(ErrorCodes.USER_PROFILE_UPDATE_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.USER_PROFILE_UPDATE_ERROR, payload=payload)

    async def update_address_information(self, address_id: str, update_fields: Dict[str, Optional[str]]) -> Optional[Dict[str, Any]]:
        try:
            address = await AddressDomain.load(user_id=self.user_id, address_id=address_id)
            await address.update_information(**update_fields)
            return address.get_info()
        except Exception as e:
            payload = {"user_id": self.user_id, "address_id": address_id, "update_fields": update_fields}
            get_logger().error(ErrorCodes.UPDATE_ADDRESS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.UPDATE_ADDRESS_ERROR, payload=payload)

    async def get_default_address(self) -> Optional[Dict[str, Any]]:
        try:
            addresses = await AddressDomain.load_user_addresses(self.user_id)

            default_address = next((address for address in addresses if address.is_default), None)
            if not default_address:
                raise BaseError(error_code=ErrorCodes.DEFAULT_ADDRESS_NOT_FOUND_ERROR, payload=dict(user_id=self.user_id))
            return default_address.get_info()
        except Exception as e:
            payload = {"user_id": self.user_id}
            get_logger().error(ErrorCodes.GET_ADDRESS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.GET_ADDRESS_ERROR, payload=payload)

    def get_info(self) -> Dict[str, Any]:
        info_dict = dict(
            user_id=self.user_id,
            first_name=self.first_name,
            last_name=self.last_name,
            phone_number=self.phone_number,
            hashed_password=self.hashed_password,
            gender=self.gender,
            national_id=self.national_id,
            role=self.role,
        )
        return {key: value for key, value in info_dict.items() if value is not None}

    async def add_address(
        self, latitude: float, longitude: float, address_line_1: str, address_line_2: str, city: str,
        postal_code: Optional[str] = None, country: Optional[str] = None) -> Optional[Dict[str, Any]]:
        try:
            address = await AddressDomain.add_address(
                user_id=self.user_id,
                latitude=latitude,
                longitude=longitude,
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                city=city,
                postal_code=postal_code,
                country=country,
            )
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

    async def get_address_info(self, address_id: str) -> Optional[Dict[str, Any]]:
        try:
            address = await AddressDomain.load(user_id=self.user_id, address_id=address_id)
            return address.get_info()
        except Exception as e:
            payload = {"user_id": self.user_id, "address_id": address_id}
            get_logger().error(ErrorCodes.GET_ADDRESS_INFO_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.GET_ADDRESS_INFO_ERROR, payload=payload)

    async def get_addresses_info(self) -> List[Dict[str, Any]]:
        try:
            addresses = await AddressDomain.load_user_addresses(self.user_id)
            return [address.get_info() for address in addresses]
        except Exception as e:
            payload = {"user_id": self.user_id}
            get_logger().error(ErrorCodes.GET_ADDRESSES_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.GET_ADDRESSES_ERROR, payload=payload)

    async def delete_address(self, address_id: str) -> bool:
        try:
            address = await AddressDomain.load(user_id=self.user_id, address_id=address_id)
            await address.delete()
        except Exception as e:
            payload = {"user_id": self.user_id, "address_id": address_id}
            get_logger().error(ErrorCodes.DELETE_ADDRESS_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.DELETE_ADDRESS_ERROR, payload=payload)

    async def set_address_as_default(self, address_id: str):
        try:
            address = await AddressDomain.load(user_id=self.user_id, address_id=address_id)
            if address.is_default:
                return

            addresses = await AddressDomain.load_user_addresses(self.user_id)
            default_address = next((addr for addr in addresses if addr.is_default), None)

            if default_address is not None and default_address.address_id != address_id:
                await default_address.unset_as_default()
            await address.set_as_default()
            return address.get_info()

        except Exception as e:
            payload = {"user_id": self.user_id, "address_id": address_id}
            get_logger().error(ErrorCodes.DEFAULT_ADDRESS_DELETION_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.DEFAULT_ADDRESS_DELETION_ERROR, payload=payload)

    async def unset_address_as_default(self, address_id: str):
        try:
            address = await AddressDomain.load(user_id=self.user_id, address_id=address_id)

            if not address.is_default:
                return

            await address.unset_as_default()
            return address.get_info()
        except Exception as e:
            payload = {"user_id": self.user_id, "address_id": address_id}
            get_logger().error(ErrorCodes.DEFAULT_ADDRESS_DELETION_ERROR.value, payload=payload)
            await handle_exception(e=e, error_code=ErrorCodes.DEFAULT_ADDRESS_DELETION_ERROR, payload=payload)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "hashed_password": self.hashed_password,
            "national_id": self.national_id,
            "gender": self.gender,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "verified_at": self.verified_at,
            "role": self.role,
        }

    def is_verified(self) -> bool:
        return self.verified_at is not None

    async def fetch_auth_code(self) -> Optional[str]:
        try:
            auth_code = await CacheRepository.get(self.user_id)
            if auth_code and Authenticator.verify_auth_code(auth_code):
                return str(auth_code)
            return None
        except:
            get_logger().warning("Failed to fetch auth code", payload=dict(user_id=self.user_id))
            return None

    async def generate_auth_code(self) -> str:
        auth_code, ttl = Authenticator.create_auth_code(self.user_id)
        await CacheRepository.set(self.user_id, auth_code, ttl)
        return auth_code

    def _update_from_schema(self, profile: Profile):
        updated_user = UserDomain._from_schema(profile)
        if not updated_user:
            return
        self.first_name = updated_user.first_name
        self.last_name = updated_user.last_name
        self.phone_number = updated_user.phone_number
        self.hashed_password = updated_user.hashed_password
        self.national_id = updated_user.national_id
        self.role = updated_user.role
        self.gender = updated_user.gender
        self.updated_at = updated_user.updated_at
        self.verified_at = updated_user.verified_at

    @staticmethod
    def _from_schema(profile: Profile) -> Optional["UserDomain"]:
        if not profile:
            return None

        return UserDomain(
            user_id=str(profile.id),
            first_name=profile.first_name,
            last_name=profile.last_name,
            phone_number=profile.phone_number,
            hashed_password=profile.hashed_password,
            national_id=profile.national_id,
            gender=profile.gender,
            role=profile.role,
            created_at=profile.created_at.astimezone(utils.utc_time.timezone) if profile.created_at else None,
            updated_at=profile.updated_at.astimezone(utils.utc_time.timezone) if profile.updated_at else None,
            verified_at=profile.verified_at.astimezone(utils.utc_time.timezone) if profile.verified_at else None,
        )
