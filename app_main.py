"""
WooMessages
CS 232
Final Project


AVI VAJPEYI, JEMAL JEMAL, ISAAC WEISS, MORGAN THOMPSON

This Flask app allows a user to interact with a music artist database in a
RESTful fashion. Resources can be posted, updated, deleted or queired for.


To run the flask app:
$ <activate virtual environment>
$ pip install flask
$ pip install WTForms
$ pip install tabulate
$ pip install flask_login
$ pip install passlib
$ export FLASK_APP=app_main.py
$ flask run

*******************************************************************************
A general description of the WooMessage API is as follows.

There are three types of resources: Artists, Albums, Tracks

--ARTISTS
An artist resource is an individual musical artist.

    Attributes:
    id int -- The unique number to represent this resource.
    name string -- The name of the artist.
    age int -- The age of the artist.


GET /artist

Description:
Get a list of all artists

Parameters:
None

Example usage:
$ curl -X GET http://127.0.0.1:5000/artists/
[
  {
        "id": 1,
        "name": Bob,
        "age": 80,
  },
  {
        "id": 1,
        "name": Bobbie,
        "age": 8,
  }
]

GET /artists/:id

Description:
Get a single artist by ID

Parameters:
id - the ID of the dog

Example usage:
$ curl -X GET http://127.0.0.1:5000/artists/1
{
    "id": 1,
    "name": Bobbie,
    "age": 8,
}


POST /artist

Description:
Add a new artist and get the added artist in response


Example usage:
$ curl -X POST -d "name"="Elvis" -d "age="131" http://127.0.0.1:5000/artists/
{
    "id": 1,
    "name": Bobbie,
    "age": 8,
}


PUT /artist

Description:
Update ALL attributes of an artist and
get the updated artist in response

Parameters:
id - the id of the artist


Example usage:
$ curl -X PUT -d "name"="Elvis" -d "age="131" http://127.0.0.1:5000/artists/1
{
    "id": 1,
    "name": Bobbie,
    "age": 8,
}


PATCH /artist

Description:
Update one or more attributes of an artist and
get the updated artist in response

Parameters:
id - the id of the artist

Example usage:
$ curl -X PATCH -d "name"="Elvis" -d "age="131" http://127.0.0.1:5000/artists/1
{
    "id": 1,
    "name": Bobbieee,
    "age": 8,
}


DELETE /artist

Description:
Delete an artist and get the deleted artist in response

Parameters:
id - the id of the artist

Example usage:
$ curl -X DELETE http://127.0.0.1:5000/artists/1
{
    "id": 1,
    "name": Bobbie,
    "age": 8,
}

*******************************************************************************
--Albums
An album resource is an individual musical album.

    Attributes:
    id int -- The unique number to represent this resource.
    name string -- The name of the album.
    artist_id int -- The id of the artist who created the album.


GET /album

Description:
Get a list of all albums

Parameters:
None

Example usage:
$ curl -X GET http://127.0.0.1:5000/albums/
[
  {
        "id": 1,
        "name": Bob,
        "artist_id": 80,
  },
  {
        "id": 1,
        "name": Bobbie,
        "artist_id": 8,
  }
]

GET /albums/:id

Description:
Get a single album by ID

Parameters:
id - the ID of the album

Example usage:
$ curl -X GET http://127.0.0.1:5000/albums/1
{
    "id": 1,
    "name": Bobbie,
    "artist_id": 8,
}


POST /album

Description:
Add a new album and get the added album in response

Example usage:
$ curl -X POST -d "name"="Elvis" -d "age="131" http://127.0.0.1:5000/albums/
{
    "id": 1,
    "name": Bobbie,
    "artist_id": 8,
}


PUT /album

Description:
Update ALL attributes of an album and
get the updated album in response

Parameters:
id - the id of the album

Example usage:
$ curl -X POST -d "name"="Elvis" -d "age="131" http://127.0.0.1:5000/albums/1
{
    "id": 1,
    "name": Bobbie,
    "artist_id": 8,
}

PATCH /album

Description:
Update one or more attributes of an album and
get the updated album in response

Parameters:
id - the id of the album

Example usage:
$ curl -X PATCH -d "name"="Elvis" -d "age="131" http://127.0.0.1:5000/albums/1
{
    "id": 1,
    "name": Bobbie,
    "artist_id": 8,
}


DELETE /album

Description:
Delete an album and get the deleted album in response

Parameters:
id - the id of the album

Example usage:
$ curl -X DELETE http://127.0.0.1:5000/albums/1
{
    "id": 1,
    "name": Bobbie,
    "artist_id": 8,
}

*******************************************************************************
--Track
A track resource is an individual musical track.

    Attributes:
    album_id int -- The id of the album the track is from
    duration int -- The duration of the track in seconds
    id int -- The unique number to represent this resource.
    name string -- The name of the track.


GET /tracks/

Description:
Get a list of all tracks

Parameters:
None

Example usage:
$ curl -X GET http://127.0.0.1:5000/tracks/
[
  {
    "album_id": 1,
    "duration": 156,
    "id": 1,
    "name": "Ace of Spades"
  },
  {
    "album_id": 2,
    "duration": 120,
    "id": 2,
    "name": "All My Life"
  }
]

GET /tracks/:id

Description:
Get a single track by ID

Parameters:
id - the ID of the track

Example usage:
$ curl -X GET http://127.0.0.1:5000/tracks/1
{
    "album_id": 1,
    "duration": 156,
    "id": 1,
    "name": "Ace of Spades"
}


POST /tracks/

Description:
Add a new track and get the added track in response

Parameters:
id - the id of the track

Example usage:
$ curl -X POST -d "album_id"="23" -d "duration"="23" -d "name"="Blah"
http://127.0.0.1:5000/tracks/1
{
    "album_id": 23,
    "duration": 23,
    "id": 1,
    "name": "Blah"
}


PUT /tracks/

Description:
Update ALL attributes of an track (other than ID) and
get the updated track in response

Parameters:
id - the id of the track

Example usage:
$ curl -X PUT -d "album_id"="23" -d "duration"="23" -d "name"="Blah"
http://127.0.0.1:5000/tracks/1
{
    "album_id": 1,
    "duration": 156,
    "id": 1,
    "name": "Ace of Spades"
}



PATCH -d album_id="1" -d duration="155" \
http://127.0.0.1:5000/track/1

Description:
Update one or more attributes of an track and
get the updated track in response

Parameters:
id - the id of the track

Example usage:
$ curl -X PATCH -d "duration"="23" http://127.0.0.1:5000/tracks/1
{
    "album_id": 1,
    "duration": 23,
    "id": 1,
    "name": "Ace of Spades"
}



DELETE /tracks/:id

Description:
Delete an track and get the deleted track in response

Parameters:
id - the id of the track

Example usage:
$ curl -X DELETE http://127.0.0.1:5000/tracks/1
{
    "album_id": 1,
    "duration": 156,
    "id": 1,
    "name": "Ace of Spades"
}



*******************************************************************************
"""
from flask import Flask, g, jsonify, request, render_template
from flask.views import MethodView
import os
import csv
import sqlite3
from collections import OrderedDict

