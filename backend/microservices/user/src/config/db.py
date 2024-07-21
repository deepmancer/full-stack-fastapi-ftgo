from ftgo_utils import class_property

from config.base import BaseConfig, env_var

class PostgresConfig(BaseConfig):
    @class_property
    def host(cls):
        return env_var("POSTGRES_HOST", "localhost")

    @class_property
    def port(cls):
        return env_var("POSTGRES_PORT", 5438, int)

    @class_property
    def db(cls):
        return env_var("POSTGRES_DB", "database")

    @class_property
    def user(cls):
        return env_var("POSTGRES_USER", "postgres")

    @class_property
    def password(cls):
        print('fuckkkkkkkkkkkk')
        print(env_var("POSTGRES_PASSWORD", "mypassword"))
        print(env_var("POSTGRES_PASSWORD", "mypassword"))
        return env_var("POSTGRES_PASSWORD", "mypassword")

    @class_property
    def enable_echo_log(cls):
        return env_var("ENABLE_DB_ECHO_LOG", False, bool)

    @class_property
    def enable_force_rollback(cls):
        return env_var("ENABLE_DB_FORCE_ROLLBACK", False, bool)

    @class_property
    def enable_expire_on_commit(cls):
        return env_var("ENABLE_DB_EXPIRE_ON_COMMIT", False, bool)

    @class_property
    def sync_url(cls) -> str:
        return f"postgresql://{cls.user}:{cls.password}@{cls.host}:{cls.port}/{cls.db}"

    @class_property
    def async_url(cls) -> str:
        return f"postgresql+asyncpg://{cls.user}:{cls.password}@{cls.host}:{cls.port}/{cls.db}"
