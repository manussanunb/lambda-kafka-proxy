import dacite
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional
from confluent_kafka import KafkaException, Producer

class DataClassMixin:
    @classmethod
    def from_dict(cls, cfg_dict: Dict[Any, Any]):
        return dacite.from_dict(cls, cfg_dict)


@dataclass
class KafkaProducerConfig(DataClassMixin):
    bootstrap_servers: str
    topic: str
    sasl_username: str
    sasl_password: str
    retries: Optional[int] = 1
    compression: Optional[str] = "none"
    acks: Optional[int] = -1
    timeout: Optional[int] = 30000


class KafkaProducerClient:
    def __init__(self, config: Dict):
        self.config = KafkaProducerConfig.from_dict(config)
        self.producer = self._init_client()

    def _init_client(self):
        return Producer(
            {
                "bootstrap.servers": self.config.bootstrap_servers,
                "retries": self.config.retries,
                "security.protocol": "SASL_SSL",
                "sasl.mechanism": "SCRAM-SHA-512",
                "sasl.username": self.config.sasl_username,
                "sasl.password": self.config.sasl_password,
                "acks": self.config.acks,
                "request.timeout.ms": self.config.timeout,
                "compression.type": self.config.compression,
            }
        )

    @staticmethod
    def callback(err, event):
        if err:
            print(err)
            print(f"Produce to topic {event.topic()} failed")
            raise Exception(err)

    def send_message(self, message: str, key: Optional[str] = None):
        try:
            print(f"Start send message:{message}")
            self.producer.produce(self.config.topic, message, key, on_delivery=self.callback)
            self.producer.flush()
            print("Send message: Success")
        except KafkaException as e:
            print("Send message: Fail")
            raise e
