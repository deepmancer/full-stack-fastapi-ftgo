from datetime import datetime
from domain.entities.base import BaseEntity
from models.delivery_rating import DeliveryRating as DeliveryRatingDocument
from typing import Optional
class DeliveryRating(BaseEntity):
    document_cls = DeliveryRatingDocument

    def __init__(self, document: DeliveryRatingDocument):
        super().__init__(document)

    @classmethod
    def create(cls, delivery_id: str, order_id: str, customer_id: str, rating: int, feedback: Optional[str] = None, driver_id: Optional[str] = None) -> "DeliveryRating":
        delivery_rating_doc = DeliveryRatingDocument(
            delivery_id=delivery_id,
            order_id=order_id,
            customer_id=customer_id,
            driver_id=driver_id,
            rating=rating,
            feedback=feedback,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        return cls(document=delivery_rating_doc)

    async def save(self):
        await super().save()

    async def update_rating(self, rating: int, feedback: Optional[str] = None):
        await self.update(rating=rating, feedback=feedback, updated_at=datetime.utcnow())
