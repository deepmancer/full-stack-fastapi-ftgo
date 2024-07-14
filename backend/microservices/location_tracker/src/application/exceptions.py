from typing import Optional
import json
from config.exceptions import ApplicationError


class TooOldTimestampError(ApplicationError):
    def __init__(self, timestamp_date, message: Optional[str] = None,):
        base_message = f"Timestamp with date {timestamp_date} is too old"
        super().__init__(base_message, message)
   
class AbnormalSpeedError(ApplicationError):
    def __init__(self, speed, message: Optional[str] = None,):
        base_message = f"Speed {speed} is too high"
        super().__init__(base_message, message)

class NoisyLocationError(ApplicationError):
    def __init__(self, accuracy, message: Optional[str] = None,):
        base_message = f"Accuracy {accuracy} is too high"
        super().__init__(base_message, message)

class StatusValueError(ApplicationError):
    def __init__(self, status: str, message: Optional[str] = None):
        base_message = f"Status of {status} is invalid"
        super().__init__(base_message, message)

class InvalidUserUUDDError(ApplicationError):
    def __init__(self, user_id: str, message: Optional[str] = None):
        base_message = f"User id {user_id} is not a valid UUID (v4)"
        super().__init__(base_message, message)
