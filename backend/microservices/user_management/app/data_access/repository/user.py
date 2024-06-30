from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.data_access.models.user import User
from uuid import uuid4

class UserRepository:

    async def create_user(self, db: AsyncSession, user: User) -> User:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def get_user_by_id(self, db: AsyncSession, user_id: uuid4) -> User:
        result = await db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()
