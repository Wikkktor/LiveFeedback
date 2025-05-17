from typing import Any
from elastic.client import BaseElasticClient


class ProductElasticClient(BaseElasticClient):
    def __init__(self):
        """
        Initialize the Product Elasticsearch client.
        """
        super().__init__(index_name="product-index")

    def index_document(self, product: dict[str, Any]):
        """
        Index or update a product document.
        """
        return super().index_document(doc_id=product["id"], body=product)

    def delete_document(self, product_id: int):
        """
        Delete a product document.
        """
        return super().delete_document(doc_id=product_id)
