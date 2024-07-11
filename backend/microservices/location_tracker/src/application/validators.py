import uuid
import datetime
from config.timezone import tz as UTC
import string
import validators
from pydantic import ValidationError
from config.enums import Status
from config.location import KEEP_LAST_LOCATIONS_COUNT, ACCURACY_THRESHOLD, MAXIMUM_SPEED_THRESHOLD, TIMESTAMP_MAXIMUM_DELAY_THRESHOLD

from application.exceptions import (
    InvalidUserUUDDError, TooOldTimestampError, AbnormalSpeedError, NoisyLocationError, StatusValueError,
)

def validate_status(status: str):
    try:
        status = status.strip()
        eligible_statuses = [field.value for field in Status]
        if status not in eligible_statuses:
            raise ValueError(f"Invalid status name {status}, must be one of {eligible_statuses}")
        return status
    except ValueError as e:
        raise ValueError(str(StatusValueError(status, message=str(e))))
    
def validate_uuid(user_id: str):
    try:
        if not user_id:
            raise Exception
        user_id = user_id.strip()
        user_uuid = uuid.UUID(user_id, version=4)
        return user_id
    except Exception as e:
        raise ValueError(str(InvalidUserUUDDError(user_id, message=str(e.args[0]))))

def validate_timestamp(timestamp):
    try:
        if not isinstance(timestamp, float):
            timestamp = float(timestamp)

        if timestamp > 1e12:
            timestamp /= 1000
            
        timestamp_dt = datetime.datetime.fromtimestamp(timestamp, UTC)
        if datetime.datetime.now(UTC) - timestamp_dt > datetime.timedelta(seconds=TIMESTAMP_MAXIMUM_DELAY_THRESHOLD):
            raise TooOldTimestampError(timestamp_dt)
        return float(timestamp)
    except Exception as e:
        raise ValueError(str(e))


def validate_speed(speed):
    if speed is None:
        return speed
    try:
        if speed is not None:
            if speed > MAXIMUM_SPEED_THRESHOLD:
                raise AbnormalSpeedError(speed=speed)
            speed_m_s = speed * 1000 / 3600
            return speed_m_s
    except AbnormalSpeedError as e:
        raise ValueError(str(e))
    except Exception as e:
        return None
    
def validate_accuracy(accuracy):
    try:
        if accuracy > ACCURACY_THRESHOLD:
            raise NoisyLocationError(accuracy=accuracy)
        return accuracy
    except Exception as e:
        raise ValueError(str(e))
