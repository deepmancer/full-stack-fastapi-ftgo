from data_access.models.user_profile import User
from data_access.models.address import UserAddress
from data_access.session.interface import AsyncSessionInterface
from data_access.session.db import DatabaseSession
from data_access.session.cache import CacheSession
from typing import Type
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from uuid import UUID
from sqlalchemy.exc import NoResultFound
import asyncio

class UserRepository:
    def __init__(self, db_da: DatabaseSession, cache_da: CacheSession):
        self.db_da = db_da
        self.cache_da = cache_da    

    async def create_user(self, first_name: str, last_name: str, phone_number: str, password: str) -> str:
        async with self.db_da.get_or_create_session() as session:
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                hashed_password=password,
            )
            session.add(new_user)
            await session.commit()
            return str(new_user.id)
        
    async def get_user_id_by_phone_number(self, phone_number: str) -> str:
        async with self.db_da.get_or_create_session() as session:
            result = await session.execute(select(User).filter_by(phone_number=phone_number))
            user = result.scalars().one_or_none()
            if user:
                return str(user.id)
            return None

    async def cache_auth_code(self, user_id: str, auth_code: str):
        await self.cache_da.set(user_id, auth_code, ttl=120)

    async def get_auth_code_by_user_id(self, user_id: str) -> str:
        auth_code = await self.cache_da.get(user_id)
        return auth_code

    async def authenticate_user(self, user_id: str) -> User:
        async with self.db_da.get_or_create_session() as session:
            result = await session.execute(select(User).filter_by(id=user_id))
            user = result.scalars().one_or_none()
            if user:
                user.is_verified = True
                await session.commit()
                await self.cache_da.delete(user_id)
                return user
            return None

    async def get_user_by_id(self, user_id: str) -> User:
        async with self.db_da.get_or_create_session() as session:
            result = await session.execute(select(User).filter_by(id=user_id))
            user = result.scalars().one_or_none()
            return user

    async def delete_user(self, user_id: str):
        async with self.db_da.get_or_create_session() as session:
            result = await session.execute(select(User).filter_by(id=user_id))
            user = result.scalars().one_or_none()
            if user:
                await session.delete(user)
                await session.commit()
                await self.cache_da.delete(user_id)

    async def add_address(self, user_id: str, address_line_1: str, address_line_2: str, city: str, state: str, postal_code: str, country: str) -> str:
        async with self.db_da.get_or_create_session() as session:
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

    async def update_address(self, address_id: str, address_line_1: str, address_line_2: str, city: str, state: str, postal_code: str, country: str):
        async with self.db_da.get_or_create_session() as session:
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

    async def delete_address(self, address_id: str):
        async with self.db_da.get_or_create_session() as session:
            result = await session.execute(select(UserAddress).filter_by(id=address_id))
            address = result.scalars().one_or_none()
            if address:
                await session.delete(address)
                await session.commit()

    async def set_preferred_address(self, address_id: str):
        async with self.db_da.get_or_create_session() as session:
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
