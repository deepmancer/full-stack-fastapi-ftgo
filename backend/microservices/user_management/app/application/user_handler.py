from app.domain.user import UserService
from app.schemas.user import UserCreate
from uuid import UUID

class UserHandler:
    def __init__(self):
        self.user_service = UserService()

    async def create_user(self, first_name: str, last_name: str, phone_number: str, email: str, password: str):
        user_in = UserCreate(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            password=password
        )
        return await self.user_service.create_user(user_in)

    async def get_user_by_id(self, user_id: UUID):
        return await self.user_service.get_user_by_id(user_id)
