from data_access.models.user_profile import User
from data_access.models.address import UserAddress
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from uuid import UUID

class UserRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def create_user(self, first_name: str, last_name: str, phone_number: str, password: str) -> str:
        async with self.session_factory() as session:
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                hashed_password=password  # Ideally, hash password before saving
            )
            session.add(new_user)
            await session.commit()
            return str(new_user.id)

    async def get_user_id_by_phone_number(self, phone_number: str) -> str:
        async with self.session_factory() as session:
            result = await session.execute(select(User.id).filter_by(phone_number=phone_number))
            return str(result.scalar())

    async def verify_phone_number(self, user_id: str):
        async with self.session_factory() as session:
            await session.execute(
                select(User).filter_by(id=UUID(user_id)).update({'phone_number_verified': True})
            )
            await session.commit()

    async def authenticate_user(self, phone_number: str, password: str) -> User:
        async with self.session_factory() as session:
            result = await session.execute(
                select(User).filter_by(phone_number=phone_number, hashed_password=password)
            )
            return result.scalar_one()

    async def get_user_by_id(self, user_id: str) -> User:
        async with self.session_factory() as session:
            result = await session.execute(
                select(User).options(joinedload(User.addresses)).filter_by(id=UUID(user_id))
            )
            return result.scalar_one()

    async def add_address(self, user_id: str, address_line_1: str, address_line_2: str, city: str, state: str, postal_code: str, country: str) -> str:
        async with self.session_factory() as session:
            new_address = UserAddress(
                user_id=UUID(user_id),
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                city=city,
                state=state,
                postal_code=postal_code,
                country=country
            )
            session.add(new_address)
            await session.commit()
            return str(new_address.id)

    async def update_address(self, address_id: str, address_line_1: str, address_line_2: str, city: str, state: str, postal_code: str, country: str):
        async with self.session_factory() as session:
            await session.execute(
                select(UserAddress).filter_by(id=UUID(address_id)).update({
                    'address_line_1': address_line_1,
                    'address_line_2': address_line_2,
                    'city': city,
                    'state': state,
                    'postal_code': postal_code,
                    'country': country
                })
            )
            await session.commit()

    async def delete_address(self, address_id: str):
        async with self.session_factory() as session:
            await session.execute(
                select(UserAddress).filter_by(id=UUID(address_id)).delete()
            )
            await session.commit()

    async def set_preferred_address(self, address_id: str):
        async with self.session_factory() as session:
            address = await session.get(UserAddress, UUID(address_id))
            user_id = address.user_id
            await session.execute(
                select(UserAddress).filter_by(user_id=user_id).update({'is_default': False})
            )
            await session.execute(
                select(UserAddress).filter_by(id=UUID(address_id)).update({'is_default': True})
            )
            await session.commit()
