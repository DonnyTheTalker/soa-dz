import json
import uuid
from datetime import datetime
from kafka import KafkaProducer
import os

KAFKA_PORT = os.environ.get('KAFKA_PORT', 9092)

class PostsEventProducer:
    def __init__(self):
        bootstrap_servers = [f'kafka:{KAFKA_PORT}']
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: str(k).encode('utf-8')
        )

    def send_view_event(self, client_id, entity_type, entity_id):
        event = {
            'event_id': str(uuid.uuid4()),
            'event_type': 'VIEW',
            'client_id': client_id,
            'timestamp': datetime.now().isoformat(),
            'entity_type': entity_type,
            'entity_id': entity_id
        }
        self.producer.send('content-views', key=client_id, value=event)

    def send_like_event(self, client_id, entity_type, entity_id):
        event = {
            'event_id': str(uuid.uuid4()),
            'event_type': 'LIKE',
            'client_id': client_id,
            'timestamp': datetime.now().isoformat(),
            'entity_type': entity_type,
            'entity_id': entity_id
        }
        self.producer.send('content-likes', key=client_id, value=event)

    def send_unlike_event(self, client_id, entity_type, entity_id):
        event = {
            'event_id': str(uuid.uuid4()),
            'event_type': 'UNLIKE',
            'client_id': client_id,
            'timestamp': datetime.now().isoformat(),
            'entity_type': entity_type,
            'entity_id': entity_id
        }
        self.producer.send('content-likes', key=client_id, value=event)

    def send_comment_event(self, client_id, entity_type, entity_id):
        event = {
            'event_id': str(uuid.uuid4()),
            'event_type': 'COMMENT',
            'client_id': client_id,
            'timestamp': datetime.now().isoformat(),
            'entity_type': entity_type,
            'entity_id': entity_id
        }
        self.producer.send('content-comments', key=client_id, value=event)
