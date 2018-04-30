"""
WooMessages
CS 232
Final Project
AVI VAJPEYI, JEMAL JEMAL, ISAAC WEISS, MORGAN THOMPSON

"""

from wtforms import *


# Register Form Class
class RegisterForm(Form):
    """
    This connects the html registeration form fields corresponding to the
    rendered HTML page's fields. The validators set requirements on the form
    fields.

    Inherits from Form. See http://flask.pocoo.org/snippets/135/
    """
    name = StringField('Name',
                       [validators.Length(min=1, max=50),
                        validators.DataRequired()])

    username = StringField('Username',
                           [validators.Length(min=4, max=25),
                            validators.DataRequired()])

    email = StringField('Email',
                        [validators.Length(min=6, max=50),
                         validators.DataRequired(),
                         validators.Email()])

    password = PasswordField('Password',
                             [validators.DataRequired(),
                              validators.EqualTo('confirm',
                                                 message='Incorrect Password'),
                              validators.DataRequired()])

    confirm = PasswordField('Confirm Password')


# Register Form Class
class ChatRoomForm(Form):
    """


    Inherits from Form. See http://flask.pocoo.org/snippets/135/
    """
    title = StringField('Name',
                        [validators.Length(min=1, max=50)])
    participants = StringField('Participants',
                               [validators.Length(min=4, max=250)])


# Register Form Class
class MessageForm(Form):
    """

    Inherits from Form. See http://flask.pocoo.org/snippets/135/
    """
    message = StringField('Message', [validators.Length(min=1, max=500)])
