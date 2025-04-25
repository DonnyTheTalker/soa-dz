import pytest
import requests
import logging

API_URL = "http://api:5000"

def setup_module():
    import time
    time.sleep(5)


def test_like_post():
    response = requests.post(
        f"{API_URL}/register",
        json={'username': 'test_like_post', "email": "testuser@example.com", "password": "goodPassword1"},
    )
    assert response.status_code == 200

    response = requests.post(
        f"{API_URL}/like_post", json={'username': 'test_like_post', 'password': 'goodPassword'}
    )
    assert response.status_code == 401
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Invalid credentials"

    response = requests.post(
        f"{API_URL}/like_post",
        json={
            'username': 'test_like_post',
            'password': 'goodPassword1',
            'id': 10000000
        },
    )
    assert response.status_code == 404
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Post not found or access denied"

    response = requests.post(
        f"{API_URL}/create_post",
        json={
            'username': 'test_like_post',
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
            'username': 'test_like_post',
            'password': 'goodPassword1',
            'id': post_id,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "Post liked"

    response = requests.post(
        f"{API_URL}/like_post",
        json={
            'username': 'test_like_post',
            'password': 'goodPassword1',
            'id': post_id,
        },
    )
    assert response.status_code == 404
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Post already liked"

    response = requests.post(
        f"{API_URL}/create_post",
        json={
            'username': 'test_like_post',
            'password': 'goodPassword1',
            'title': 'Test title',
            'description': 'Test description',
            'tags': ['tag1', 'tag2'],
            'is_private': True
        },
    )
    assert response.status_code == 200
    data = response.json()
    post_id = data['post']['id']

    response = requests.post(
        f"{API_URL}/register",
        json={'username': 'test_like_post_2', "email": "testuser@example.com", "password": "goodPassword1"},
    )
    assert response.status_code == 200

    response = requests.post(
        f"{API_URL}/like_post",
        json={
            'username': 'test_like_post_2',
            'password': 'goodPassword1',
            'id': post_id
        },
    )
    assert response.status_code == 404
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Post not found or access denied"


def test_unlike_post():
    response = requests.post(
        f"{API_URL}/register",
        json={'username': 'test_unlike_post', "email": "testuser@example.com", "password": "goodPassword1"},
    )
    assert response.status_code == 200

    response = requests.post(
        f"{API_URL}/unlike_post", json={'username': 'test_unlike_post', 'password': 'goodPassword'}
    )
    assert response.status_code == 401
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Invalid credentials"

    response = requests.post(
        f"{API_URL}/unlike_post",
        json={
            'username': 'test_unlike_post',
            'password': 'goodPassword1',
            'id': 10000000
        },
    )
    assert response.status_code == 404
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Post not found or access denied"

    response = requests.post(
        f"{API_URL}/create_post",
        json={
            'username': 'test_unlike_post',
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
        f"{API_URL}/unlike_post",
        json={
            'username': 'test_unlike_post',
            'password': 'goodPassword1',
            'id': post_id,
        },
    )
    assert response.status_code == 404
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Post not liked"

    response = requests.post(
        f"{API_URL}/like_post",
        json={
            'username': 'test_unlike_post',
            'password': 'goodPassword1',
            'id': post_id,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "Post liked"

    response = requests.post(
        f"{API_URL}/unlike_post",
        json={
            'username': 'test_unlike_post',
            'password': 'goodPassword1',
            'id': post_id,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "Post unliked"

    response = requests.post(
        f"{API_URL}/unlike_post",
        json={
            'username': 'test_unlike_post',
            'password': 'goodPassword1',
            'id': post_id,
        },
    )
    assert response.status_code == 404
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Post not liked"

    response = requests.post(
        f"{API_URL}/create_post",
        json={
            'username': 'test_unlike_post',
            'password': 'goodPassword1',
            'title': 'Test title',
            'description': 'Test description',
            'tags': ['tag1', 'tag2'],
            'is_private': True
        },
    )
    assert response.status_code == 200
    data = response.json()
    post_id = data['post']['id']

    response = requests.post(
        f"{API_URL}/register",
        json={'username': 'test_unlike_post_2', "email": "testuser@example.com", "password": "goodPassword1"},
    )
    assert response.status_code == 200

    response = requests.post(
        f"{API_URL}/unlike_post",
        json={
            'username': 'test_unlike_post_2',
            'password': 'goodPassword1',
            'id': post_id
        },
    )
    assert response.status_code == 404
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Post not found or access denied"


def test_leave_comment():
    response = requests.post(
        f"{API_URL}/register",
        json={'username': 'test_leave_comment', "email": "testuser@example.com", "password": "goodPassword1"},
    )
    assert response.status_code == 200

    response = requests.post(
        f"{API_URL}/comment_post", json={'username': 'test_leave_comment', 'password': 'goodPassword'}
    )
    assert response.status_code == 401
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Invalid credentials"

    response = requests.post(
        f"{API_URL}/comment_post",
        json={
            'username': 'test_leave_comment',
            'password': 'goodPassword1',
            'id': 10000000,
            'comment': 'Test comment'
        },
    )
    assert response.status_code == 404
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Post not found or access denied"

    response = requests.post(
        f"{API_URL}/create_post",
        json={
            'username': 'test_leave_comment',
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
            'username': 'test_leave_comment',
            'password': 'goodPassword1',
            'id': post_id,
            'comment': 'Test comment'
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "Comment left"

    response = requests.post(
        f"{API_URL}/comment_post",
        json={
            'username': 'test_leave_comment',
            'password': 'goodPassword1',
            'id': post_id,
            'comment': 'Test comment 2'
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "Comment left"

    response = requests.get(
        f"{API_URL}/list_comments",
        json={
            'username': 'test_leave_comment',
            'password': 'goodPassword1',
            "id": post_id,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['comments']) == 2
    assert data['comments'][0]['text'] == 'Test comment'
    assert data['comments'][1]['text'] == 'Test comment 2'
