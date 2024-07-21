from config.base import BaseConfig, env_var
from decouple import config as de_config

class PostgresConfig(BaseConfig):
    container_name: str = env_var("DB_CONTAINER_NAME", "user_db")

    host: str = env_var("POSTGRES_HOST", "localhost")
    port: int = env_var("POSTGRES_PORT", 5432, int)
    db: str = env_var("POSTGRES_DB", "database")
    user: str = env_var("POSTGRES_USERNAME", "postgres")
    password: str = env_var("POSTGRES_PASSWORD", "mypassword")
    db_schema: str = env_var("POSTGRES_SCHEMA", "postgresql")

    enable_echo_log: bool = env_var("ENABLE_DB_ECHO_LOG", False, bool)
    enable_force_rollback: bool = env_var("ENABLE_DB_FORCE_ROLLBACK", False, bool)
    enable_expire_on_commit: bool = env_var("ENABLE_DB_EXPIRE_ON_COMMIT", False, bool)

    @property
    def sync_url(self) -> str:
        return f"{self.db_schema}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
    
    @property
    def async_url(self) -> str:
        return f"{self.db_schema}+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
