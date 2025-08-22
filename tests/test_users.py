import json
import pytest

from app import create_app, db


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def test_create_user_and_hash_password(client):
    payload = {"user": "alice", "password": "secret", "dosha": "vata"}
    rv = client.post('/api/users', data=json.dumps(payload),
                     content_type='application/json')
    assert rv.status_code == 201
    data = rv.get_json()
    assert data['user'] == 'alice'
    # password hash should never be exposed in API responses
    assert 'password_hash' not in data


def test_unique_username(client):
    payload = {"user": "bob", "password": "pass"}
    rv1 = client.post('/api/users', data=json.dumps(payload),
                      content_type='application/json')
    assert rv1.status_code == 201

    rv2 = client.post('/api/users', data=json.dumps(payload),
                      content_type='application/json')
    assert rv2.status_code == 409


def test_list_and_get_user(client):
    # create two users
    for name in ["carl", "dina"]:
        client.post(
            '/api/users',
            data=json.dumps({"user": name, "password": "x"}),
            content_type='application/json'
        )

    rv = client.get('/api/users')
    assert rv.status_code == 200
    lst = rv.get_json()
    assert len(lst) == 2

    # get one by id
    user_id = lst[0]['id']
    rv2 = client.get(f'/api/users/{user_id}')
    assert rv2.status_code == 200
    obj = rv2.get_json()
    assert obj['id'] == user_id


def test_update_and_delete_user(client):
    rv = client.post(
        '/api/users',
        data=json.dumps({"user": "eve", "password": "old"}),
        content_type='application/json'
    )
    assert rv.status_code == 201
    user_id = rv.get_json()['id']

    # update username and dosha
    rv2 = client.patch(
        f'/api/users/{user_id}',
        data=json.dumps({"user": "eve2", "dosha": "kapha"}),
        content_type='application/json'
    )
    assert rv2.status_code == 200
    obj = rv2.get_json()
    assert obj['user'] == 'eve2'
    assert obj['dosha'] == 'kapha'

    # delete the user
    rv3 = client.delete(f'/api/users/{user_id}')
    assert rv3.status_code == 204

    # verify not found afterwards
    rv4 = client.get(f'/api/users/{user_id}')
    assert rv4.status_code == 404
