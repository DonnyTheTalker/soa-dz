import json
import uuid
from datetime import datetime
from kafka import KafkaProducer
import os

KAFKA_PORT = os.environ.get('KAFKA_PORT', 9092)

class UserEventProducer:
    def __init__(self):
        bootstrap_servers = [f'kafka:{KAFKA_PORT}']
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: str(k).encode('utf-8')
        )

    def send_registration_event(self, user_id):
        event = {
            'event_id': str(uuid.uuid4()),
            'event_type': 'REGISTRATION',
            'client_id': user_id,
            'timestamp': datetime.now().isoformat()
        }
        self.producer.send('user-registration', key=user_id, value=event)
