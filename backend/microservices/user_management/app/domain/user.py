from sqlalchemy.future import select
from app.data_access.models.user import User
from app.schemas.user import UserCreate
from app.data_access.session import get_session
from uuid import uuid4

class UserService:
    def __init__(self):
        self.db = next(get_session())

    async def create_user(self, user_in: UserCreate) -> User:
        new_user = User(
            id=uuid4(),
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            phone_number=user_in.phone_number,
            email=user_in.email,
            hashed_password=user_in.password,
            email_verified=False,
            phone_number_verified=False
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def get_user_by_id(self, user_id: uuid4) -> User:
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()