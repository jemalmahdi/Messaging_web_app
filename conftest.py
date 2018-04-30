"""
WooMessages
CS 232
Final Project
AVI VAJPEYI, JEMAL JEMAL, ISAAC WEISS, MORGAN THOMPSON


"""
import app_main
import pytest
import os
import tempfile
import logging
import time
logging.basicConfig(filename='flask_api_test.log', level=logging.DEBUG)
logging.debug(time.ctime() + ': ------------------------------------')


@pytest.fixture(scope='session')
def test_client():
    db_fd, app_main.app.config['DATABASE'] = tempfile.mkstemp()
    app_main.app.testing = True
    test_client = app_main.app.test_client()
    logging.debug('run')
    print('lets init')
    with app_main.app.app_context():
        app_main.init_db()

    yield test_client

    os.close(db_fd)
    os.unlink(app_main.app.config['DATABASE'])
