from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import Product
from schemas.product import ProductCreate, ProductUpdate, ProductElasticSearch
from elastic import ProductElasticClient
from kafka.producer import send_to_kafka


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def search(self, q: str | None = None) -> list[Product]:
        """Search for Product by query."""
        # Create some query for elastic search with fuzzy search
        query = (
            {
                "query": {
                    "multi_match": {
                        "query": q,
                        "fields": ["comment"],  # Adjust fields as needed
                        "fuzziness": "AUTO",
                    }
                }
            }
            if q
            else {}
        )
        results = ProductElasticClient().search_documents(query=query)
        print(results)
        return [hit["_source"] for hit in results["hits"]["hits"]]

    def create(self, db: Session, *, obj_in: ProductCreate) -> Product:
        """Create a new Product."""
        product_db: Product = super().create(db=db, obj_in=obj_in)
        send_to_kafka(
            model_type=self.model_name,
            action="create",
            payload=ProductElasticSearch.model_validate(
                product_db, from_attributes=True
            ).model_dump(),
        )
        return product_db

    def update(
        self,
        db: Session,
        *,
        product_id: int,
        obj_in: ProductUpdate,
    ) -> Product:
        """Update a Product."""
        db_obj: Product = self.get_or_404(db=db, id=product_id)
        product_db: Product = super().update(db=db, db_obj=db_obj, obj_in=obj_in)
        send_to_kafka(
            model_type=self.model_name,
            action="update",
            payload=ProductElasticSearch.model_validate(
                product_db, from_attributes=True
            ).model_dump(),
        )
        return product_db

    def remove(self, db: Session, *, product_id: int) -> Product:
        """Remove a Product."""
        product_db: Product = self.get_or_404(db=db, id=product_id)
        db.delete(product_db)
        db.commit()
        send_to_kafka(
            model_type=self.model_name,
            action="delete",
            payload=ProductElasticSearch.model_validate(
                product_db, from_attributes=True
            ).model_dump(),
        )
        return product_db


crud_product: CRUDProduct = CRUDProduct(Product)
