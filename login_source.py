"""
flask-login.readthedocs.io

To run the flask app:
$ <activate virtual environment>
$ pip install flask
$ pip install WTForms
$ pip install tabulate
$ pip install flask_login
$ pip install passlib
$ export FLASK_APP=login_source
$ flask run

Investigated ways to implement a login system with flask, with Jemal Jemal. We
 went through the docs for flask-login and WTForms and decided that these were
 the tools we will use. Following this, we watched two youtube videos:
 1) https://www.youtube.com/watch?v=2dEM-s3mRLE
 2) https://www.youtube.com/watch?v=zRwy8gtgJ1A
 The first was not to helpful. The second is just what we need, and we plan on
 meeting tomorrow to use it to help us implement the login.


24th April afternoon
Spoke with Isaac, Morgan and Jemal discussing the studtures of the tables and
divying up work. Set a timeline for when certain work is due by.

24th April evening
Pair-prgramming with Jemal to set up the Registeration. Used WTFform tutorials,
and bootstrap examples. Also relied on code snippets from
http://flask.pocoo.org/snippets/98/

25th April morning
Wrapped up the the login code. A user can now register and then log into our
website. There are validation checks in both the login and registeration page.
The password is encrypted. Upon Loging in, the user is moved to a dashboard
where all the active chats that the user is in are displayed.

"""

import sqlite3
from database import *
from Social_Media import *
from flask import *
from flask.ext.login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user

from passlib.hash import sha256_crypt # a hash algorithm that encrypts password
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
import os



class User(UserMixin):
    """
    Inherits from UserMixin that implments:

    1) is_authenticated(self): Checks if user is authenticated (has provided
    valid credentials).

    2) is_active(self):

    3) is_anonymous(self):

    4) get_id(self):
    return

    """

    def __init__(self, id):
        """
        Constructor for user object.
        """
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        """
        Overloading print function for User Objects.
        """
        return "%d/%s/%s" % (self.id, self.name, self.password)


# Register Form Class
class RegisterForm(Form):
    """
    This connects the html registeration form fields corresponding to the
    rendered HTML page's fields. The validators set requirements on the form
    fields.

    Inherits from Form. See http://flask.pocoo.org/snippets/135/
    """
    name = StringField('Name',
                       [validators.Length(min=1, max=50)])
    username = StringField('Username',
                           [validators.Length(min=4, max=25)])
    email = StringField('Email',
                        [validators.Length(min=6, max=50)])
    password = PasswordField('Password',
                             [validators.DataRequired(),
                              validators.EqualTo('confirm',
                                                 message='Incorrect Password')
                              ])
    confirm = PasswordField('Confirm Password')



