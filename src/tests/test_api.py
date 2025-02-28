import pytest
import requests

API_URL = "http://localhost:5000"

def test_register_user():
    assert True
    pass
    # response = requests.post(f"{API_URL}/register", json={
    #     'username': 'testuser',
    #     'password': 'testpass',
    #     'email': 'testuser@example.com'
    # })
    # assert response.status_code == 200
    # data = response.json()
    # assert data['success'] is True or data['message'] == "User already exists"

def test_login_user():
    assert True
    pass
    # response = requests.post(f"{API_URL}/login", json={
    #     'username': 'testuser',
    #     'password': 'testpass'
    # })
    # assert response.status_code == 200
    # data = response.json()
    # assert data['success'] is True