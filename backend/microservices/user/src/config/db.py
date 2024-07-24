from config.base import BaseConfig, env_var

class PostgresConfig(BaseConfig):
    def __init__(
        self,
        host: str = None,
        port: int = None,
        db: str = None,
        user: str = None,
        password: str = None,
        enable_echo_log: bool = None,
        enable_force_rollback: bool = None,
        enable_expire_on_commit: bool = None,
    ):
        self.host = host or env_var("POSTGRES_HOST", default="localhost")
        self.port = port or env_var("POSTGRES_PORT", default=5438, cast_type=int)
        self.db = db or env_var("POSTGRES_DB", default="user_database")
        self.user = user or env_var("POSTGRES_USER", default="user_user")
        self.password = password or env_var("POSTGRES_PASSWORD", default="user_password")
        self.enable_echo_log = enable_echo_log or env_var(
            "ENABLE_DB_ECHO_LOG", default=False, cast_type=lambda s: isinstance(s, str) and s.lower() in ['true', '1']
        )
        self.enable_force_rollback = enable_force_rollback or env_var(
            "ENABLE_DB_FORCE_ROLLBACK", default=False, cast_type=lambda s: isinstance(s, str) and s.lower() in ['true', '1']
        )
        self.enable_expire_on_commit = enable_expire_on_commit or env_var(
            "ENABLE_DB_EXPIRE_ON_COMMIT", default=False, cast_type=lambda s: isinstance(s, str) and s.lower() in ['true', '1']
        )

    @property
    def url(self):
        return self.async_url

    @property
    def sync_url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    @property
    def async_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
