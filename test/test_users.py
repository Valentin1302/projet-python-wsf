import pytest
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def reset_users():
    with open('users.json', 'w') as f:
        json.dump([], f)
    yield
    with open('users.json', 'w') as f:
        json.dump([], f)

def test_create_user(client, reset_users):
    headers = {'X-API-Key': 'api-key-123', 'Content-Type': 'application/json'}
    data = {'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com'}
    
    response = client.post('/users', json=data, headers=headers)
    
    assert response.status_code == 201
    assert response.json['first_name'] == 'John'
    assert response.json['last_name'] == 'Doe'
    assert response.json['email'] == 'john@example.com'

def test_get_all_users(client, reset_users):
    headers = {'X-API-Key': 'api-key-123', 'Content-Type': 'application/json'}
    
    client.post('/users', json={'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com'}, headers=headers)
    client.post('/users', json={'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane@example.com'}, headers=headers)
    
    response = client.get('/users', headers=headers)
    
    assert response.status_code == 200
    assert len(response.json) == 2

def test_get_user_by_id(client, reset_users):
    headers = {'X-API-Key': 'api-key-123', 'Content-Type': 'application/json'}
    
    client.post('/users', json={'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com'}, headers=headers)
    
    response = client.get('/users/1', headers=headers)
    
    assert response.status_code == 200
    assert response.json['first_name'] == 'John'

def test_update_user(client, reset_users):
    headers = {'X-API-Key': 'api-key-123', 'Content-Type': 'application/json'}
    
    client.post('/users', json={'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com'}, headers=headers)
    
    update_data = {'first_name': 'Johnny'}
    response = client.put('/users/1', json=update_data, headers=headers)
    
    assert response.status_code == 200
    assert response.json['first_name'] == 'Johnny'

def test_delete_user(client, reset_users):
    headers = {'X-API-Key': 'api-key-123', 'Content-Type': 'application/json'}
    
    client.post('/users', json={'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com'}, headers=headers)
    
    response = client.delete('/users/1', headers=headers)
    
    assert response.status_code == 200
    assert response.json['message'] == 'User deleted'

def test_unauthorized_access(client, reset_users):
    headers = {'Content-Type': 'application/json'}
    
    response = client.get('/users', headers=headers)
    
    assert response.status_code == 401
    assert response.json['error'] == 'Unauthorized'
