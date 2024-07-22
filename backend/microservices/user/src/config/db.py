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
        if host is None:
            config = self.load()
            self.host = config.host
            self.port = config.port
            self.db = config.db
            self.user = config.user
            self.password = config.password
            self.enable_echo_log = config.enable_echo_log
            self.enable_force_rollback = config.enable_force_rollback
            self.enable_expire_on_commit = config.enable_expire_on_commit
        else:
            self.host = host
            self.port = port
            self.db = db
            self.user = user
            self.password = password
            self.enable_echo_log = enable_echo_log
            self.enable_force_rollback = enable_force_rollback
            self.enable_expire_on_commit = enable_expire_on_commit
        
    @classmethod
    def load(cls):
        return cls(
            host=env_var("POSTGRES_HOST", default="localhost"),
            port=env_var("POSTGRES_PORT", default=5438, cast_type=int),
            db=env_var("POSTGRES_DB", default="user_database"),
            user=env_var("POSTGRES_USER", default="user_user"),
            password=env_var("POSTGRES_PASSWORD", default="user_password"),
            enable_echo_log=env_var("ENABLE_DB_ECHO_LOG", default=False, cast_type=lambda s: isinstance(s, str) and s.lower() in ['true', '1']),
            enable_force_rollback=env_var("ENABLE_DB_FORCE_ROLLBACK", default=False, cast_type=lambda s:  isinstance(s, str) and s.lower() in ['true', '1']),
            enable_expire_on_commit=env_var("ENABLE_DB_EXPIRE_ON_COMMIT", default=False, cast_type=lambda s:  isinstance(s, str) and s.lower() in ['true', '1'])
        )

    @property
    def sync_url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    @property
    def async_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
