import json
import threading
from typing import Any, Type
from confluent_kafka import Consumer, KafkaError, KafkaException

from core.logger import logger
from config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_GROUP_ID
from elastic import (
    BaseElasticClient,
    FeedbackElasticClient,
    ProductElasticClient,
)


class KafkaConsumerService:
    def __init__(self):
        self.running: bool = False
        self.thread: threading.Thread | None = None
        self.elastic_clients: dict[str, Type[BaseElasticClient]] = {
            "feedback": FeedbackElasticClient,
            "product": ProductElasticClient,
        }

    def _initialize_consumer(self) -> Consumer:
        """Initialize and configure the Kafka consumer."""
        consumer_config: dict[str, str] = {
            "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
            "group.id": KAFKA_GROUP_ID,
            "auto.offset.reset": "earliest",
        }
        return Consumer(consumer_config)

    def _process_message(self, message: dict) -> None:
        """Process a single Kafka message."""
        try:
            model_type: str = message["model"]
            action: str = message["action"]
            payload: dict[str, Any] = message["payload"]

            if client_class := self.elastic_clients.get(model_type):
                client_instance: BaseElasticClient = client_class()
                if action in {"create", "update"}:
                    client_instance.index_document(doc_id=payload["id"], body=payload)
                    logger.info(
                        f"[Elasticsearch] {model_type} {action}: {payload['id']}"
                    )
                elif action == "delete":
                    client_instance.delete_document(payload["id"])
                    logger.info(
                        f"[Elasticsearch] {model_type} deleted: {payload['id']}"
                    )
                else:
                    logger.warning(f"[Kafka] Unknown action: {action}")
            else:
                logger.warning(f"[Kafka] Unknown model type: {model_type}")
        except KeyError as e:
            logger.error(f"[Kafka Consumer] Missing key in message: {e}")
        except Exception as e:
            logger.error(f"[Kafka Consumer] Error processing message: {e}")

    def _consume(self):
        """Consume messages from Kafka and process them."""
        consumer = self._initialize_consumer()
        consumer.subscribe(["feedback-topic", "product-topic"])
        logger.info("[Kafka Consumer] Started in background")

        try:
            while self.running:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        logger.debug("[Kafka Consumer] Reached end of partition")
                    else:
                        logger.error(f"[Kafka Error] {msg.error()}")
                        raise KafkaException(msg.error())
                else:
                    try:
                        message_data = json.loads(msg.value().decode("utf-8"))
                        self._process_message(message_data)
                    except json.JSONDecodeError as e:
                        logger.error(f"[Kafka Consumer] Invalid JSON: {e}")
        except KafkaException as e:
            logger.error(f"[Kafka Consumer] Kafka exception: {e}")
        except Exception as e:
            logger.error(f"[Kafka Consumer Error] {e}")
        finally:
            consumer.close()
            logger.info("[Kafka Consumer] Stopped")

    def start(self):
        """Start the Kafka consumer in a background thread."""
        if self.running:
            logger.warning("[Kafka Consumer] Already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._consume, daemon=True)
        self.thread.start()
        logger.info("[Kafka Consumer] Service started")

    def stop(self):
        """Stop the Kafka consumer and wait for the thread to finish."""
        if not self.running:
            logger.warning("[Kafka Consumer] Not running")
            return

        self.running = False
        if self.thread:
            self.thread.join()
            logger.info("[Kafka Consumer] Service stopped")
