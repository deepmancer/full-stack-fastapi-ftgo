from pydantic import BaseModel

class BaseConfig(BaseModel):
    class Config:
        env_file: str = ".env"
        case_sensitive: bool = True
        validate_assignment: bool = True
