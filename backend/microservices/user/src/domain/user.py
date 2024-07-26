import asyncio
from typing import Any, Dict, List, Optional

from data_access.repository import CacheRepository, DatabaseRepository
from domain.address import AddressDomain
from domain.authentication import Authenticator
from domain.exceptions import *
from domain import get_logger
from models import Address, Profile, VehicleInfo

import ftgo_utils as utils

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
        self.addresses = None

    @classmethod
    async def load(
        cls,
        user_id: Optional[str] = None,
        phone_number: Optional[str] = None,
        role: Optional[str] = None,
        validate_verified: bool = True,
    ) -> "UserDomain":
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
                raise UserNotFoundError(query_dict)

            user = UserDomain._from_profile(user_profile)
            if validate_verified and not user.is_verified():
                raise UserNotVerifiedError(user_id=user_id)

            return user
        except Exception as e:
            get_logger().error(f"Error loading user with query {query_dict}: {str(e)}")
            raise e

    @staticmethod
    async def register(
        first_name: str,
        last_name: str,
        phone_number: str,
        password: str,
        role: str,
        national_id: Optional[str] = None,
    ):
        try:
            current_records = await DatabaseRepository.fetch_by_query(Profile, query={"phone_number": phone_number, "role": role})
            if current_records:
                raise AccountExistsError(phone_number=phone_number, role=role)

            if role != utils.enums.Roles.CUSTOMER.value and national_id is None:
                raise MissingNationalIDError(role=role)

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
            
            user = UserDomain._from_profile(new_profile)
            auth_code = await user.generate_auth_code()

            get_logger().info(f"User with user_id: {user_id} and phone_number: {phone_number} was created successfully")
    
            return user_id, auth_code
        except Exception as e:
            get_logger().error(f"Error registering user with phone_number {phone_number} and role {role}: {str(e)}")
            raise e

    @staticmethod
    async def verify_account(user_id: str, auth_code: str):
        try:
            profile = await DatabaseRepository.fetch_by_query(Profile, query={"id": user_id}, one_or_none=True)
            if not profile:
                raise UserNotFoundError(dict(user_id=user_id))

            user = UserDomain._from_profile(profile)
            if user.is_verified():
                raise UserAlreadyVerifiedError(user_id=user_id)

            if not Authenticator.verify_auth_code(auth_code):
                raise AuthenticationCodeError(user_id=user_id, auth_code=auth_code)
            
            stored_auth_code = await user._get_auth_code()

            if stored_auth_code and stored_auth_code == auth_code:
                verified_profile = (await DatabaseRepository.update_by_query(
                    Profile, query={"id": user_id}, update_fields={"verified_at": utils.utc_time.now()}
                ))[0]
                user.verified_at = verified_profile.verified_at
                user.updated_at = verified_profile.updated_at
            else:
                raise WrongAuthenticationCodeError(user_id=user_id, auth_code=auth_code, actual_auth_code=stored_auth_code)

            return user_id
        except Exception as e:
            get_logger().error(f"Error authenticating user with id {user_id} and auth code {auth_code}: {str(e)}")
            raise e

    async def resend_auth_code(self):
        try:
            if self.is_verified():
                raise UserAlreadyVerifiedError(user_id=self.user_id)
            auth_code = await self.generate_auth_code()
            return auth_code
        except Exception as e:
            get_logger().error(f"Error resending auth code for user with id {self.user_id}: {str(e)}")
            raise e

    async def login(self, password):
        try:
            if not self.is_verified():
                raise UserNotVerifiedError(user_id=self.user_id)

            if not utils.hash_utils.verify(password, self.hashed_password):
                raise WrongPasswordError(user_id=self.user_id, entered_password=password)

            await DatabaseRepository.update_by_query(Profile, query={"id": self.user_id}, update_fields={"last_login_time": utils.utc_time.now()})
            return
        except Exception as e:
            get_logger().error(f"Error logging in user with id {self.user_id} and role {self.role}: {str(e)}")
            raise e

    async def logout(self):
        try:
            await CacheRepository.delete(self.user_id)
            return
        except Exception as e:
            get_logger().error(f"Error logging out user with id {self.user_id}: {str(e)}")
            raise e

    async def delete_account(self) -> bool:
        try:
            await DatabaseRepository.delete_by_query(Profile, query={"id": self.user_id})
            await CacheRepository.delete(self.user_id)
            return True
        except Exception as e:
            get_logger().error(f"Error deleting account for user with id {self.user_id}: {str(e)}")
            raise e

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
                return {}
    
            updated_profile = await DatabaseRepository.update_by_query(
                Profile, 
                query={"id": self.user_id}, 
                update_fields=new_fields,
            )
            self._update_from_profile(updated_profile[0])
            return self.get_info()
        except Exception as e:
            get_logger().error(f"Error updating profile for user with id {self.user_id}: {str(e)}, update_fields: {update_fields}")
            raise e

    async def update_address_information(self, address_id: str, update_fields: Dict[str, Optional[str]]):
        try:
            address = await self.get_address(address_id)
            if not address:
                raise AddressNotFoundError(address_id=address_id)
            await address.update_address(update_fields)
            return address.get_info()
        except Exception as e:
            get_logger().error(f"Error updating address for user with id {self.user_id} and address_id {address_id}: {str(e)}, update_fields: {update_fields}")
            raise e

    async def get_default_address(self):
        try:
            if not self.addresses:
                await self.load_addresses()
            
            default_address = next((address for address in self.addresses if address.is_default), None)
            return default_address.get_info() if default_address else None
        except Exception as e:
            get_logger().error(f"Error getting default address for user with id {self.user_id}: {str(e)}")
            raise e

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

    async def add_address(self, address_line_1: str, address_line_2: str, city: str, postal_code: str = None, country: str = None) -> str:
        try:
            address =  await AddressDomain.add_address(self.user_id, address_line_1, address_line_2, city, postal_code, country)
            if self.addresses is None:
                self.addresses = [address]
            else:
                self.addresses.append(address)
            
            return address.get_info()
        except Exception as e:
            get_logger().error(f"Error adding address for user with id {self.user_id}: {str(e)}, address_line_1: {address_line_1}, address_line_2: {address_line_2}")
            raise e

    async def get_address_info(self, address_id: str) -> Dict[str, Any]:
        try:
            address = await self.get_address(address_id)
            if not address:
                raise AddressNotFoundError(address_id=address_id)
            
            return address.get_info()
        except Exception as e:
            get_logger().error(f"Error getting address info for user with id {self.user_id} and address_id {address_id}: {str(e)}")
            raise e
    
    async def get_addresses_info(self) -> List[Dict[str, Any]]:
        try:
            if not self.addresses:
                await self.load_addresses()
            
            return [address.get_info() for address in self.addresses]
        except Exception as e:
            get_logger().error(f"Error getting addresses info for user with id {self.user_id}: {str(e)}")
            raise e

    async def get_address(self, address_id: str) -> Optional[AddressDomain]:
        try:
            if not self.addresses:
                await self.load_addresses()
            
            address = next((address for address in self.addresses if address.address_id == address_id), None)
            if not address:
                return None

            return address
        except Exception as e:
            get_logger().error(f"Error getting address for user with id {self.user_id} and address_id {address_id}: {str(e)}")
            raise e

    async def delete_address(self, address_id: str) -> bool:
        try:
            # address = await self.get_address(address_id)
            # if not address:
            #     raise AddressNotFoundError(address_id=address_id)
            #
            # if address.is_default:
            #     raise DefaultAddressDeletionError(address_id=address_id)
            await DatabaseRepository.delete_by_query(Address, query={"id": address_id})
            # await CacheRepository.delete(self.user_id)
            return
            # await AddressDomain.delete_address(address_id)
            # return address_id
        except Exception as e:
            get_logger().error(f"Error deleting address for user with id {self.user_id} and address_id {address_id}: {str(e)}")
            raise e

    async def set_address_as_default(self, address_id: str) -> bool:
        try:
            address = await self.get_address(address_id)

            if not address:
                raise AddressNotFoundError(address_id=address_id)
            if address.is_default:
                return
            
            default_address = next((address for address in self.addresses if address.is_default), None)
            if default_address is not None and default_address.address_id != address_id:
                await default_address.unset_as_default()
            await address.set_as_default(address_id=address_id)
            return address_id
        except Exception as e:
            get_logger().error(f"Error setting address as default for user with id {self.user_id} and address_id {address_id}: {str(e)}")
            raise e

    async def unset_address_as_default(self, address_id: str) -> bool:
        try:
            address = await self.get_address(address_id)

            if not address:
                raise AddressNotFoundError(address_id=address_id)
            if address.is_default:
                return True

            default_address = next((address for address in self.addresses if address.is_default), None)
            if default_address is not None and default_address.address_id != address_id:
                await default_address.unset_as_default()
            await address.set_as_default(address_id=address_id)
            return address_id
        except Exception as e:
            get_logger().error(str(e), user_id=self.user_id, address_id=address_id)
            raise SetDefaultAddressError(user_id=self.user_id, address_id=address_id) from e
      
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "hashed_password": self.hashed_password,
            "nationl_id": self.national_id,
            "gender": self.gender,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "verified_at": self.verified_at,
            "role": self.role,
        }


    def is_verified(self) -> bool:
        return self.verified_at is not None

    async def load_addresses(self) -> List[AddressDomain]:
        if self.addresses is None:
            addresses = await DatabaseRepository.fetch_by_query(Address, query={"user_id": self.user_id})
            self.addresses = [AddressDomain._from_address(address) for address in addresses]
        return self.addresses

    def get_phone_number(self) -> str:
        return self.phone_number

    def get_role(self) -> Optional[str]:
        return self.role

    def _get_secret(self) -> str:
        return f"{self.phone_number}{self.role}"

    async def _get_auth_code(self):
        auth_code = await CacheRepository.get(self.user_id)
        if auth_code and Authenticator.verify_auth_code(auth_code):
            return str(auth_code)
        return None

    async def generate_auth_code(self) -> str:
        auth_code, ttl = Authenticator.create_auth_code(self.user_id)
        await CacheRepository.set(self.user_id, auth_code, ttl)
        return auth_code

    def _update_from_profile(self, profile: Profile):
        updated_user = UserDomain._from_profile(profile)
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
    def _from_profile(profile: Profile):
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
