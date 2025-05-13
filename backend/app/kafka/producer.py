from typing import Any, Literal
import json

from confluent_kafka import Producer
from config import KAFKA_BOOTSTRAP_SERVERS

producer_config: dict[str, str] = {"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS}
producer: Producer = Producer(producer_config)


def delivery_report(err, msg) -> None:
    if err:
        print(f"[Kafka Producer] Delivery failed: {err}")
    else:
        print(
            f"[Kafka Producer] Message delivered to {msg.topic()} [{msg.partition()}]"
        )


def send_to_kafka(
    model_type: str,
    action: Literal["create", "update", "delete"],
    payload: dict[str, Any],
) -> None:
    """
    Send a message to Kafka.
    Args:
        model_type (str): The type of model (e.g., "feedback", "product").
        action (Literal["create", "update", "delete"]): The action performed.
        payload (dict[str, Any]): The data to send.
    """

    message: dict[str, Any] = {
        "model": model_type,
        "action": action,
        "payload": payload,
    }
    producer.produce(
        topic=f"{model_type}-topic",  # Each model can have a dedicated topic
        value=json.dumps(message, default=str),
        callback=delivery_report,
    )
    producer.flush()
