from uuid import uuid4
from typing import Optional, List, Dict, Any
from loguru import logger
from domain.password import PasswordHandler
from domain.authorization import TokenHandler
from domain.authentication import Authenticator
from data_access.repository.user import UserRepository
from data_access.repository.session import SessionRepository
from data_access.models.profile import Profile
from config.db import PostgresConfig
from config.cache import RedisConfig
from config.auth import AUTH_CODE_TTL_SECONDS
from config.access_token import ACCESS_TOKEN_TTL_SEC
from domain.address import AddressDomain
from domain.uuid_generator import UUIDGenerator
from config.timezone import tz
from utils.exceptions import (
    UserNotFoundError,
    UserNotVerifiedError,
    AccountExistsError,
    InvalidPasswordError,
    AuthenticationCodeError,
    AddressNotFoundError,
    DefaultAddressDeletionError,
)

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
        national_id: Optional[str],
        created_at: str,
        updated_at: Optional[str],
        verified_at: Optional[str],
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

        self.addresses = None

    @staticmethod
    async def load(user_id: str):
        user_profile = await UserRepository.load_user_by_id(user_id)
        if not user_profile:
            raise UserNotFoundError()

        user = UserDomain._from_profile(user_profile)
        if not user.is_verified():
            raise UserNotVerifiedError()

        access_token = await user._get_access_token()
        if not access_token:
            raise UserNotVerifiedError()

        return user

    @staticmethod
    async def register(
        first_name: str,
        last_name: str,
        phone_number: str,
        password: str,
        role: str,
        national_id: Optional[str] = None,
    ) -> str:
        if not (await UserRepository.exists_role_for_phone_number(phone_number, role)):
            raise AccountExistsError()

        user_id = UUIDGenerator.generate()
        hashed_password = PasswordHandler.hash_password(password)
        new_profile = await UserRepository.create_user(
            user_id,
            first_name,
            last_name,
            phone_number,
            hashed_password,
            role,
            national_id,
        )
        user = UserDomain._from_profile(new_profile)
        auth_code = await user._generate_auth_code()
        return user_id, auth_code

    @staticmethod
    async def verify_account(user_id: str, auth_code: str):
        profile = await UserRepository.load_user_by_id(user_id)
        if not profile:
            raise UserNotFoundError()

        user = UserDomain._from_profile(profile)
        if user.is_verified():
            raise UserNotVerifiedError()

        if not Authenticator.verify_auth_code(auth_code):
            raise AuthenticationCodeError()
        
        stored_auth_code = await user._get_auth_code()
        if stored_auth_code and stored_auth_code == auth_code:
            verified_profile = await UserRepository.verify_user(self.user_id)
            self.verified_at = verified_profile.verified_at
            self.updated_at = verified_profile.updated_at
        else:
            raise InvalidAuthenticationCodeError()

        return user_id

    @staticmethod
    async def login(phone_number, password, role):
        profile = await UserRepository.load_user_by_phone_number_and_role(phone_number, role)
        if not profile:
            raise UserNotFoundError()
        user = UserDomain._from_profile(profile)

        if not user.is_verified():
            raise UserNotVerifiedError()

        hashed_password = PasswordHandler.hash_password(password)
        if hashed_password != user.hashed_password:
            raise InvalidPasswordError()

        access_token = await user._get_access_token()

        if access_token:
            return access_token

        access_token = await user._generate_session_token()
        return access_token

    async def delete_account(self) -> bool:
        await UserRepository.delete_user(self.user_id)
        await SessionRepository.delete_user_data(self.user_id)

    def get_info(self) -> Dict[str, Any]:
        return dict(
            first_name=self.first_name,
            last_name=self.last_name,
            phone_number=self.phone_number,
            gender=self.gender,
            role=self.role,
        )

    async def logout(self):
        await SessionRepository.delete_user_token(self.user_id)

    async def add_address(self, address_line_1: str, address_line_2: str, city: str, state: str, postal_code: str = None, country: str = None) -> str:
        address =  await AddressDomain.add_address(self.user_id, address_line_1, address_line_2, city, state, postal_code, country)
        self.addresses.append(address)
        return address.to_dict()

    async def get_address(self, address_id: str) -> Optional[AddressDomain]:
        if not self.addresses:
            await self.load_addresses()
        
        address = next((address for address in self.addresses if address.address_id == address_id), None)
        if not address:
            return None

        return address

    async def delete_address(self, address_id: str) -> bool:
        address = await self.get_address(address_id)
        if not address:
            raise AddressNotFoundError()
        
        if address.is_default:
            raise DefaultAddressDeletionError()
        
        await AddressDomain.delete_address(address_id)
        return address_id

    async def set_preferred_address(self, address_id: str) -> bool:
        address = await self.get_address(address_id)
        if not address:
            raise AddressNotFoundError
        if address.is_default:
            return True
        
        default_address = next((address for address in self.addresses if address.is_default), None)
        await default_address.unset_as_default()
        await address.set_as_default()
        return address_id

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
            addresses = await UserRepository.load_user_addresses(self.user_id)
            self.addresses = [AddressDomain._from_address(address) for address in addresses]
        return self.addresses

    def get_phone_number(self) -> str:
        return self.phone_number

    def get_role(self) -> Optional[str]:
        return self.role

    def _get_secret(self) -> str:
        return f"{self.phone_number}{self.role}"

    async def _get_auth_code(self):
        auth_code = await SessionRepository.get_auth_code_by_user_id(self.user_id)
        if auth_code and Authenticator.verify_auth_code(auth_code):
            return auth_code
        return None

    async def _get_access_token(self):
        access_token = await SessionRepository.get_token_by_user_id(self.user_id)
        if access_token and TokenHandler.validate_token(self.user_id, self._get_secret(), access_token):
            return access_token
        return None

    async def _generate_auth_code(self) -> str:
        auth_code, ttl = Authenticator.create_auth_code(self.user_id)
        await SessionRepository.cache_auth_code(self.user_id, auth_code, ttl=ttl)
        return auth_code

    async def _generate_session_token(self) -> str:
        access_token, ttl = TokenHandler.generate_token(self.user_id, self._get_secret())
        await SessionRepository.cache_token(self.user_id, access_token, ttl=ttl)
        return access_token

    @staticmethod
    def _from_profile(profile: Profile) -> "UserDomain":
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
            created_at=profile.created_at.astimezone(tz) if profile.created_at else None,
            updated_at=profile.updated_at.astimezone(tz) if profile.updated_at else None,
            verified_at=profile.verified_at.astimezone(tz) if profile.verified_at else None,
        )