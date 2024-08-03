from datetime import datetime
from domain.entities.base import BaseEntity
from models.order_rating import OrderRating as OrderRatingDocument
from typing import Optional

class OrderRating(BaseEntity):
    document_cls = OrderRatingDocument

    def __init__(self, document: OrderRatingDocument):
        super().__init__(document)

    @classmethod
    def create(cls, order_id: str, customer_id: str, rating: int, feedback: Optional[str] = None) -> "OrderRating":
        order_rating_doc = OrderRatingDocument(
            order_id=order_id,
            customer_id=customer_id,
            rating=rating,
            feedback=feedback,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        return cls(document=order_rating_doc)

    async def save(self):
        await super().save()

    async def update_rating(self, rating: int, feedback: Optional[str] = None):
        await self.update(rating=rating, feedback=feedback, updated_at=datetime.utcnow())
