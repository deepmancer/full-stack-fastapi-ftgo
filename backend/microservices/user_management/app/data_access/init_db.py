from data_access.models.user_profile import User
from foodzood.backend.microservices.user_management.app.data_access.session import async_session

async def init_db():
    async with async_session() as session:
        await session.run_sync(User.metadata.create_all)