from flask import Flask, g, jsonify, request, \
    render_template, redirect, url_for
import os
import click

from flask import *
from flask.ext.login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user
# a hash algorithm that encrypts password
from passlib.hash import sha256_crypt
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
import os

from login_source import *
from custom_views import *
from database import *
from Social_Media import *
from exception_classes import *
from queries import *
from custom_forms import *
import tabulate


app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.root_path, 'WooMessages.sqlite')
app.config["SECRET_KEY"] = 'thisissecret'
app.config.update(
    DATABASE=os.path.join(app.root_path, 'WooMessages.sqlite'),
    DEBUG=True,
    SECRET_KEY='thisissecret'
)

# flask-login
login_manager = LoginManager()  # allows Flask-Login
login_manager.init_app(app)  # Once app obj created, configures it for login
login_manager.login_view = "login"


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Database Created')


@app.cli.command('initdb_with_csv')
@click.argument('filename')
def convert_csv_to_sqlite_command(filename):
    convert_csv_to_sqlite(filename)
    print('Inserted ' + filename)


@login_manager.user_loader
def load_user(user_id):
    """
    Reloads the USER obj specified by USER ID, stored during one login session.

    :param userid: unicode ID of user
    :return: corresponding user object
    """
    return User.get(user_id)


@app.route('/')
def home_page():
    """
    Serves as a home page
    """
    return render_template('HomePage.html')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        # check if there is a post request and if the data inputted to form
        # is in the correct format (if it has been validated)

        insert_user(name=form.name.data,
                    email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        # Flash a message to the HTML cause we just registered babbyyyyyy
        flash('Congratulations! You have sold your soul to WooMessages! Next '
              'time, read terms and conditions. Proceed to Login.', 'success')

        # now that registered, send to login site
        return redirect(url_for('login'))
    return render_template('RegisterationPage.html', form=form)  # default GET


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_entered = request.form['password']

        userdata = get_user_by_username(username)

        # if the returned data is for a user
        if userdata is not None:
            # Get stored hash
            password_real = userdata['password']

            # Compare Password entered to password saved in DB
            if sha256_crypt.verify(password_entered, password_real):
                # yay! The passwords match
                session['logged_in'] = True
                session['username'] = username
                welcome_text = "Welcome back, " + str(userdata['name'])

                flash(welcome_text, 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid password'
                flash("Invalid password", 'danger')
                return render_template('Login.html', error=error)

        else:
            error = 'Username not found'
            flash("WHO IS U??? Username not found", 'danger')
            return render_template('login.html', error=error)

    return render_template('Login.html')


# Check if user logged in
def is_logged_in(f):
    """
    Code adapted from http://flask.pocoo.org/snippets/98/

    :param f:
    :return:
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('Logged out!', 'success')
    return redirect(url_for('login'))


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    """

    :param e:
    :return:
    """
    return Response('<p>Login failed!</p>')


# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    """


    :return:
    """

    data = get_chat_rooms(get_user_id(session['username']))

    # data = get_chat_rooms(get_user_id(session['username']))

    num_rows = 0
    if data is not None:
        num_rows = 1

    if num_rows > 0:
        return render_template('dashboard.html', chats=data)
    else:
        msg = 'No active chats'
        return render_template('dashboard.html', msg=msg)
    # Close connection
    cur.close()


##############################################################################


# Single chat room
@app.route('/chat_room/<string:id>/', methods=['GET', 'POST'])
def chat_room(id):
    data = get_messages_in_chatroom(id)
    room_data = get_room_info(id)
    participant_list = get_participants_in_chat(id)
    participant_str = ", ".join(str(participant) for
                                participant in participant_list)

    form = MessageForm(request.form)
    if request.method == 'POST' and form.validate():
        insert_message(message=form.message.data,
                       time=get_date(),
                       user_id=get_user_id(session['username']),
                       chat_id=id)

        data = get_messages_in_chatroom(id)

        return render_template('chat_room.html', names=participant_str,
                               room=room_data, chat_room=data, form=form)

    return render_template('chat_room.html', names=participant_str,
                           room=room_data, chat_room=data, form=form)


# Add chat room
@app.route('/add_chat', methods=['GET', 'POST'])
@is_logged_in
def add_chat():
    form = ChatRoomForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        participants = form.participants.data
        participant_list = participants.split(",")
        participant_list[:] = [p.replace(' ', '') for p in participant_list]

        # user creating the chat must be in the chat
        participant_list.append(session['username'])

        result = insert_chat_room(title, participant_list)

        if result.isdigit():
            flash('Chat room \"{}\" created!'.format(get_chat_room_name(id)),
                  'success')
            return redirect(url_for('dashboard'))
        else:
            flash('User \"{}\" does not exist. '
                  'Could not create chat.'.format(str(result)),
                  'danger')
            return redirect(url_for('add_chat'))

        return redirect(url_for('dashboard'))

    return render_template('add_chat.html', form=form)


# Delete chat room
@app.route('/delete_chat/<string:id>', methods=['POST'])
@is_logged_in
def delete_chat(id):

    delete_user_from_chat(session['username'], id)

    chat_name = get_chat_room_name(id)

    flash('You have left the chat \"{}\"'.format(chat_name), 'success')

    return redirect(url_for('dashboard'))


##############################################################################

@app.errorhandler(RequestError)
def handle_invalid_usage(error):
    """
    Returns a JSON response built from RequestError.

    :param error: the RequestError
    :return: a response containing the error message
    """
    return error.to_response()


def add_view_rules(view, view_url):
    """
    Adds rules to a custom MethodView. Preconditions are that the custom
    MethodView has the RESTful API implmented.

    :param view: the custom MethodView
    :param view_url: the URL that the view is routed to.
    :return:
    """

    app.add_url_rule(view_url,
                     defaults={'id': None},
                     view_func=view,
                     methods=['GET'])
    app.add_url_rule(view_url+'<int:id>',
                     view_func=view,
                     methods=['GET'])

    app.add_url_rule(view_url,
                     view_func=view,
                     methods=['POST'])

    app.add_url_rule(view_url+'<int:id>',
                     view_func=view,
                     methods=['DELETE'])

    app.add_url_rule(view_url+'<int:id>',
                     view_func=view,
                     methods=['PUT'])

    app.add_url_rule(view_url+'<int:id>',
                     view_func=view,
                     methods=['PATCH'])


def create_views_with_rules():
    """
    Helper function to add rules to the custom views written for the API of
    the Free Music Database.

    :return: None
    """
    message_view = MessageView.as_view('message_view')
    add_view_rules(message_view, '/api/message/')

    user_view = UserView.as_view('user_view')
    add_view_rules(user_view, '/api/user/')

    chat_view = ChatView.as_view('chat_view')
    add_view_rules(chat_view, '/api/chat/')

    chatrel_view = ChatRelView.as_view('chatrel_view')
    add_view_rules(chatrel_view, '/api/chatrel/')


create_views_with_rules()

if __name__ == "__main__":
    app.secret_key = 'thisissecret'
    app.run(debug=True)
