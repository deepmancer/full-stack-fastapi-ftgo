from typing import Dict, Any

from domain.driver import DriverDomain

class VehicleService:
    """
    Service class for managing vehicle registrations and information.
    """

    @staticmethod
    async def register_vehicle(user_id: str, plate_number: str, license_number: str) -> Dict[str, Any]:
        """
        Registers a vehicle for the user.

        :param user_id: ID of the user.
        :param plate_number: Plate number of the vehicle.
        :param license_number: License number of the vehicle.
        :return: Dictionary containing vehicle information if registration is successful, otherwise an empty dictionary.
        """
        user = await DriverDomain.load(user_id)
        vehicle_info = await user.register_vehicle_data(
            plate_number=plate_number,
            license_number=license_number,
        )
        return {
            "vehicle_id": vehicle_info["vehicle_id"],
            "plate_number": vehicle_info["plate_number"],
            "license_number": vehicle_info["license_number"],
        } if vehicle_info else {}

    @staticmethod
    async def get_vehicle_info(user_id: str) -> Dict[str, Any]:
        """
        Retrieves vehicle information for the user.

        :param user_id: ID of the user.
        :return: Dictionary containing vehicle information if available, otherwise an empty dictionary.
        """
        user = await DriverDomain.load(user_id)
        vehicle_info = await user.get_vehicle_info(user_id=user_id)
        return {
            "vehicle_id": vehicle_info["vehicle_id"],
            "plate_number": vehicle_info["plate_number"],
            "license_number": vehicle_info["license_number"],
        } if vehicle_info else {}
