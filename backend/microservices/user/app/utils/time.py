import pytz
from datetime import datetime

def utcnow():
    return int(datetime.now(pytz.UTC).timestamp())
