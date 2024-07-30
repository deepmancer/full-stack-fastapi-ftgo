from typing import Optional

from pydantic import Field

from ftgo_utils.schemas import BaseSchema

class EmptyResponse(BaseSchema):
    pass

class SuccessResponse(BaseSchema):
    success: Optional[bool] = Field(True)
