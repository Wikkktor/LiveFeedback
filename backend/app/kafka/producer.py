from confluent_kafka import Producer
import json

from schemas.feedback import FeedbackInDB
from app.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC


producer_config: dict[str, str] = {"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS}

producer: Producer = Producer(producer_config)


def delivery_report(err, msg) -> None:
    if err:
        print(f"[Kafka Producer] Delivery failed: {err}")
    else:
        print(
            f"[Kafka Producer] Message delivered to {msg.topic()} [{msg.partition()}]"
        )


def send_feedback(feedback: FeedbackInDB) -> None:
    producer.produce(
        KAFKA_TOPIC, value=feedback.model_dump_json(), callback=delivery_report
    )
    producer.flush()
