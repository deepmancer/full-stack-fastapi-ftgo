import pytz
from datetime import datetime

def utcnow():
    return datetime.now(pytz.UTC)

def utcnow_timestamp():
    return int(datetime.now(pytz.UTC).timestamp())
