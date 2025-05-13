from elastic.client import BaseElasticClient
from schemas.product import ProductElasticSearch


class ProductElasticClient(BaseElasticClient):
    def __init__(self):
        """
        Initialize the Product Elasticsearch client.
        """
        super().__init__(index="product-index")

    def index_document(self, product: ProductElasticSearch):
        """
        Index or update a product document.
        """
        return super().index_document(doc_id=product.id, body=product.model_dump_json())

    def delete_document(self, product_id: int):
        """
        Delete a product document.
        """
        return super().delete_document(doc_id=product_id)
