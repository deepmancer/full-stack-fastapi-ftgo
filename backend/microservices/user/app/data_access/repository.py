from typing import Optional, List
from data_access.models.user import User
from data_access.models.address import UserAddress
from data_access.models.role import Role, RoleName
from data_access.session.db import DatabaseDataAccess
from data_access.session.cache import CacheDataAccess
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from config.db import PostgresConfig
from config.cache import RedisConfig


class UserRepository:
    database_da: Optional[DatabaseDataAccess] = None
    cache_da: Optional[CacheDataAccess] = None

    @classmethod
    def initialize(cls, db_config: PostgresConfig, cache_config: RedisConfig):
        cls.database_da = DatabaseDataAccess(db_config)
        cls.cache_da = CacheDataAccess(cache_config)

    @classmethod
    def get_authentication_key(cls, key: str) -> str:
        return f"auth_{key}"

    @classmethod
    def get_token_key(cls, key) -> str:
        return f"token_{key}"

    @classmethod
    async def create_user(cls, first_name: str, last_name: str, phone_number: str, password: str, role_name: str) -> User:
        async with cls.database_da.get_or_create_session() as session:
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                hashed_password=password,
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            new_role = Role(
                role_name=role_name,
                user_id=new_user.id
            )
            session.add(new_role)
            await session.commit()

            return new_user

    @classmethod
    async def is_phone_number_taken(cls, phone_number: str, role_name: str) -> bool:
        async with cls.database_da.get_or_create_session() as session:
            result = await session.execute(
                select(User).join(Role).filter(User.phone_number == phone_number, Role.role_name == role_name)
            )
            return result.scalars().one_or_none() is not None

    @classmethod
    async def cache_auth_code(cls, user_id: str, auth_code: str, ttl: int):
        key = cls.get_authentication_key(user_id)
        await cls.cache_da.set(key, auth_code, ttl)

    @classmethod
    async def cache_token(cls, user_id: str, token: str, ttl: int):
        key = cls.get_token_key(user_id)
        await cls.cache_da.set(key, token, ttl)

    @classmethod
    async def get_auth_code_by_user_id(cls, user_id: str) -> Optional[str]:
        key = cls.get_authentication_key(user_id)
        auth_code = await cls.cache_da.get(key)
        return auth_code

    @classmethod
    async def get_token_by_user_id(cls, user_id: str) -> Optional[str]:
        key = cls.get_token_key(user_id)
        token = await cls.cache_da.get(key)
        return token

    @classmethod
    async def delete_user_auth_code(cls, user_id: str):
        key = cls.get_authentication_key(user_id)
        await cls.cache_da.delete(key)

    @classmethod
    async def delete_user_token(cls, user_id: str):
        key = cls.get_token_key(user_id)
        await cls.cache_da.delete(key)

    @classmethod
    async def flush_user_cached_data(cls, user_id: str):
        auth_key = cls.get_authentication_key(user_id)
        token_key = cls.get_token_key(user_id)
        async with cls.cache_da.pipeline() as pipe:
            pipe.delete(auth_key)
            pipe.delete(token_key)
            await pipe.execute()

    @classmethod
    async def authenticate_user(cls, user_id: str) -> Optional[User]:
        async with cls.database_da.get_or_create_session() as session:
            result = await session.execute(select(User).filter_by(id=user_id))
            user = result.scalars().one_or_none()
            if user:
                user.is_verified = True
                await session.commit()

        await cls.flush_user_cached_data(user_id)
        return user

    @classmethod
    async def get_user_by_id(cls, user_id: str) -> Optional[User]:
        async with cls.database_da.get_or_create_session() as session:
            result = await session.execute(select(User).filter_by(id=user_id))
            user = result.scalars().one_or_none()
            return user

    @classmethod
    async def get_user_by_phone_number_role(cls, phone_number: str, role_name: str) -> Optional[User]:
        async with cls.database_da.get_or_create_session() as session:
            result = await session.execute(
                select(User).join(Role).filter(User.phone_number == phone_number, Role.role_name == role_name)
            )
            user = result.scalars().one_or_none()
            return user

    @classmethod
    async def delete_user(cls, user_id: str):
        async with cls.database_da.get_or_create_session() as session:
            result = await session.execute(select(User).filter_by(id=user_id))
            user = result.scalars().one_or_none()
            if user:
                roles_result = await session.execute(select(Role).filter_by(user_id=user_id))
                roles = roles_result.scalars().all()
                for role in roles:
                    await session.delete(role)
                
                await session.delete(user)
                await session.commit()
        await cls.flush_user_cached_data(user_id)

    @classmethod
    async def add_address(cls, user_id: str, address_line_1: str, address_line_2: str, city: str, state: str, postal_code: str, country: str) -> str:
        async with cls.database_da.get_or_create_session() as session:
            new_address = UserAddress(
                user_id=user_id,
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                city=city,
                state=state,
                postal_code=postal_code,
                country=country,
            )
            session.add(new_address)
            await session.commit()
            return str(new_address.id)

    @classmethod
    async def update_address(cls, address_id: str, address_line_1: str, address_line_2: str, city: str, state: str, postal_code: str, country: str):
        async with cls.database_da.get_or_create_session() as session:
            result = await session.execute(select(UserAddress).filter_by(id=address_id))
            address = result.scalars().one_or_none()
            if address:
                address.address_line_1 = address_line_1
                address.address_line_2 = address_line_2
                address.city = city
                address.state = state
                address.postal_code = postal_code
                address.country = country
                await session.commit()

    @classmethod
    async def delete_address(cls, address_id: str):
        async with cls.database_da.get_or_create_session() as session:
            result = await session.execute(select(UserAddress).filter_by(id=address_id))
            address = result.scalars().one_or_none()
            if address:
                await session.delete(address)
                await session.commit()

    @classmethod
    async def set_preferred_address(cls, address_id: str):
        async with cls.database_da.get_or_create_session() as session:
            result = await session.execute(select(UserAddress).filter_by(id=address_id))
            address = result.scalars().one_or_none()
            if address:
                user_id = address.user_id
                result = await session.execute(select(UserAddress).filter_by(user_id=user_id))
                addresses = result.scalars().all()
                for addr in addresses:
                    addr.is_default = False
                address.is_default = True
                await session.commit()

    @classmethod
    async def get_addresses_by_user_id(cls, user_id: str) -> List[UserAddress]:
        async with cls.database_da.get_or_create_session() as session:
            result = await session.execute(select(UserAddress).filter_by(user_id=user_id))
            addresses = result.scalars().all()
            return addresses

    @classmethod
    async def get_address(cls, address_id: str, user_id: str) -> Optional[UserAddress]:
        async with cls.database_da.get_or_create_session() as session:
            result = await session.execute(select(UserAddress).filter_by(id=address_id, user_id=user_id))
            address = result.scalars().one_or_none()
            return address

    @classmethod
    async def get_role_by_user_id(cls, user_id: str) -> Optional[Role]:
        async with cls.database_da.get_or_create_session() as session:
            result = await session.execute(
                select(Role).filter_by(user_id=user_id)
            )
            return result.scalars().one_or_none()

    @classmethod
    async def delete_role(cls, user_id: str, role_name: str):
        async with cls.database_da.get_or_create_session() as session:
            result = await session.execute(select(Role).filter_by(user_id=user_id, role_name=role_name))
            role = result.scalars().one_or_none()
            if role:
                await session.delete(role)
                await session.commit()
