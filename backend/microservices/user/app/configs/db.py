from pydantic import BaseModel, Field, PostgresDsn
from decouple import config as de_config

class PostgresConfig(BaseModel):
    class Config:
        env_file: str = ".env"
        case_sensitive: bool = True
        validate_assignment: bool = True

    container_name: str = de_config("DB_CONTAINER_NAME", default="user_db")

    host: str = de_config("POSTGRES_HOST")
    port: int = de_config("POSTGRES_PORT", cast=int)
    db: str = de_config("POSTGRES_DB")
    user: str = de_config("POSTGRES_USERNAME")
    password: str = de_config("POSTGRES_PASSWORD")
    db_schema: str = de_config("POSTGRES_SCHEMA", default="postgresql", cast=str)

    max_pool_con: int = de_config("DB_MAX_POOL_CON", default=10, cast=int)
    pool_size: int = de_config("DB_POOL_SIZE", default=5, cast=int)
    pool_overflow: int = de_config("DB_POOL_OVERFLOW", default=10, cast=int)
    timeout: int = de_config("DB_TIMEOUT", default=30, cast=int)

    enable_echo_log: bool = de_config("ENABLE_DB_ECHO_LOG", default=False, cast=bool)
    enable_force_rollback: bool = de_config("ENABLE_DB_FORCE_ROLLBACK", default=False, cast=bool)
    enable_expire_on_commit: bool = de_config("ENABLE_DB_EXPIRE_ON_COMMIT", default=True, cast=bool)

    @property
    def sync_url(self) -> str:
        return f"{self.db_schema}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
    
    @property
    def async_url(self) -> str:
        return f"{self.db_schema}+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
