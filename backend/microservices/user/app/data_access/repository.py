from typing import Optional, List
from data_access.models.user import User
from data_access.models.address import UserAddress
from data_access.models.role import Role, RoleName
from data_access.session.db import DatabaseDataAccess
from data_access.session.cache import CacheDataAccess
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from configs.db import PostgresConfig
from configs.cache import RedisConfig


class UserRepository:
    _db_da: Optional[DatabaseDataAccess] = None
    _cache_da: Optional[CacheDataAccess] = None

    @classmethod
    def initialize(cls, db_config: PostgresConfig, cache_config: RedisConfig):
        cls._db_da = DatabaseDataAccess(db_config)
        cls._cache_da = CacheDataAccess(cache_config)

    @classmethod
    async def create_user(cls, first_name: str, last_name: str, phone_number: str, password: str, role_name: str) -> User:
        async with cls._db_da.get_or_create_session() as session:
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                hashed_password=password,
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)  # Ensure the new_user instance is updated with the database defaults

            new_role = Role(
                role_name=role_name,
                user_id=new_user.id
            )
            session.add(new_role)
            await session.commit()

            return new_user

    @classmethod
    async def is_phone_number_taken(cls, phone_number: str, role_name: str) -> bool:
        async with cls._db_da.get_or_create_session() as session:
            result = await session.execute(
                select(User).join(Role).filter(User.phone_number == phone_number, Role.role_name == role_name)
            )
            return result.scalars().one_or_none() is not None

    @classmethod
    async def cache_auth_code(cls, user_id: str, auth_code: str):
        session = await cls._cache_da.get_or_create_session()
        await session.delete(user_id)
        await session.set(user_id, auth_code, ex=120)

    @classmethod
    async def get_auth_code_by_user_id(cls, user_id: str) -> Optional[str]:
        session = await cls._cache_da.get_or_create_session()
        auth_code = await session.get(user_id)
        return auth_code

    @classmethod
    async def authenticate_user(cls, user_id: str) -> Optional[User]:
        async with cls._db_da.get_or_create_session() as session:
            result = await session.execute(select(User).filter_by(id=user_id))
            user = result.scalars().one_or_none()
            if user:
                user.is_verified = True
                await session.commit()
                session = await cls._cache_da.get_or_create_session()
                await session.delete(user_id)
                return user
            return None

    @classmethod
    async def get_user_by_id(cls, user_id: str) -> Optional[User]:
        async with cls._db_da.get_or_create_session() as session:
            result = await session.execute(select(User).filter_by(id=user_id))
            user = result.scalars().one_or_none()
            return user

   @classmethod
    async def delete_user(cls, user_id: str):
        async with cls._db_da.get_or_create_session() as session:
            result = await session.execute(select(User).filter_by(id=user_id))
            user = result.scalars().one_or_none()
            if user:
                roles_result = await session.execute(select(Role).filter_by(user_id=user_id))
                roles = roles_result.scalars().all()
                for role in roles:
                    await session.delete(role)
                
                await session.delete(user)
                await session.commit()
                
                session = await cls._cache_da.get_or_create_session()
                await session.delete(user_id)

    @classmethod
    async def add_address(cls, user_id: str, address_line_1: str, address_line_2: str, city: str, state: str, postal_code: str, country: str) -> str:
        async with cls._db_da.get_or_create_session() as session:
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
        async with cls._db_da.get_or_create_session() as session:
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
        async with cls._db_da.get_or_create_session() as session:
            result = await session.execute(select(UserAddress).filter_by(id=address_id))
            address = result.scalars().one_or_none()
            if address:
                await session.delete(address)
                await session.commit()

    @classmethod
    async def set_preferred_address(cls, address_id: str):
        async with cls._db_da.get_or_create_session() as session:
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
        async with cls._db_da.get_or_create_session() as session:
            result = await session.execute(select(UserAddress).filter_by(user_id=user_id))
            addresses = result.scalars().all()
            return addresses

    @classmethod
    async def get_address(cls, address_id: str, user_id: str) -> Optional[UserAddress]:
        async with cls._db_da.get_or_create_session() as session:
            result = await session.execute(select(UserAddress).filter_by(id=address_id, user_id=user_id))
            address = result.scalars().one_or_none()
            return address

    @classmethod
    async def get_role_by_user_id(cls, user_id: str) -> Optional[Role]:
        async with cls._db_da.get_or_create_session() as session:
            result = await session.execute(
                select(Role).filter_by(user_id=user_id)
            )
            return result.scalars().one_or_none()

    @classmethod
    async def delete_role(cls, user_id: str, role_name: str):
        async with cls._db_da.get_or_create_session() as session:
            result = await session.execute(select(Role).filter_by(user_id=user_id, role_name=role_name))
            role = result.scalars().one_or_none()
            if role:
                await session.delete(role)
                await session.commit()
