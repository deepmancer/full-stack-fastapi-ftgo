from typing import Optional, List, Dict

from loguru import logger

from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from config.db import PostgresConfig
from utils.time import utcnow

from data_access.connection.db import DatabaseDataAccess
from data_access.models.account import Account
from data_access.models.address import Address
from data_access.models.role import Role
from data_access.models.base import Base


class UserRepository:
    data_access: Optional[DatabaseDataAccess] = None

    @classmethod
    def initialize(cls, db_config: PostgresConfig):
        cls.data_access = DatabaseDataAccess(db_config)

    @classmethod
    async def create_user(
        cls,
        first_name: str,
        last_name: str,
        phone_number: str,
        password: str,
        role_name: str,
        national_code: str = None,
    ) -> UserProfile:
        async with cls.data_access.get_or_create_session() as session:
            async with session.begin():
                try:
                    new_account = Account(
                        first_name=first_name,
                        last_name=last_name,
                        phone_number=phone_number,
                        hashed_password=password,
                        national_id=national_id,
                    )
                    session.add(new_account)
                    await session.flush()
                    await session.refresh(new_account)

                    new_role = Role(
                        role_name=role_name,
                        user_id=new_account.id,
                    )
                    session.add(new_role)
                    await session.flush()
                    await session.refresh(new_role)

                    logger.info(f"User with user_id: {new_account.id} and phone_number: {phone_number} was created successfully")    
                    return dict(
                        account=new_account,
                        role=new_role,
                        addresses=[],
                    )
                except Exception as e:
                    await session.rollback()
                    message = f"Error occurred while creating user: {e}"
                    logger.error(message, first_name=first_name, last_name=last_name, phone_number=phone_number, role_name=role_name)
                    raise e
    @classmethod
    async def load_user(cls, user_id: str):
        try:
            account = await cls.data_access.load_from_table_by_query(Account, {"id": user_id}, one_or_none=True)
            role = await cls.data_access.load_from_table_by_query(Role, {"user_id": user_id}, one_or_none=True)
            addresses = await cls.data_access.load_from_table_by_query(Address, {"user_id": user_id})
            return dict(
                account=account,
                role=role,
                addresses=addresses,
            )
        except Exception as e:
            message = f"Error occurred while loading user: {e}"
            logger.error(message, user_id=user_id)
            raise e

    @classmethod
    async def exists_role_for_phone_number(cls, phone_number: str, role_name: str) -> bool:
        async with cls.data_access.get_or_create_session() as session:
            try:
                result = await session.execute(
                    select(Account).join(Role).filter(Account.phone_number == phone_number, Role.role_name == role_name)
                )
                return result.scalars().one_or_none() is not None
            except Exception as e:
                message = f"Error occurred while checking if phone number is taken: {e}"
                logger.error(message, phone_number=phone_number, role_name=role_name)
                raise e

    @classmethod
    async def verify_user(cls, user_id: str) -> Optional[Account]:
        async with cls.data_access.get_or_create_session() as session:
            try:
                result = await session.execute(select(Account).filter_by(id=user_id))
                user_account = result.scalars().one_or_none()
                if user_account:
                    user_account.verified_at = utcnow()
                    await session.commit()

                return user_account
            except Exception as e:
                message = f"Error occurred while authenticating user: {e}"
                logger.error(message, user_id=user_id)
                raise e

    @classmethod
    async def load_user_by_role_and_phone_number(cls, phone_number: str, role_name: str) -> Optional[Account]:
        async with cls.data_access.get_or_create_session() as session:
            try:
                result = await session.execute(
                    select(Account).join(Role).filter(Account.phone_number == phone_number, Role.role_name == role_name)
                )
                user_account = result.scalars().one_or_none()
                return user_account
            except Exception as e:
                message = f"Error occurred while retrieving user by phone number and role: {e}"
                logger.error(message, phone_number=phone_number, role_name=role_name)
                raise e

    @classmethod
    async def delete_user(cls, user_id: str):
        async with cls.data_access.get_or_create_session() as session:
            async with session.begin():
                try:
                    result = await session.execute(select(UserAccount).filter_by(id=user_id))
                    user_account = result.scalars().one_or_none()
                    roles = await session.execute(select(Role).filter_by(user_id=user_id)).scalars().all()
                    for role in roles:
                        await session.delete(role)

                    addresses = await session.execute(select(Address).filter_by(user_id=user_id)).scalars().all()
                    for address in addresses:
                        await session.delete(address)

                    await session.delete(user_account)
                    await session.commit()
                except Exception as e:
                    await session.rollback()
                    message = f"Error occurred while deleting user: {e}"
                    logger.error(message, user_id=user_id)
                    raise e

    @classmethod
    async def add_address(cls, user_id: str, address_line_1: str, address_line_2: str, city: str, postal_code: str = None, country: str = None):
        async with cls.data_access.get_or_create_session() as session:
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
                    await session.commit()
                    return new_address
                except Exception as e:
                    await session.rollback()
                    message = f"Error occurred while adding address: {e}"
                    logger.error(message, user_id=user_id, address_line_1=address_line_1, city=city)
                    raise e

    @classmethod
    async def update_address(cls, address_id, update_data):
        try:
            updated_address = (await cls.data_access.update_table_by_query(Address, {"id": address_id}, update_data))[0]
            return updated_address
        except Exception as e:
            message = f"Error occurred while updating address: {e}"
            logger.error(message, address_id=address_id, update_data=update_data)
            raise e

    @classmethod
    async def unset_user_default_addresses(cls, user_id: str):
        try:
            await cls.data_access.update_table_by_query(Address, {"user_id": user_id}, {"is_default": False})
        except Exception as e:
            message = f"Error occurred while unsetting default address: {e}"
            logger.error(message, user_id=user_id)
            raise e

    @classmethod
    async def delete_address(cls, address_id: str):
        try:
            await cls.data_access.delete_from_table_by_query(Address, {"id": address_id})
        except Exception as e:
            message = f"Error occurred while deleting address: {e}"
            logger.error(message, address_id=address_id)
            raise e


    @classmethod
    async def get_user_addresses(cls, user_id: str) -> List[Address]:
        try:
            addresses = await cls.data_access.load_from_table_by_query(Address, {"user_id": user_id})
            return addresses
        except Exception as e:
            message = f"Error occurred while retrieving addresses by user ID: {e}"
            logger.error(message, user_id=user_id)
            raise e

    @classmethod
    async def get_address_by_id(cls, address_id: str) -> Optional[Address]:
        try:
            address = await cls.data_access.load_from_table_by_query(Address, {"id: address_id"}, one_or_none=True)
            return address
        except Exception as e:
            message = f"Error occurred while retrieving address: {e}"
            logger.error(message, address_id=address_id)
            raise e
