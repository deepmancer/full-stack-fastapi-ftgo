import time
import datetime
from typing import Optional, Any

from ftgo_utils.constants import Provinces
from ftgo_utils.geo import get_province, get_country, get_hexagon_id

from config import LocationConfig

class GeoLocation:
    def __init__(
        self,
        latitude: float,
        longitude: float,
        timestamp: Optional[Any] = None,
        accuracy: Optional[float] = None,
        speed: Optional[float] = None,
        bearing: Optional[float] = None,
    ):
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp
        self.accuracy = accuracy
        self.speed = speed
        self.bearing = bearing
        self._province = get_province(self.latitude, self.longitude, return_closest=True)
        self._country = get_country(self.latitude, self.longitude)

    @property
    def _config(self) -> LocationConfig:
        return LocationConfig()

    @property
    def province(self) -> str:
        return self._province
    
    @property
    def country(self) -> str:
        return self._country

    def _validate_accuracy(self) -> bool:
        if self.accuracy is None:
            return False
        return self.accuracy <= self._config.accuracy_threshold_m

    def _validate_speed(self) -> bool:
        if self.speed is None:
            return False
        return self.speed <= self._config.maximum_speed_threshold_m

    def _validate_timestamp(self) -> bool:
        if self.timestamp is None:
            return False
        current_timestamp = int(time.time())
        return current_timestamp - self.timestamp <= self._config.timestamp_maximum_delay_threshold_s

    def _validate_latitude(self) -> bool:
        return -90 <= self.latitude <= 90

    def _validate_longitude(self) -> bool:
        return -180 <= self.longitude <= 180

    def _validate_bearing(self) -> bool:
        return self.bearing is None or 0 <= self.bearing <= 360

    def _validate_province(self) -> bool:
        return self._province in Provinces.values()

    def is_valid(self) -> bool:
        return True
        try:
            return all([
                self._validate_accuracy(),
                self._validate_speed(),
                self._validate_timestamp(),
                self._validate_latitude(),
                self._validate_longitude(),
                self._validate_bearing(),
                self._validate_province(),
            ])
        except Exception:
            return False

    def get_hexagon_index(self, resolution: int) -> str:
        return get_hexagon_id(lat=self.latitude, lng=self.longitude, resolution=resolution)

    def to_dict(self) -> dict:
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timestamp": self.timestamp,
            "accuracy": self.accuracy,
            "speed": self.speed,
            "bearing": self.bearing,
            "province": self.province,
        }
        
    @classmethod
    def from_dict(cls, data: dict) -> 'GeoLocation':
        return cls(
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            timestamp=data.get("timestamp"),
            accuracy=data.get("accuracy"),
            speed=data.get("speed"),
            bearing=data.get("bearing"),
        )
