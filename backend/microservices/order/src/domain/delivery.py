from typing import Dict, Any
from domain.entities.delivery import Delivery
from ftgo_utils.enums import DeliveryStatus
from ftgo_utils.errors import ErrorCodes, BaseError
from domain import get_logger
from utils import handle_exception

class DeliveryHandler:
    @staticmethod
    async def schedule_delivery(
        order_id: str,
        driver_id: str,
        source_address_id: str,
        destination_address_id: str,
        **kwargs,
    ) -> Dict[str, Any]:
        try:
            delivery = Delivery.create(
                order_id=order_id,
                driver_id=driver_id,
                source_address_id=source_address_id,
                destination_address_id=destination_address_id
            )
            await delivery.save()
            return delivery.document.dict()
        except Exception as e:
            get_logger().error(ErrorCodes.SCHEDULE_DELIVERY_ERROR.value, payload={"order_id": order_id})
            await handle_exception(e, error_code=ErrorCodes.SCHEDULE_DELIVERY_ERROR, payload={"order_id": order_id})

    @staticmethod
    async def update_delivery_status(delivery_id: str, status: DeliveryStatus, **kwargs) -> Dict[str, Any]:
        try:
            delivery = await DeliveryHandler.load_delivery(delivery_id)
            await delivery.update_status(status)
            return delivery.document.dict()
        except Exception as e:
            payload = {"delivery_id": delivery_id, "status": status.value}
            get_logger().error(ErrorCodes.UPDATE_DELIVERY_STATUS_ERROR.value, payload=payload)
            await handle_exception(e, error_code=ErrorCodes.UPDATE_DELIVERY_STATUS_ERROR, payload=payload)

    @staticmethod
    async def get_delivery_details(delivery_id: str, **kwargs) -> Dict[str, Any]:
        delivery = await DeliveryHandler.load_delivery(delivery_id)
        return delivery.document.dict()

    @staticmethod
    async def load_delivery(delivery_id: str) -> Delivery:
        delivery_doc = await Delivery.load(id=delivery_id)
        if not delivery_doc:
            raise BaseError(error_code=ErrorCodes.DELIVERY_NOT_FOUND_ERROR, payload={"delivery_id": delivery_id})
        return delivery_doc

    @staticmethod
    async def assign_driver_to_order(driver_id: str, delivery_id: str) -> Dict[str, Any]:
        delivery = await DeliveryHandler.load_delivery(delivery_id)
        await delivery.assign_driver(driver_id)
        await delivery.save()

        return {
            "delivery": delivery.document.dict(),
        }
