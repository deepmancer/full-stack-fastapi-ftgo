from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict, ValidationError

from ftgo_utils.enums import Roles, Gender
from ftgo_utils.validation import validate_phone_number, validate_enum_value

from schemas.base import BaseSchema

class PhoneNumberMixin(BaseSchema):
    phone_number: str = Field(..., min_length=10, max_length=14)

    @field_validator('phone_number', mode='before')
    def validate_phone_number_field(cls, value):
        return validate_phone_number(value)


class RoleMixin(BaseSchema):
    role: str = Field(..., min_length=1, max_length=10)

    @field_validator('role', mode='before')
    def validate_role_field(cls, value):
        return validate_enum_value(value, Roles, 'role')

class GenderMixin(BaseSchema):
    gender: Optional[str] = Field(None, min_length=1, max_length=10)

    @field_validator('gender', mode='before')
    def validate_gender_role(cls, value):
        if not value:
            return None
        return validate_enum_value(value, Gender, 'gender')

class NationalIdMixin(BaseSchema):
    national_id: Optional[str] = Field(None, min_length=1, max_length=20)

    @field_validator('national_id', mode='before')
    def validate_national_id_field(cls, value):
        if not value:
            return None
        if not value.isdigit():
            raise ValidationError('national_id should only contain digits')
        return value.strip()

def uuid_field() -> Field:
    return Field(..., min_length=1, max_length=36)
