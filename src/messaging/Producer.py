from confluent_kafka import Producer as KafkaProducer
from config import config
import abc


class Producer:
    def __init__(self, topic):
        self.topic = topic
        self.kafka_producer = KafkaProducer(config["kafka"]["conf"])

    def send(self, key=None, value=None):
        self.kafka_producer.poll(0)
        self.kafka_producer.produce(self.topic, key=key, value=value)

    @abc.abstractmethod
    def produce(self, *values):
        pass
