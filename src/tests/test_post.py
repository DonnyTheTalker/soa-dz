import pytest
import requests

API_URL = "http://api:5000"


@pytest.fixture(autouse=True)
def test_setup():
    import time

    time.sleep(3)


def test_create_post():
    response = requests.post(
        f"{API_URL}/register",
        json={'username': 'test_create_post', "email": "testuser@example.com", "password": "goodPassword1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "User created"

    response = requests.post(
        f"{API_URL}/create_post", json={'username': 'test_create_post', 'password': 'goodPassword'}
    )
    assert response.status_code == 401
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Invalid credentials"

    response = requests.post(
        f"{API_URL}/create_post",
        json={
            'username': 'test_create_post',
            'password': 'goodPassword1',
            'title': 'Test title',
            'description': 'Test description',
            'tags': ['tag1', 'tag2'],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "Post created"
    assert data['post']['title'] == 'Test title'
    assert data['post']['description'] == 'Test description'
    assert data['post']['tags'] == ['tag1', 'tag2']
    assert data['post']['creatorId'] == 'test_create_post'

    old_id = data['post']['id']

    response = requests.post(
        f"{API_URL}/create_post",
        json={
            'username': 'test_create_post',
            'password': 'goodPassword1',
            'title': 'Test title 2',
            'description': 'Test description 2',
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "Post created"
    assert data['post']['title'] == 'Test title 2'
    assert data['post']['description'] == 'Test description 2'
    assert data['post'].get("tags", []) == []
    assert data['post']['creatorId'] == 'test_create_post'
    assert data['post']['id'] != old_id


def test_delete_post():
    response = requests.post(
        f"{API_URL}/register",
        json={'username': 'test_delete_post', "email": "testuser@example.com", "password": "goodPassword1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "User created"

    response = requests.post(
        f"{API_URL}/create_post",
        json={
            'username': 'test_delete_post',
            'password': 'goodPassword1',
            'title': 'Test title',
            'description': 'Test description',
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "Post created"
    post_id = data['post']['id']

    response = requests.delete(
        f"{API_URL}/delete_post",
        json={
            'username': 'test_delete_post',
            'password': 'goodPassword1',
            'id': post_id,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "Post deleted"

    response = requests.delete(
        f"{API_URL}/delete_post",
        json={
            'username': 'test_delete_post',
            'password': 'goodPassword1',
            'id': post_id,
        },
    )
    assert response.status_code == 404
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Post not found or access denied"


def test_get_post():
    response = requests.post(
        f"{API_URL}/register",
        json={'username': 'test_get_post', "email": "testuser@example.com", "password": "goodPassword1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "User created"

    response = requests.post(
        f"{API_URL}/create_post",
        json={
            'username': 'test_get_post',
            'password': 'goodPassword1',
            'title': 'Test title',
            'description': 'Test description',
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "Post created"
    post_id = data['post']['id']

    response = requests.get(f"{API_URL}/get_post", json={'username': 'test_get_post', 'password': 'goodPassword1'})
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Missing fields"

    response = requests.get(
        f"{API_URL}/get_post", json={'username': 'test_get_post', 'password': 'goodPassword1', 'id': post_id}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "Post found"
    assert data['post']['id'] == post_id
    assert data['post']['title'] == 'Test title'
    assert data['post']['description'] == 'Test description'

    invalid_id = 1000000
    response = requests.get(
        f"{API_URL}/get_post", json={'username': 'test_get_post', 'password': 'goodPassword1', 'id': invalid_id}
    )
    assert response.status_code == 404
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Post not found or access denied"


def test_get_private_post():
    response = requests.post(
        f"{API_URL}/register",
        json={'username': 'test_get_private_post', "email": "testuser@example.com", "password": "goodPassword1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "User created"

    response = requests.post(
        f"{API_URL}/create_post",
        json={
            'username': 'test_get_private_post',
            'password': 'goodPassword1',
            'title': 'Test title',
            'description': 'Test description',
            "is_private": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "Post created"
    assert data['post']['isPrivate'] is True
    post_id = data['post']['id']

    response = requests.get(
        f"{API_URL}/get_post", json={'username': 'test_get_private_post', 'password': 'goodPassword1', 'id': post_id}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "Post found"
    assert data['post']['id'] == post_id
    assert data['post']['title'] == 'Test title'
    assert data['post']['description'] == 'Test description'

    response = requests.post(
        f"{API_URL}/register",
        json={
            'username': 'test_get_private_post_2',
            "email": "testusertestuser@example.com",
            "password": "goodPassword1",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "User created"

    response = requests.get(
        f"{API_URL}/get_post", json={'username': 'test_get_private_post_2', 'password': 'goodPassword1', 'id': post_id}
    )
    assert response.status_code == 404
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Post not found or access denied"


def test_update_post():
    response = requests.post(
        f"{API_URL}/register",
        json={'username': 'test_update_post', "email": "testuser@example.com", "password": "goodPassword1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "User created"

    response = requests.post(
        f"{API_URL}/create_post",
        json={
            'username': 'test_update_post',
            'password': 'goodPassword1',
            'title': 'Test title',
            'description': 'Test description',
            'tags': ['tag1', 'tag2'],
            'is_private': False,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "Post created"
    assert data['post']['tags'] == ['tag1', 'tag2']
    assert data['post']['title'] == 'Test title'
    assert data['post']['description'] == 'Test description'
    post_id = data['post']['id']

    response = requests.patch(
        f"{API_URL}/update_post",
        json={
            'username': 'test_update_post',
            'password': 'goodPassword1',
            'id': post_id,
            'title': 'New title',
            'description': 'New description',
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "Post updated"
    assert data['post']['title'] == 'New title'
    assert data['post']['description'] == 'New description'
    assert data['post']['tags'] == ['tag1', 'tag2']

    response = requests.get(
        f"{API_URL}/get_post", json={'username': 'test_update_post', 'password': 'goodPassword1', 'id': post_id}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "Post found"
    assert data['post']['id'] == post_id
    assert data['post']['title'] == 'New title'
    assert data['post']['description'] == 'New description'
    assert data['post']['tags'] == ['tag1', 'tag2']

    invalid_post_id = 1000000

    response = requests.patch(
        f"{API_URL}/update_post",
        json={
            'username': 'test_update_post',
            'password': 'goodPassword1',
            'id': invalid_post_id,
            'title': 'New title',
            'description': 'New description',
        },
    )
    assert response.status_code == 404
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Post not found or access denied"

    response = requests.post(
        f"{API_URL}/register",
        json={'username': 'test_update_post_2', "email": "testuser@example.com", "password": "goodPassword1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "User created"

    response = requests.patch(
        f"{API_URL}/update_post",
        json={
            'username': 'test_update_post_2',
            'password': 'goodPassword1',
            'id': post_id,
            'title': 'New title',
            'description': 'New description',
        },
    )
    assert response.status_code == 404
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Post not found or access denied"


def test_list_posts():
    response = requests.post(
        f"{API_URL}/register",
        json={'username': 'test_list_posts', "email": "testuser@example.com", "password": "goodPassword1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "User created"

    for i in range(3):
        response = requests.post(
            f"{API_URL}/create_post",
            json={
                'username': 'test_list_posts',
                'password': 'goodPassword1',
                'title': f'Test title {i}',
                'description': f'Test description {i}',
                'is_private': i == 1,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['message'] == "Post created"

    response = requests.get(
        f"{API_URL}/list_posts",
        json={
            'username': 'test_list_posts',
            'password': 'goodPassword1',
            'page_number': 0,
            'page_size': 3,
            'author': 'test_list_posts',
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['posts']) == 3
    assert data['posts'][0]['title'] == 'Test title 0'
    assert data['posts'][1]['title'] == 'Test title 1'
    assert data['posts'][2]['title'] == 'Test title 2'

    response = requests.get(
        f"{API_URL}/list_posts",
        json={
            'username': 'test_list_posts',
            'password': 'goodPassword1',
            'page_number': 1,
            'page_size': 2,
            'author': 'test_list_posts',
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['posts']) == 1
    assert data['posts'][0]['title'] == 'Test title 2'

    response = requests.get(
        f"{API_URL}/list_posts",
        json={
            'username': 'test_list_posts',
            'password': 'goodPassword1',
            'page_number': 1,
            'page_size': 3,
            'author': 'test_list_posts',
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['posts']) == 0

    response = requests.post(
        f"{API_URL}/register",
        json={
            'username': 'test_list_posts_2',
            "email": "testuser@example.com",
            "password": "goodPassword1",
            'author': 'test_list_posts',
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "User created"

    response = requests.get(
        f"{API_URL}/list_posts",
        json={
            'username': 'test_list_posts_2',
            'password': 'goodPassword1',
            'page_number': 0,
            'page_size': 3,
            'author': 'test_list_posts',
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['posts']) == 2

    response = requests.get(
        f"{API_URL}/list_posts",
        json={
            'username': 'test_list_posts_2',
            'password': 'goodPassword1',
            'page_number': 1,
            'page_size': 1,
            'author': 'test_list_posts',
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['posts']) == 1
    assert data['posts'][0]['title'] == 'Test title 2'
