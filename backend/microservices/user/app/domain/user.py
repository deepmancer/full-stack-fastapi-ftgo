from data_access.crud.address import UserRepository
from data_access.session.cache import RedisSession
import uuid

class UserService:
    def __init__(self, user_repository: UserRepository, redis_session: RedisSession):
        self.user_repository = user_repository
        self.redis_session = redis_session

    async def register(self, first_name: str, last_name: str, phone_number: str, password: str) -> str:
        user_id = await self.user_repository.create_user(first_name, last_name, phone_number, password)
        auth_code = str(uuid.uuid4())[:6]
        await self.redis_session.client.setex(f'auth_code:{user_id}', 120, auth_code)
        return auth_code

    async def authenticate_phone_number(self, phone_number: str, auth_code: str) -> bool:
        user_id = await self.user_repository.get_user_id_by_phone_number(phone_number)
        stored_code = await self.redis_session.client.get(f'auth_code:{user_id}')
        if stored_code and stored_code == auth_code:
            await self.user_repository.verify_phone_number(user_id)
            return True
        return False

    async def login(self, phone_number: str, password: str) -> str:
        user = await self.user_repository.authenticate_user(phone_number, password)
        return user.generate_jwt()

    async def get_user_info(self, user_id: str) -> dict:
        user = await self.user_repository.get_user_by_id(user_id)
        return {
            "id": str(user.id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": user.phone_number,
            "phone_number_verified": user.phone_number_verified,
            "email": user.email,
            "gender": user.gender,
            "created_at": str(user.created_at),
            "updated_at": str(user.updated_at)
        }

    async def add_address(self, user_id: str, address_line_1: str, address_line_2: str, city: str, state: str, postal_code: str, country: str) -> str:
        address_id = await self.user_repository.add_address(user_id, address_line_1, address_line_2, city, state, postal_code, country)
        return address_id

    async def modify_address(self, address_id: str, address_line_1: str, address_line_2: str, city: str, state: str, postal_code: str, country: str) -> bool:
        await self.user_repository.update_address(address_id, address_line_1, address_line_2, city, state, postal_code, country)
        return True

    async def delete_address(self, address_id: str) -> bool:
        await self.user_repository.delete_address(address_id)
        return True

    async def set_preferred_address(self, address_id: str) -> bool:
        await self.user_repository.set_preferred_address(address_id)
        return True
