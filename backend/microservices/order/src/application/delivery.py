from typing import Dict, Any, List, Optional
from ftgo_utils.enums import DeliveryStatus
from domain.delivery import DeliveryHandler

class DeliveryService:
    @staticmethod
    async def schedule_delivery(
        order_id: str,
        driver_id: str,
        source_address_id: str,
        destination_address_id: str,
        **kwargs,
    ) -> Dict[str, Any]:
        return await DeliveryHandler.schedule_delivery(
            order_id=order_id,
            driver_id=driver_id,
            source_address_id=source_address_id,
            destination_address_id=destination_address_id,
            **kwargs
        )

    @staticmethod
    async def update_delivery_status(delivery_id: str, status: DeliveryStatus, **kwargs) -> Dict[str, Any]:
        return await DeliveryHandler.update_delivery_status(delivery_id, status, **kwargs)

    @staticmethod
    async def get_delivery_details(delivery_id: str, **kwargs) -> Dict[str, Any]:
        return await DeliveryHandler.get_delivery_details(delivery_id, **kwargs)

    @staticmethod
    async def assign_driver_to_delivery(driver_id: str, delivery_id: str, **kwargs) -> Dict[str, Any]:
        return await DeliveryHandler.assign_driver_to_order(driver_id, delivery_id, **kwargs)
