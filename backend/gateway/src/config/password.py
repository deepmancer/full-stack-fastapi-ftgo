from config.base import BaseConfig

class PasswordConfig(BaseConfig):
    schema: str = "bcrypt"
    rounds: int = 12
