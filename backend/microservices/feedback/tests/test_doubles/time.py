import asyncio
import datetime
from typing import Optional

from freezegun import freeze_time


class TimeProvider:
    def __init__(self, timestamp: float) -> None:
        self._frozen_time_cls = freeze_time(datetime.datetime.fromtimestamp(timestamp))
        self._frozen_time = None

    def start(self) -> freeze_time:
        self._frozen_time = self._frozen_time_cls.start()
        return self._frozen_time

    def advance_time(self, seconds: int) -> None:
        if self._frozen_time is not None:
            self._frozen_time.tick(datetime.timedelta(seconds=seconds+1e-2))

    def stop(self) -> None:
        if self._frozen_time is not None:
            self._frozen_time_cls.stop()
            self._frozen_time = None

    def current_timestamp(self) -> Optional[float]:
        if self._frozen_time is not None:
            return self._frozen_time.time_to_freeze.timestamp()
        return None

    def current_datetime(self) -> Optional[datetime.datetime]:
        if self._frozen_time is not None:
            return self._frozen_time.time_to_freeze
        return None
