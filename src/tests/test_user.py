import pytest
import requests

API_URL = "http://api:5000"

@pytest.fixture(autouse=True)
def test_setup():
    import time
    time.sleep(3)


def test_register_user():
    response = requests.post(f"{API_URL}/register", json={
        'username': 'test_register_user',
    })
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Missing fields"

    response = requests.post(f"{API_URL}/register", json={
        'username': 'test_register_user',
        "email": "testuser@example.com",
        "password": "12341234"
    })
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Password must be at least 8 characters long, contain a number and an uppercase letter"

    response = requests.post(f"{API_URL}/register", json={
        'username': 'test_register_user',
        "email": "testuser",
        "password": "goodPassword1"
    })
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Invalid email format"

    response = requests.post(f"{API_URL}/register", json={
        'username': 'test_register_user',
        "email": "testuser@example.com",
        "password": "goodPassword1"
    })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "User created"

    response = requests.post(f"{API_URL}/register", json={
        'username': 'test_register_user',
        "email": "testuser@example.com",
        "password": "goodPassword1"
    })
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "User already exists"


def test_get_user():
    response = requests.get(f"{API_URL}/user")
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Username is required"
    assert response.status_code == 400

    response = requests.get(f"{API_URL}/user", params={'username': 'test_get_user'})
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "User not found"
    assert response.status_code == 404

    response = requests.post(f"{API_URL}/register", json={
        'username': 'test_get_user',
        'password': 'testpAss1',
        'email': 'testuser@example.com'
    })
    assert response.status_code == 200
    data = response.json()
    assert data['success']

    response = requests.get(f"{API_URL}/user", params={'username': 'test_get_user'})
    data = response.json()
    assert response.status_code == 200
    assert data['success'] is True
    assert data['username'] == 'test_get_user'
    assert data['email'] == 'testuser@example.com'
    assert data['first_name'] == ''
    assert data['last_name'] == ''
    assert data['phone_number'] == ''
    assert data['birth_date'] == ''


def test_login_user():
    response = requests.post(f"{API_URL}/register", json={
        'username': 'test_login_user',
        "email": "testuser@example.com",
        "password": "goodPassword1"
    })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "User created"

    response = requests.post(f"{API_URL}/login", json={
        'username': 'test_login_user',
        "password": "wrongPassword1"
    })
    assert response.status_code == 401
    data = response.json()
    assert data['success'] is False
    assert data['message'] == "Invalid credentials"

    response = requests.post(f"{API_URL}/login", json={
        'username': 'test_login_user',
        "password": "goodPassword1"
    })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "Auth succeeded"


def test_update_user():
    response = requests.post(f"{API_URL}/register", json={
        'username': 'test_update_user',
        "email": "testuser@example.com",
        "password": "goodPassword1"
    })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['message'] == "User created"

    response = requests.get(f"{API_URL}/user", params={'username': 'test_update_user'})
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['phone_number'] == ""

    response = requests.patch(f"{API_URL}/update_profile", json={
        "username": "test_update_user",
        "password": "goodPassword1",
        "phone_number": "88005553535"
    })
    assert response.status_code == 200

    response = requests.get(f"{API_URL}/user", params={'username': 'test_update_user'})
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['phone_number'] == "88005553535"

    response = requests.patch(f"{API_URL}/update_profile", json={
        "username": "test_update_user",
        "password": "goodPassword13",
        "phone_number": "88005553536"
    })
    assert response.status_code == 401

    response = requests.get(f"{API_URL}/user", params={'username': 'test_update_user'})
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['phone_number'] == "88005553535"
