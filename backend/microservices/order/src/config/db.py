from config.base import BaseConfig, env_var

class MongoConfig(BaseConfig):
    def __init__(
        self,
        host: str = None,
        port: int = None,
        database: str = None,
        username: str = None,
        password: str = None,
    ):
        self.host = host or env_var("MONGO_HOST", default="localhost")
        self.port = port or env_var("MONGO_PORT", default=7017, cast_type=int)
        self.database = database or env_var("MONGO_DATABASE", default="order_database")
        self.username = username or env_var("MONGO_USERNAME", default="order_user")
        self.password = password or env_var("MONGO_PASSWORD", default="order_password")

    @property
    def url(self):
        return f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}"
