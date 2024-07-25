from typing import Optional, List, Dict

from loguru import logger

from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from config.db import PostgresConfig
from utils.time import utcnow

from data_access.connection.db import DatabaseDataAccess
from data_access.models.location import DriverLocation
from data_access.models.base import Base


class UserRepository:
    data_access: Optional[DatabaseDataAccess] = None

    @classmethod
    def initialize(cls, db_config: PostgresConfig):
        cls._data_access = DatabaseDataAccess(db_config)

    @classmethod
    async def create_user(
        cls,
        user_id: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        hashed_password: str,
        role: str,
        national_id: str = None,
    ) -> Profile:
        async with cls._data_access.get_or_create_session() as session:
            async with session.begin():
                try:
                    new_profile = Profile(
                        id=user_id,
                        first_name=first_name,
                        last_name=last_name,
                        phone_number=phone_number,
                        hashed_password=hashed_password,
                        national_id=national_id,
                        role=role,
                    )
                    session.add(new_profile)
                    await session.flush()
                    await session.refresh(new_profile)

                    logger.info(f"User with user_id: {new_profile.id} and phone_number: {new_profile.phone_number} was created successfully")    
                    return new_profile
                except Exception as e:
                    await session.rollback()
                    message = f"Error occurred while creating user: {e}"
                    logger.error(message, first_name=first_name, last_name=last_name, phone_number=phone_number, role=role, national_id=national_id, hashed_password=hashed_password)
                    raise e

    @classmethod
    async def load_user_by_id(cls, user_id: str):
        try:
            profile = await cls._data_access.load_from_table_by_query(Profile, {"id": user_id}, one_or_none=True)
            return profile
        except Exception as e:
            message = f"Error occurred while loading user: {e}"
            logger.error(message, user_id=user_id)
            return None

    @classmethod
    async def load_user_by_phone_number_and_role(cls, phone_number: str, role: str):
        try:
            profile = await cls._data_access.load_from_table_by_query(Profile, {"phone_number": phone_number, "role": role}, one_or_none=True)
            return profile
        except Exception as e:
            message = f"Error occurred while loading user by phone number & role: {e}"
            logger.error(message, phone_number=phone_number, role=role)
            return None

    @classmethod
    async def exists_role_for_phone_number(cls, phone_number: str, role: str) -> bool:
        try:
            result = await cls._data_access.load_from_table_by_query(Profile, {"phone_number": phone_number, "role": role}, one_or_none=False)
            return len(result) > 0
        except Exception as e:
            message = f"Error occurred while checking if phone number is taken: {e}"
            logger.error(message, phone_number=phone_number, role=role)
            raise e

    @classmethod
    async def verify_user(cls, user_id: str) -> Optional[Profile]:
        async with cls._data_access.get_or_create_session() as session:
            try:
                result = await session.execute(select(Profile).filter_by(id=user_id))
                user_profile = result.scalars().one_or_none()
                if user_profile:
                    user_profile.verified_at = utcnow()
                    await session.commit()
                    await session.refresh(user_profile)  # Refresh to ensure the instance is up-to-date and bound
                
                return user_profile
            except Exception as e:
                message = f"Error occurred while verifying user: {e}"
                logger.error(message, user_id=user_id)
                raise e

    @classmethod
    async def delete_user(cls, user_id: str):
        async with cls._data_access.get_or_create_session() as session:
            async with session.begin():
                try:
                    result = await session.execute(select(Profile).filter_by(id=user_id))
                    user_profile = result.scalars().one_or_none()
                  
                    addresses = (await session.execute(select(Address).filter_by(user_id=user_id))).scalars().all()
                    for address in addresses:
                        await session.delete(address)
                    await session.delete(user_profile)

                    await session.commit()
                except Exception as e:
                    await session.rollback()
                    message = f"Error occurred while deleting user: {e}"
                    logger.error(message, user_id=user_id)
                    raise e

    @classmethod
    async def add_address(cls, user_id: str, address_line_1: str, address_line_2: str, city: str, postal_code: str = None, country: str = None):
        async with cls._data_access.get_or_create_session() as session:
            async with session.begin():
                try:
                    new_address = Address(
                        user_id=user_id,
                        address_line_1=address_line_1,
                        address_line_2=address_line_2,
                        city=city,
                        postal_code=postal_code,
                        country=country,
                    )
                    session.add(new_address)
                    await session.flush()
                    await session.refresh(new_address)
                    return new_address
                except Exception as e:
                    await session.rollback()
                    message = f"Error occurred while adding address: {e}"
                    logger.error(message, user_id=user_id, address_line_1=address_line_1, city=city)
                    raise e

    @classmethod
    async def update_address(cls, address_id, update_data):
        try:
            updated_address = (await cls._data_access.update_table_by_query(Address, {"id": address_id}, update_data))[0]
            return updated_address
        except Exception as e:
            message = f"Error occurred while updating address: {e}"
            logger.error(message, address_id=address_id, update_data=update_data)
            raise e

    @classmethod
    async def unset_user_default_addresses(cls, user_id: str):
        try:
            await cls._data_access.update_table_by_query(Address, {"user_id": user_id}, {"is_default": False})
        except Exception as e:
            message = f"Error occurred while unsetting default address: {e}"
            logger.error(message, user_id=user_id)
            raise e

    @classmethod
    async def delete_address(cls, address_id: str):
        try:
            await cls._data_access.delete_from_table_by_query(Address, {"id": address_id})
        except Exception as e:
            message = f"Error occurred while deleting address: {e}"
            logger.error(message, address_id=address_id)
            raise e


    @classmethod
    async def load_user_addresses(cls, user_id: str) -> List[Address]:
        try:
            addresses = await cls._data_access.load_from_table_by_query(Address, {"user_id": user_id})
            return addresses
        except Exception as e:
            message = f"Error occurred while retrieving addresses by user ID: {e}"
            logger.error(message, user_id=user_id)
            raise e

    @classmethod
    async def load_address_by_id(cls, address_id: str) -> Optional[Address]:
        try:
            address = await cls._data_access.load_from_table_by_query(Address, {"id: address_id"}, one_or_none=True)
            return address
        except Exception as e:
            message = f"Error occurred while retrieving address: {e}"
            logger.error(message, address_id=address_id)
            raise e

    @classmethod
    async def delete_unverified_users(cls) -> List[str]:
        async with cls._data_access.get_or_create_session() as session:
            async with session.begin():
                try:
                    result = await session.execute(select(Profile).filter_by(verified_at=None))
                    unverified_users = result.scalars().all()
                    unverified_user_ids = [user.id for user in unverified_users]
                    
                    for user in unverified_users:
                        addresses = (await session.execute(select(Address).filter_by(user_id=user.id))).scalars().all()
                        for address in addresses:
                            await session.delete(address)
                    
                    for user in unverified_users:
                        await session.delete(user)
                    
                    await session.commit()
                    
                    logger.info(f"Deleted unverified users: {unverified_user_ids}")
                    return unverified_user_ids
                except Exception as e:
                    await session.rollback()
                    message = f"Error occurred while deleting unverified users: {e}"
                    logger.error(message)
                    raise e
