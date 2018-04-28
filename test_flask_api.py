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


# ---------BEGIN POST TESTS----------
def test_post_user(test_client):
    """
    Tests the posting of a user for functionality using the post method.

    :param test_client: flask test client
    """
    api_path = '/api/user/'
    user_complete = {
        'name': 'TestUser',
        'email': 'test@test.test',
        'username': 'user',
        'password': 'sup3rs3cur3passw0rd'
    }
    user_partial = {
        'name': 'Break'
    }
    expected_keys = ('id', 'name', 'email', 'username', 'password')
    expected_values = {
        'id': 1,
        'name': 'TestUser',
        'email': 'test@test.test',
        'username': 'user',
        'password': None
    }
    data = (api_path,
            user_complete,
            user_partial,
            expected_keys,
            expected_values)
    post(test_client, data)


def test_post_chat(test_client):
    """
    Tests the post of a chat for functionality using the post method.

    :param test_client: flask test client
    """
    api_path = '/api/chat/'
    chat_complete = {
        'title': 'TestChat',
        'time': '12:00'
    }
    chat_partial = {
        'name': 'Chat'
    }
    expected_keys = ('id', 'title', 'time')
    expected_values = {
        'id': 1,
        'title': 'TestChat',
        'time': '12:00'
    }
    data = (api_path,
            chat_complete,
            chat_partial,
            expected_keys,
            expected_values)
    post(test_client, data)


def test_post_message(test_client):
    """
    Tests the post of a message for functionality using the post method.
    :param test_client: flask test client
    """
    api_path = '/api/message/'
    chat_complete = {
        'message': 'Hello world!',
        'time': '14:00',
        'user_id': 1,
        'chat_id': 1
    }
    chat_partial = {
        'message': 'Hello world!'
    }
    expected_keys = ('id', 'message', 'time', 'user_id', 'chat_id')
    expected_values = {
        'id': 1,
        'message': 'Hello world!',
        'time': '14:00',
        'user_id': 1,
        'chat_id': 1
    }
    data = (api_path,
            chat_complete,
            chat_partial,
            expected_keys,
            expected_values)
    post(test_client, data)


def test_post_chatrel(test_client):
    api_path = '/api/chatrel/'
    chatrel_complete = {
        'user_id': 1,
        'chat_id': 1
    }
    chatrel_partial = {
        'user_id': 1
    }
    expected_keys = ('id', 'user_id', 'chat_id')
    expected_values = {
        'id': 1,
        'user_id': 1,
        'chat_id': 1
    }
    data = (api_path,
            chatrel_complete,
            chatrel_partial,
            expected_keys,
            expected_values)
    post (test_client, data)


def post(test_client, data):
    """
    Checks the POST functionality of the API

    Checks:
    1) Checks for HTTP status code 200 for successful insert.
    2) Checks that the response has the expected key values.
    3) Checks that the data returned is the data that was submitted
    4) Attempts to GET the new submission and checks for a 200 HTTP status code
    5) Checks that the retrieved data matches what was submitted
    6) Attempts to submit partial form data, checks for a 422 HTTP status code.

    :param test_client: flask test client
    :param data: A tuple of the values to test. (api_path, user_complete,
    user_partial, expected_keys, expected_values)
    """
    api_path = data[0]
    user_complete = data[1]
    user_partial = data[2]
    expected_keys = data[3]
    expected_values = data[4]

    # executes a POST request and checks the status code for success
    response = test_client.post(api_path, data=user_complete)
    assert response.status_code == 200

    # checks that the keys in the response are as expected
    response_json = json.loads(response.data)
    assert check_keys(expected_keys, response_json)

    # A special case for testing the posing of users. It checks that the
    # passwords match and then updates the expected_values to have the
    # password in it. This is done so the check_values assertion below works.
    if 'password' in expected_values and expected_values['password'] is None:
        assert sha256_crypt.verify(user_complete['password'],
                                   response_json['password'])
        expected_values['password'] = response_json['password']

    # checks that the data in the response is as expected
    assert check_values(expected_values, response_json)

    # executes a GET request
    response = test_client.get(api_path+'1')
    assert response.status_code == 200

    # checks if the GET request data was as expected
    response_json = json.loads(response.data)
    assert check_values(expected_values, response_json)

    # attempt to post a partial input and checks if it throws a 422 error
    response = test_client.post(api_path, data=user_partial)
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
# ----------END POST TESTS----------
