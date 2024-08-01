from pydantic import Field

from ftgo_utils.schemas import BaseSchema

class DriverStatusSchema(BaseSchema):
    is_online: bool = Field(...)
