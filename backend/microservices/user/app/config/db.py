from config.base import BaseConfig
from decouple import config as de_config

class PostgresConfig(BaseConfig):
    container_name: str = de_config("DB_CONTAINER_NAME", default="user_db")

    host: str = de_config("POSTGRES_HOST")
    port: int = de_config("POSTGRES_PORT", cast=int)
    db: str = de_config("POSTGRES_DB")
    user: str = de_config("POSTGRES_USERNAME")
    password: str = de_config("POSTGRES_PASSWORD")
    db_schema: str = de_config("POSTGRES_SCHEMA", default="postgresql", cast=str)

    enable_echo_log: bool = de_config("ENABLE_DB_ECHO_LOG", default=False, cast=bool)
    enable_force_rollback: bool = de_config("ENABLE_DB_FORCE_ROLLBACK", default=False, cast=bool)
    enable_expire_on_commit: bool = de_config("ENABLE_DB_EXPIRE_ON_COMMIT", default=True, cast=bool)

    @property
    def local_url(self) -> str:
        return f"{self.db_schema}://{self.user}:{self.password}@localhost:{self.port}/{self.db}"

    @property
    def sync_url(self) -> str:
        return f"{self.db_schema}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
    
    @property
    def async_url(self) -> str:
        return f"{self.db_schema}+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
