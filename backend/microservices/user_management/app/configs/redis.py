import os
from pydantic import BaseModel
from dotenv import load_dotenv
from utils.dynamic_port import get_dynamic_port

load_dotenv()

class RedisConfig(BaseModel):
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_CONTAINER_NAME: str = os.getenv("REDIS_CONTAINER_NAME", "user_redis")
    REDIS_INTERNAL_PORT: int = int(os.getenv("REDIS_INTERNAL_PORT", 6379))
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))

    class Config:
        env_file = ".env"

    @property
    def port(self) -> int:
        try:
            return int(get_dynamic_port(self.REDIS_CONTAINER_NAME, self.REDIS_INTERNAL_PORT))
        except Exception as e:
            print(f"Error fetching Redis dynamic port: {e}")
            return self.REDIS_INTERNAL_PORT
    
    @property
    def host(self) -> str:
        return self.REDIS_HOST

    @property
    def db(self) -> int:
        return self.REDIS_DB
