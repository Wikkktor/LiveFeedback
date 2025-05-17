from typing import Any
from elastic import BaseElasticClient


class FeedbackElasticClient(BaseElasticClient):
    def __init__(self):
        """
        Initialize the Feedback Elasticsearch client.
        """
        super().__init__(index_name="feedback-index")

    def index_document(self, feedback: dict[str, Any]):
        """
        Index or update a product document.
        """
        return super().index_document(doc_id=feedback["id"], body=feedback)

    def delete_document(self, feedback_id: int):
        """
        Delete a feedback document.
        """
        return super().delete_document(doc_id=feedback_id)
