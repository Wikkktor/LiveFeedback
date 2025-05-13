from elastic import BaseElasticClient
from schemas.feedback import FeedBackElasticSearch


class FeedbackElasticClient(BaseElasticClient):
    def __init__(self):
        """
        Initialize the Feedback Elasticsearch client.
        """
        super().__init__(index_name="feedback-index")

    def index_document(self, feedback: FeedBackElasticSearch):
        """
        Index or update a feedback document.
        """
        return super().index_document(
            doc_id=feedback.id, body=feedback.model_dump_json()
        )

    def delete_document(self, feedback_id: int):
        """
        Delete a feedback document.
        """
        return super().delete_document(doc_id=feedback_id)
