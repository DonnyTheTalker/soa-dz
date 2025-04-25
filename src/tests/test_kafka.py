import pytest
import requests
import logging
import time
import json
from kafka import KafkaConsumer

API_URL = "http://api:5000"

def setup_module():
    import time
    time.sleep(5)

def wait_for_event(consumer, event_type, user_id):
    for _ in range(10):
        for msg in consumer.poll(timeout_ms=1000).values():
            for record in msg:
                data = json.loads(record.value)
                if data['event_type'] == event_type and data['client_id'] == user_id:
                    return data
            time.sleep(1)
    return None


def test_kafka_register_user():
    consumer = KafkaConsumer(
        "user-registration",
        bootstrap_servers="kafka:9092",
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        group_id='test-group'
    )

    response = requests.post(
        f"{API_URL}/register",
        json={'username': 'test_kafka_register_user', "email": "testuser@example.com", "password": "goodPassword1"},
    )
    assert response.status_code == 200
    assert wait_for_event(consumer, "REGISTRATION", "test_kafka_register_user") is not None
    consumer.close()


def test_kafka_like_post():
    consumer = KafkaConsumer(
        "content-likes",
        bootstrap_servers="kafka:9092",
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        group_id='test-group'
    )

    response = requests.post(
        f"{API_URL}/register",
        json={'username': 'test_kafka_like_post', "email": "testuser@example.com", "password": "goodPassword1"},
    )
    assert response.status_code == 200

    response = requests.post(
        f"{API_URL}/create_post",
        json={
            'username': 'test_kafka_like_post',
            'password': 'goodPassword1',
            'title': 'Test title',
            'description': 'Test description',
            'tags': ['tag1', 'tag2'],
        },
    )
    assert response.status_code == 200
    data = response.json()
    post_id = data['post']['id']

    response = requests.post(
        f"{API_URL}/like_post",
        json={
            'username': 'test_kafka_like_post',
            'password': 'goodPassword1',
            'id': post_id,
        },
    )
    assert response.status_code == 200

    event = wait_for_event(consumer, "LIKE", "test_kafka_like_post")
    assert event is not None
    assert event["entity_id"] == post_id
    assert event["entity_type"] == "post"

    response = requests.post(
        f"{API_URL}/unlike_post",
        json={
            'username': 'test_kafka_like_post',
            'password': 'goodPassword1',
            'id': post_id,
        },
    )
    assert response.status_code == 200

    event = wait_for_event(consumer, "UNLIKE", "test_kafka_like_post")
    assert event is not None
    assert event["entity_id"] == post_id
    assert event["entity_type"] == "post"

    consumer.close()

def test_kafka_comment_post():
    consumer = KafkaConsumer(
        "content-comments",
        bootstrap_servers="kafka:9092",
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        group_id='test-group'
    )

    response = requests.post(
        f"{API_URL}/register",
        json={'username': 'test_kafka_comment_post', "email": "testuser@example.com", "password": "goodPassword1"},
    )
    assert response.status_code == 200

    response = requests.post(
        f"{API_URL}/create_post",
        json={
            'username': 'test_kafka_comment_post',
            'password': 'goodPassword1',
            'title': 'Test title',
            'description': 'Test description',
            'tags': ['tag1', 'tag2'],
        },
    )
    assert response.status_code == 200
    data = response.json()
    post_id = data['post']['id']

    response = requests.post(
        f"{API_URL}/comment_post",
        json={
            'username': 'test_kafka_comment_post',
            'password': 'goodPassword1',
            'id': post_id,
            'comment': 'Test comment'
        },
    )
    assert response.status_code == 200

    event = wait_for_event(consumer, "COMMENT", "test_kafka_comment_post")
    assert event is not None
    assert event["entity_id"] == post_id
    assert event["entity_type"] == "post"


def test_kafka_view_post():
    consumer = KafkaConsumer(
        "content-views",
        bootstrap_servers="kafka:9092",
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        group_id='test-group'
    )

    response = requests.post(
        f"{API_URL}/register",
        json={'username': 'test_kafka_view_post', "email": "testuser@example.com", "password": "goodPassword1"},
    )
    assert response.status_code == 200

    response = requests.post(
        f"{API_URL}/create_post",
        json={
            'username': 'test_kafka_view_post',
            'password': 'goodPassword1',
            'title': 'Test title',
            'description': 'Test description',
            'tags': ['tag1', 'tag2'],
        },
    )
    assert response.status_code == 200
    data = response.json()
    post_id = data['post']['id']

    response = requests.get(
        f"{API_URL}/get_post",
        json={
            'username': 'test_kafka_view_post',
            'password': 'goodPassword1',
            'id': post_id,
        },
    )
    assert response.status_code == 200

    event = wait_for_event(consumer, "VIEW", "test_kafka_view_post")
    assert event is not None
    assert event["entity_id"] == post_id
    assert event["entity_type"] == "post"

    consumer.close()


def test_kafka_list_posts():
    consumer = KafkaConsumer(
        "content-views",
        bootstrap_servers="kafka:9092",
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        group_id='test-group'
    )

    response = requests.post(
        f"{API_URL}/register",
        json={'username': 'test_kafka_list_posts', "email": "testuser@example.com", "password": "goodPassword1"},
    )
    assert response.status_code == 200

    response = requests.post(
        f"{API_URL}/create_post",
        json={
            'username': 'test_kafka_list_posts',
            'password': 'goodPassword1',
            'title': 'Test title',
            'description': 'Test description',
            'tags': ['tag1', 'tag2'],
        },
    )
    assert response.status_code == 200
    data = response.json()
    post_id = data['post']['id']

    response = requests.get(
        f"{API_URL}/list_posts",
        json={
            'username': 'test_kafka_list_posts',
            'password': 'goodPassword1',
            'author': 'test_kafka_list_posts',
        },
    )
    assert response.status_code == 200

    event = wait_for_event(consumer, "VIEW", "test_kafka_list_posts")
    assert event is not None
    assert event["entity_id"] == post_id
    assert event["entity_type"] == "post"
    
    consumer.close()
