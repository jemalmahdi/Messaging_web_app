import pytest
import tempfile
import os
import json
from passlib.hash import sha256_crypt

import app_main


@pytest.fixture
def test_client():
    db_fd, app_main.app.config['DATABASE'] = tempfile.mkstemp()
    app_main.app.testing = True
    test_client = app_main.app.test_client()

    print('lets init')
    with app_main.app.app_context():
        app_main.init_db()

    yield test_client

    os.close(db_fd)
    os.unlink(app_main.app.config['DATABASE'])


def test_post_user(test_client):
    """
    Post the user and then check the response for correctness.
    :param test_client: the flask test client
    """

    # ----------Check Success---------
    password = 'sup3rs3cur3passw0rd'
    user = {
        'name': 'TestUser',
        'email': 'test@test.test',
        'username': 'user',
        'password': password
    }
    response = test_client.post('/api/user/', data=user)

    # Check if the submission is successful
    assert response.status_code == 200

    response_json = json.loads(response.data)
    expected_keys = ('id', 'name', 'email', 'username', 'password')
    assert check_keys(expected_keys, response_json)
    # Checks if the passwords match
    assert sha256_crypt.verify(password,
                               response_json['password'])
    password_value = response_json['password']
    expected_values = {
        'id': 1,
        'name': 'TestUser',
        'email': 'test@test.test',
        'username': 'user',
        'password': password_value
    }

    # Check expected values against the response from the PUT request
    assert check_values(expected_values, response_json)

    # ----------Check 422----------
    user ={
        'name': 'testUser'
    }
    response = test_client.post('/api/user/', data=user)

    assert response.status_code == 422


def check_values(expected_values, response_json):
    """
    Checks the expected values against the response values.

    :param expected_values: A dictionary of expected values
    :param response_json: The json data of a response
    :return: True if values match, False otherwise
    """
    for key, value in expected_values.items():
        if response_json[key] != value:
            return False
    return True


def check_keys(expected_keys, response_json):
    """
    Checks that the expected keys match those of the response

    :param expected_keys: A dicitonary of expected keys
    :param response_json: The JSON data of a response
    :return: True if match, False otherwise
    """
    for key in expected_keys:
        if key not in response_json:
            return False
    return True
