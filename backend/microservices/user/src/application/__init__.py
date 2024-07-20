from ftgo_utils.logger import get_logger as _get_logger

from config import ServiceConfig, LayerNames
from application.vehicle import VehicleService
from application.address import AddressService
from application.profile import ProfileService

def get_logger():
    return _get_logger(LayerNames.APP.value, ServiceConfig.environment)
