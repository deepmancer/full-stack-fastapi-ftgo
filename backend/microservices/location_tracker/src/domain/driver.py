from typing import List, Optional
from schemas.location import LocationSchema
from domain.location import DriverLocationHandler
from config.enums import Status
from data_access.repository.location import LocationRepository
from config.location import MAXIMUM_LOCATION_TO_STORE_PER_DRIVER
from data_access.repository.status import StatusRepository

from domain.location import DriverLocationHandler

class DriverDomain:
    def __init__(self, driver_id, status):
        self.driver_id = driver_id
        self.status = status

    async def add_locations(self, locations: List[LocationSchema]):
        if self.status == Status.OFFLINE.value:
            await DriverLocationHandler.delete_driver_locations(self.driver_id)
            await StatusRepository.set_driver_status(self.driver_id, status=Status.ONLINE.value)
            self.status = Status.ONLINE.value
            locations_to_persist = sorted(locations, key=lambda x: -1 * x.timestamp)[:MAXIMUM_LOCATION_TO_STORE_PER_DRIVER]
        else:
            current_locations = await DriverLocationHandler.load_driver_locations(self.driver_id)
            new_locations = [('current', location) for location in current_locations] + [('new', location) for location in locations]
            new_locations = sorted(new_locations, key=lambda x: -1 * x[1].timestamp)
            new_locations = new_locations[:MAXIMUM_LOCATION_TO_STORE_PER_DRIVER]
            locations_to_persist = [location for group, location in new_locations if group == 'new']
        
        await DriverLocationHandler.save_driver_locations(self.driver_id, locations_to_persist)
    
    async def change_status(self, status: str):
        if status == self.status:
            return

        await DriverLocationHandler.delete_driver_locations(self.driver_id)
        await StatusRepository.set_driver_status(self.driver_id, status=status)
        self.status = status

        