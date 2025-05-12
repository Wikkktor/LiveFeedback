from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class FeedbackBase(BaseModel):
    user_id: int
    product_id: int
    rating: int
    comment: Optional[str] = None


class FeedbackCreate(FeedbackBase): ...


# Properties to receive via API on update
class FeedbackUpdate(FeedbackBase): ...


# Additional properties stored in DB but not returned by API
class FeedbackInDB(FeedbackBase):
    id: int

    date_created: datetime

    class Config:
        from_attributes = True


class FeedBackElasticSearch(FeedbackBase):
    date_created: datetime

    class Config:
        from_attributes = True
