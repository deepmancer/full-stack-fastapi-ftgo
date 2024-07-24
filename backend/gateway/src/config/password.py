from config.base import BaseConfig, env_var

class PasswordConfig(BaseConfig):
    def __init__(self, schema: str = None, rounds: int = None):
        self.schema = schema or env_var("PASSWORD_SCHEMA", default="bcrypt")
        self.rounds = rounds or env_var("PASSWORD_ROUNDS", default=12, cast_type=int)
