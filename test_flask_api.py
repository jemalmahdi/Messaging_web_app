import pytest
import tempfile
import os
import json

import Social_Media


@pytest.fixture
def test_client():
    db_fd, Social_Media.app.config['DATABASE'] = tempfile.mkstemp()
    Social_Media.app.testing = True
    test_client = Social_Media.app.test_client()

    with Social_Media.app.app_context():
        Social_Media.init_db()

    yield test_client

    os.close(db_fd)
    os.unlink(Social_Media.app.config['DATABASE'])


def test_post_user(test_client):
    """
    Post the user and then check the response for correctness.
    :param test_client: the flask test client
    """
    user = {
        'name': 'TestUser'
    }
    response = test_client.post('/api/user', data=user)

    # Check if the submission is successful
    assert response.status_code == 200

    response_json = json.loads(response.data)

    expected_keys = ('id', 'name', 'login_id')

    # Check that returned keys are those that are expected
    for key in expected_keys:
        assert key in response_json

    expected_values = {
        'id': 1,
        'name': 'TestUser',
        'login_id': 1  # Figure this out
    }

    # Check expected values against the response from the PUT request
    assert check_values(expected_values, response_json)

    response = test_client.get('/api/user/1')
    assert response.status_code == 200
    response_json = json.loads(response.data)

    # Check expected values against a GET request
    assert check_values(expected_values, response_json)


def test_get_user(test_client):
    """
    Get a series of users and checks for correctness.
    :param test_client: the flask test client
    """




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
