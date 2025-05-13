from typing import Any
from elastic_transport import ObjectApiResponse
from elasticsearch import Elasticsearch
from config import ELASTIC_HOST


class BaseElasticClient:
    def __init__(self, index_name: str, host: str = ELASTIC_HOST):
        """
        Initialize the Elasticsearch client with a specific index.
        """
        self.client = Elasticsearch(
            host,
        )
        self.index_name = index_name

    def index_document(self, doc_id: int, body: dict) -> ObjectApiResponse[Any]:
        """
        Index or update a document in Elasticsearch.
        """
        self.client.index(index=self.index_name, id=doc_id, body=body)

    def delete_document(self, doc_id: int) -> ObjectApiResponse[Any]:
        """
        Delete a document from Elasticsearch.
        """
        self.client.delete(index=self.index_name, id=doc_id)

    def search_documents(self, body: dict) -> ObjectApiResponse[Any]:
        """
        Search for documents in Elasticsearch.
        """
        return self.client.search(index=self.index_name, body=body)
