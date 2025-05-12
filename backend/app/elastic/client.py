from elasticsearch import Elasticsearch
from app.config import ELASTIC_HOST
from schemas.feedback import FeedBackElasticSearch
from schemas.product import ProductElasticSearch

es: Elasticsearch = Elasticsearch(ELASTIC_HOST)


def index_feedback(feedback: FeedBackElasticSearch):
    es.index(index="feedback-index", id=feedback.id, body=feedback.model_dump_json())


def index_product(product: ProductElasticSearch):
    es.index(index="product-index", id=product.id, body=product.model_dump_json())
