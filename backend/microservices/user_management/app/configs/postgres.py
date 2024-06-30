import os
from pydantic import BaseModel
from dotenv import load_dotenv

from utils.dynamic_port import get_dynamic_port

load_dotenv()

class PostgresConfig(BaseModel):
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_CONTAINER_NAME: str = os.getenv("POSTGRES_CONTAINER_NAME", "user_postgres")
    POSTGRES_INTERNAL_PORT: int = int(os.getenv("POSTGRES_INTERNAL_PORT", 5432))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "user_db")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")

    class Config:
        env_file = ".env"

    @property
    def port(self) -> int:
        try:
            return int(get_dynamic_port(self.POSTGRES_CONTAINER_NAME, self.POSTGRES_INTERNAL_PORT))
        except Exception as e:
            print(f"Error fetching PostgreSQL dynamic port: {e}")
            return self.POSTGRES_INTERNAL_PORT

    @property
    def host(self) -> str:
        return self.POSTGRES_HOST

    @property
    def db(self) -> str:
        return self.POSTGRES_DB

    @property
    def user(self) -> str:
        return self.POSTGRES_USER

    @property
    def password(self) -> str:
        return self.POSTGRES_PASSWORD
