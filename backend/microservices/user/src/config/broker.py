from config.base import BaseConfig, env_var

class BrokerConfig(BaseConfig):
    def __init__(
        self,
        host: str = None,
        port: int = None,
        user: str = None,
        password: str = None,
        vhost: str = None,
    ):
        self.host = host or env_var("RABBITMQ_HOST", default="localhost")
        self.port = port or env_var("RABBITMQ_PORT", default=5672, cast_type=int)
        self.user = user or env_var("RABBITMQ_USER", default="rabbitmq_user")
        self.password = password or env_var("RABBITMQ_PASS", default="rabbitmq_password")
        self.vhost = vhost or env_var("RABBITMQ_VHOST", default="/")
