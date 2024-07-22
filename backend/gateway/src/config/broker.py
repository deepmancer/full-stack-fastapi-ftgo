from config.base import BaseConfig, env_var

class BrokerConfig(BaseConfig):
    def __init__(
        self,
        host: str = None,
        port: int = None,
        user: str = None,
        password: str = None,
        vhost: str = None,
        ssl: bool = None,
    ):
        if host is None:
            config = self.load()
            self.host = config.host
            self.port = config.port
            self.user = config.user
            self.password = config.password
            self.vhost = config.vhost
            self.ssl = config.ssl
        else:
            self.host = host
            self.port = port
            self.user = user
            self.password = password
            self.vhost = vhost
            self.ssl = ssl
        
    @classmethod
    def load(cls):
        return cls(
            host=env_var("RABBITMQ_HOST", default="localhost"),
            port=env_var("RABBITMQ_PORT", default=5672, cast_type=int),
            user=env_var("RABBITMQ_USER", default="rabbitmq_user"),
            password=env_var("RABBITMQ_PASS", default="rabbitmq_password"),
            vhost=env_var("RABBITMQ_VHOST", default="/"),
            ssl=env_var("RABBITMQ_SSL_CONNECTION", default=False, cast_type=lambda s: isinstance(s, str) and s.lower() in ['true', '1']),
        )
