from config.base import BaseConfig, env_var

class PasswordConfig(BaseConfig):
    def __init__(self, schema: str = "bcrypt", rounds: int = 12):
        self.schema = schema
        self.rounds = rounds
        
    @classmethod
    def load(cls):
        return cls(
            schema=env_var("PASSWORD_SCHEMA", default="bcrypt"),
            rounds=env_var("PASSWORD_ROUNDS", default=12, cast_type=int)
        )
