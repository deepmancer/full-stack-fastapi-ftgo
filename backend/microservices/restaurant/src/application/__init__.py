from ftgo_utils.logger import get_logger as _get_logger

from config import ServiceConfig, LayerNames

def get_logger():
    return _get_logger(LayerNames.APP.value, ServiceConfig.load_environment())

from application.menu import MenuService
from application.supplier import RestaurantService
