from typing import Optional, List, Dict, Any
from data_access.repository import UserRepository
from data_access.models.user import User
from data_access.models.address import UserAddress
from data_access.models.role import Role
from configs.db import PostgresConfig
from configs.cache import RedisConfig
import uuid

class UserDomain:
    def __init__(
        self,
        user_id: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        phone_number_verified: bool,
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
        self.phone_number_verified = phone_number_verified
        self.hashed_password = hashed_password
        self.gender = gender
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_verified = is_verified
        self.role_name = role_name
        self._addresses = None

    @property
    async def addresses(self) -> List[UserAddress]:
        if self._addresses is None:
            self._addresses = await UserRepository.get_addresses_by_user_id(self.user_id)
        return self._addresses

    @staticmethod
    async def from_user_id(user_id: str) -> "UserDomain":
        user = await UserRepository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        role = await UserRepository.get_role_by_user_id(user_id, user.role.role_name) if user.role else None
        return UserDomain(
            user_id=str(user.id),
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            phone_number_verified=user.phone_number_verified,
            hashed_password=user.hashed_password,
            gender=user.gender,
            email=user.email,
            created_at=str(user.created_at),
            updated_at=str(user.updated_at) if user.updated_at else None,
            is_verified=user.is_verified,
            role_name=role.role_name if role else None
        )

    @staticmethod
    async def register(first_name: str, last_name: str, phone_number: str, password: str, role_name: str) -> str:
        if await UserRepository.is_phone_number_taken(phone_number, role_name):
            raise ValueError("Phone number with this role is already taken")
        
        new_user = await UserRepository.create_user(first_name, last_name, phone_number, password, role_name)
        auth_code = str(uuid.uuid4())[:6]
        await UserRepository.cache_auth_code(str(new_user.id), auth_code)
        return new_user, auth_code

    async def authenticate_phone_number(self, auth_code: str) -> bool:
        stored_code = await UserRepository.get_auth_code_by_user_id(self.user_id)
        if stored_code and stored_code == auth_code:
            await UserRepository.authenticate_user(self.user_id)
            return True
        return False

    async def login(self, password: str) -> str:
        user = await UserRepository.authenticate_user(self.user_id)
        if not user or not user.check_password(password):
            raise ValueError("Invalid credentials")
        return user.generate_jwt()

    async def add_address(self, address_line_1: str, address_line_2: str, city: str, state: str, postal_code: str, country: str) -> str:
        new_address = await UserRepository.add_address(
            self.user_id, address_line_1, address_line_2, city, state, postal_code, country)
        return str(new_address.id)

    async def modify_address(self, address_id: str, address_line_1: str, address_line_2: str, city: str, state: str, postal_code: str, country: str) -> bool:
        address = await UserRepository.update_address(
            address_id, address_line_1, address_line_2, city, state, postal_code, country)
        return address is not None

    async def delete_address(self, address_id: str) -> bool:
        await UserRepository.delete_address(address_id)
        return True

    async def set_preferred_address(self, address_id: str) -> bool:
        await UserRepository.set_preferred_address(address_id)
        return True

    async def delete_account(self) -> bool:
        await UserRepository.delete_user(self.user_id)
        return True

    async def get_role(self) -> Optional[str]:
        role = await UserRepository.get_role_by_user_id(self.user_id, self.role_name)
        return role.role_name if role else None

    async def set_role(self, role_name: str) -> bool:
        await UserRepository.delete_role(self.user_id, self.role_name)
        new_role = await UserRepository.create_role(self.user_id, role_name)
        self.role_name = new_role.role_name
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "phone_number_verified": self.phone_number_verified,
            "hashed_password": self.hashed_password,
            "gender": self.gender,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_verified": self.is_verified,
            "role_name": self.role_name,
        }
