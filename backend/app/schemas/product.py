from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime
from slugify import slugify


class ProductBase(BaseModel):
    name: str
    slug: Optional[str] = Field(default=None)
    price: float
    description: Optional[str]


class ProductCreate(ProductBase):
    def __init__(self, **data):
        super().__init__(**data)
        if not self.slug:
            self.slug = slugify(self.name)


# Properties to receive via API on update
class ProductUpdate(ProductBase):
    def __init__(self, **data):
        super().__init__(**data)
        if not self.slug:
            self.slug = slugify(self.name)


# Additional properties stored in DB but not returned by API
class ProductInDB(ProductBase):
    id: int

    date_created: datetime

    class Config:
        from_attributes = True


class ProductElasticSearch(ProductBase):
    date_created: datetime

    class Config:
        from_attributes = True
