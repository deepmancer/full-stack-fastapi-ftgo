from starlette.authentication import BaseUser
from schemas.user import UserSchema

class FastAPIUser(BaseUser):
    def __init__(self, user: UserSchema):
        self.user_schema = user

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return f'{self.user_schema.user_id} {self.user_schema.role}'

    @property
    def identity(self) -> str:
        return self.user_schema.user_id
