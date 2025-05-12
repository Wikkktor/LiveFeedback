import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC: str = os.getenv("KAFKA_TOPIC", "feedback-topic")

ELASTIC_HOST: str = os.getenv("ELASTIC_HOST", "http://localhost:9200")
ELASTIC_INDEX: str = os.getenv("ELASTIC_INDEX", "feedback-index")
