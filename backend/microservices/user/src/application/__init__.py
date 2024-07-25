from ftgo_utils.logger import get_logger as _get_logger

from config import ServiceConfig, LayerNames

layer_name = LayerNames.APP.value

def get_logger(layer_name: str = layer_name):
    return _get_logger(layer_name=layer_name, environment=ServiceConfig.load_environment())

from application.vehicle import VehicleService
from application.address import AddressService
from application.profile import ProfileService
