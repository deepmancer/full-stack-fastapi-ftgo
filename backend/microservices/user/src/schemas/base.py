from pydantic import BaseModel, Field, field_validator, ConfigDict, ValidationError

class BaseSchema(BaseModel):    
    model_config = ConfigDict(from_attributes=True, validate_assignment=True, populate_by_name=True)
