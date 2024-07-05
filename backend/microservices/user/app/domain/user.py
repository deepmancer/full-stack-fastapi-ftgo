from typing import Optional, List, Dict, Any
from loguru import logger
from domain.password import PasswordHandler
from domain.authorization import TokenHandler
from domain.authentication import Authenticator
from data_access.repository import UserRepository
from data_access.models.user import User
from data_access.models.address import UserAddress
from data_access.models.role import Role
from config.db import PostgresConfig
from config.cache import RedisConfig
from config.auth import AUTH_CODE_TTL_SECONDS
from config.access_token import ACCESS_TOKEN_TTL_SEC


class UserDomain:
    def __init__(
        self,
        user_id: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        hashed_password: str,
        gender: Optional[str],
        email: Optional[str],
        created_at: str,
        updated_at: Optional[str],
        is_verified: bool,
        role_name: Optional[str] = None,
    ):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.hashed_password = hashed_password
        self.gender = gender
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_verified = is_verified

        self.role_name = role_name
        self._addresses = None

    async def load_addresses(self) -> List[UserAddress]:
        if self._addresses is None:
            self._addresses = await UserRepository.get_addresses_by_user_id(self.user_id)
        return self._addresses

    @staticmethod
    async def from_user_id(user_id: str) -> "UserDomain":
        user = await UserRepository.get_user_by_id(user_id)
        if not user:
            raise "User not found"

        if not user.is_verified:
            return UserDomain._from_user(user)

        access_token = await UserRepository.get_token_by_user_id(user_id)
        is_access_token_valid = TokenHandler.validate_token(user_id, user.hashed_password, access_token)

        if not is_access_token_valid:
            raise "Access token is invalid"

        return UserDomain._from_user(user)

    @staticmethod
    async def from_phone_number_role(phone_number: str, role_name: str) -> "UserDomain":
        user = await UserRepository.get_user_by_phone_number_role(phone_number, role_name)
        if not user:
            raise "User not found"
        
        return await UserDomain.from_user_id(user.id)

    @staticmethod
    def _from_user(user: User) -> "UserDomain":
        return UserDomain(
            user_id=str(user.id),
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            hashed_password=user.hashed_password,
            gender=user.gender,
            email=user.email,
            created_at=str(user.created_at),
            updated_at=str(user.updated_at) if user.updated_at else None,
            is_verified=user.is_verified,
            role_name= user.role_name,
        )

    @staticmethod
    async def register(first_name: str, last_name: str, phone_number: str, password: str, role_name: str) -> str:
        if await UserRepository.is_phone_number_taken(phone_number, role_name):
            raise ValueError("Phone number with this role is already taken")
        
        hashed_password = PasswordHandler.hash_password(password)
        new_user = await UserRepository.create_user(first_name, last_name, phone_number, hashed_password, role_name)
        auth_code, ttl = Authenticator.create_auth_code(str(new_user.id))
        await UserRepository.cache_auth_code(new_user.id, auth_code, ttl=ttl)
        return new_user.id, auth_code

    async def authenticate(self, auth_code: str) -> bool:
        if self.is_verified:
            raise "User is already verified"

        if not Authenticator.verify_auth_code(auth_code):
            raise "Invalid authentication code"
        
        stored_auth_code = await UserRepository.get_auth_code_by_user_id(self.user_id)
        if stored_auth_code and stored_auth_code == auth_code:
            user = await UserRepository.authenticate_user(self.user_id)
            self.is_verified = user.is_verified
            self.updated_at = user.updated_at
        else:
            raise "Authentication code does not match"
        
        access_token, ttl = await self.login()
        return access_token, ttl

    async def login(self) -> str:
        if not self.is_verified:
            raise "User is not verified"

        access_token = await UserRepository.get_token_by_user_id(self.user_id)
        if access_token and TokenHandler.validate_token(self.user_id, self.hashed_password, access_token):
            return access_token, TokenHandler.get_token_ttl(access_token)

        access_token, ttl = TokenHandler.generate_token(self.user_id, self.hashed_password)
        await UserRepository.cache_token(self.user_id, access_token, ttl=ttl)

        return access_token, ttl

    async def add_address(self, address_line_1: str, address_line_2: str, city: str, state: str, postal_code: str, country: str) -> str:
        new_address = await UserRepository.add_address(
            self.user_id, address_line_1, address_line_2, city, state, postal_code, country)
        return str(new_address.id)

    async def delete_address(self, address_id: str) -> bool:
        await UserRepository.delete_address(address_id)
        return True

    async def set_preferred_address(self, address_id: str) -> bool:
        await UserRepository.set_preferred_address(address_id)
        return True

    
    async def delete_account(self) -> bool:
        await UserRepository.delete_user(self.user_id)
        return True

    async def refresh(self):
        user = await UserRepository.get_user_by_id(self.user_id)
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.phone_number = user.phone_number
        self.hashed_password = user.hashed_password
        
        self._addresses = await UserRepository.get_addresses_by_user_id(self.user_id)
        
        role = await UserRepository.get_role_by_user_id(self.user_id)
        self.role_name = role.role_name if role else None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "hashed_password": self.hashed_password,
            "gender": self.gender,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_verified": self.is_verified,
            "role_name": self.role_name,
        }
