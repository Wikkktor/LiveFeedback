import time
from elasticsearch import Elasticsearch
from config import ELASTIC_HOST


def ensure_indices_exist() -> None:
    """
    Ensure that the required Elasticsearch indices exist.
    If they do not exist, create them.
    """
    es = None
    for _ in range(30):  # Try for up to ~30 seconds
        try:
            es: Elasticsearch = Elasticsearch(ELASTIC_HOST)
            if es.ping():
                break
        except Exception:
            pass
        time.sleep(1)
    else:
        raise RuntimeError("Elasticsearch is not available after waiting.")

    for index in ["feedback-index", "product-index"]:
        print(f"Checking if index {index} exists...")
        if not es.indices.exists(index=index):
            es.indices.create(index=index)
