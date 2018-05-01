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
$ pip install pytest
$ export FLASK_APP=app_main.py
$ flask run

*******************************************************************************
OUTSIDE SOURCES

Code for the login+logout adapted from a blog in the website
http://flask.pocoo.org/snippets/98/

Code for the WTForms obtained from another page of the same blog website
http://flask.pocoo.org/docs/0.12/patterns/wtforms/

*******************************************************************************
A general description of the WooMessage API is as follows.

There are three types of resources: user, chat, message

--USER
An user resource is an individual user.

    Attributes:
    email string -- The unique email of the user
    id int -- The unique number to represent this resource.
    name string -- The name of the user.
    password string -- The ENCRYPTED password of the user.
    username string -- The unique username associated with the user.

GET /user

Description:
Get a list of all users

Parameters:
None

Example usage:
$ curl -X GET http://127.0.0.1:5000/api/user/
[
  {
    "email": "JJemal20@wooster.edu",
    "id": 1,
    "name": "Jemal",
    "password": "$5$rounds=535000$oBWsPrEhsccUSqEH$ut/SZIwokcxcNFHWIClyi8bCt.",
    "username": "JemalMahdi"
  },
  {
    "email": "Avajpai18@wooster.edu",
    "id": 2,
    "name": "Avi",
    "password": "$5$rounds=535000$68DCPBEA.GfYxWWD$eiN6GrnZWEJi5JSBbC",
    "username": "AviVajpeyi"
  }
]

GET /user/:id

Description:
Get a single user by ID number

Parameters:
id - the ID of the user

Example usage:
$ curl -X GET http://127.0.0.1:5000/api/user/1
{
    "email": "JJemal20@wooster.edu",
    "id": 1,
    "name": "Jemal",
    "password": "$5$rounds=535000$oBWsPrEhsccUSqEH$ut/SZIwokcxcNFHlrX/cEu5t.",
    "username": "JemalMahdi"
}


POST /user
-- NOT POSSIBLE because the password needs to encrypted with a secret key


PUT /user
-- NOT POSSIBLE because the password needs to encrypted with a secret key


PATCH /user

Description:
Update one or more attributes (ID and username fixed) of an user and
get the updated user in response.

Parameters:
id - the id of the user

Example usage:
$ curl -X PATCH -d "name"="Jimmy" http://127.0.0.1:5000/api/user/1
{
  "email": "JJemal20@wooster.edu",
  "id": 1,
  "name": "Jimmy",
  "password": "$5$rounds=535000$oBWsPrEhsccUSqEH$ut/SZIwokcxcNFHlrX/cEu5AIl",
  "username": "JemalMahdi"
}


DELETE /user

Description:
Delete an user and get the deleted user in response

Parameters:
id - the id of the user

Example usage:
$ curl -X DELETE http://127.0.0.1:5000/api/user/1
{
  "email": "JJemal20@wooster.edu",
  "id": 1,
  "name": "Jimmy",
  "password": "$5$rounds=535000$oBWsPrEhsccUSqEH$ut/SZIwokcxcNFHlrX/cEu5AIl2.",
  "username": "JemalMahdi"
}

*******************************************************************************
--Chat
An chat resource is an individual chat room data.

    Attributes:
    id int -- The unique number to represent this resource.
    time string --- The time (d/m/y HH:MM) the chat room was created.
    title string -- The name of the chat room.


GET /chat

Description:
Get a list of all chat

Parameters:
None

Example usage:
$ curl -X GET http://127.0.0.1:5000/api/chat/
[
  {
    "id": 1,
    "time": "4/25/18 21:49",
    "title": "School is good"
  },
  {
    "id": 2,
    "time": "5/4/18 21:49",
    "title": "I hate life"
  }
]

GET /chat/:id

Description:
Get a single chat by ID

Parameters:
id - the ID of the chat

Example usage:
$ curl -X GET http://127.0.0.1:5000/api/chat/1
{
    "id": 1,
    "time": "4/25/18 21:49",
    "title": "School is good"
}


POST /chat

Description:
Add a new chat and get the added chat in response

Example usage:
$ curl -X POST -d "title"="School" -d "time"="4/25/18 21:49"
http://127.0.0.1:5000/albums/
{
    "id": 1,
    "time": "4/25/18 21:49",
    "title": "School"
}



PUT /album

Description:
Update ALL attributes of a chat and
get the updated chat in response

Parameters:
id - the id of the chat

Example usage:
$ curl -X POST -d "title"="cool" -d "time"="4/25/18 21:49"
http://127.0.0.1:5000/api/chat/1
{
"id": 1,
    "time": "4/25/18 21:49",
    "title": "cool"
}


PATCH /album

Description:
Update one or more attributes of an chat and
get the updated chat in response

Parameters:
id - the id of the album

Example usage:
$ curl -X POST -d "title"="cool" -d "time"="4/25/18 21:49"
http://127.0.0.1:5000/api/chat/1
{
    "id": 1,
    "time": "4/25/18 21:49",
    "title": "cool"
}


DELETE /chat

Description:
Delete an chat and get the deleted chat in response

Parameters:
id - the id of the chat

Example usage:
$ curl -X DELETE http://127.0.0.1:5000/api/chat/1
{
    "id": 1,
    "time": "4/25/18 21:49",
    "title": "cool"
}

*******************************************************************************
--Message
A message resource is an individual message sent by a user in on chat room.

    Attributes:
    album_id int -- The id of the album the track is from
    duration int -- The duration of the track in seconds
    id int -- The unique number to represent this resource.
    name string -- The name of the track.

    id int -- The unique number to represent this resource.
    user_id int -- The id of the user who sent the message
    chat_id int -- The id of the chat where the message is sent
    message string -- The message content of the message
    time string -- the time the message was sent


GET /message/

Description:
Get a list of all messages

Parameters:
None

Example usage:
$ curl -X GET http://127.0.0.1:5000/api/message/
[
  {
    "chat_id": 1,
    "id": 1,
    "message": "Boy I like school",
    "time": "4/25/18 21:49",
    "user_id": 1
  },
  {
    "chat_id": 1,
    "id": 2,
    "message": "I like donkeys",
    "time": "4/26/18 21:49",
    "user_id": 2
  }
]

GET /message/:id

Description:
Get a single message by ID

Parameters:
id - the ID of the message

Example usage:
$ curl -X GET http://127.0.0.1:5000/message/1
{
    "chat_id": 1,
    "id": 3,
    "message": "nah. i think school sucks",
    "time": "4/27/18 21:49",
    "user_id": 3
}



POST /message/

Description:
Add a new message and get the added message in response

Parameters:
id - the id of the message

Example usage:
$ curl -X POST -d "message"="HI" -d "chat_id"="3" -d "user_id"="1"
-d "time"="4/27/18 21:49"
http://127.0.0.1:5000/api/message/1
{
    "chat_id": 1,
    "id": 3,
    "message": "nah. i think school sucks",
    "time": "4/27/18 21:49",
    "user_id": 3
}


PUT /message/:id

Description:
Update ALL attributes of an track (other than ID) and
get the updated track in response

Parameters:
id - the id of the track

Example usage:
$ curl -X POST -d "message"="HI" -d "chat_id"="3" -d "user_id"="1"
-d "time"="4/27/18 21:49" http://127.0.0.1:5000/api/message/1
{
    "chat_id": 1,
    "id": 3,
    "message": "nah. i think school sucks",
    "time": "4/27/18 21:49",
    "user_id": 3
}



PATCH /message/:id

Description:
Update one or more attributes of an track and
get the updated track in response

Parameters:
id - the id of the track

Example usage:
$ curl -X PATCH -d "message"="HI" -d "chat_id"="3" -d "user_id"="1"
-d "time"="4/27/18 21:49" http://127.0.0.1:5000/api/message/1
{
    "chat_id": 1,
    "id": 3,
    "message": "nah. i think school sucks",
    "time": "4/27/18 21:49",
    "user_id": 3
}


DELETE /message/:id

Description:
Delete an track and get the deleted track in response

Parameters:
id - the id of the track

Example usage:
$ curl -X DELETE http://127.0.0.1:5000/api/message/1
{
    "chat_id": 1,
    "id": 3,
    "message": "nah. i think school sucks",
    "time": "4/27/18 21:49",
    "user_id": 3
}

*******************************************************************************
"""
# Imported Scripts
import click
from flask import *
from flask.ext.login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user
# a hash algorithm that encrypts password
from passlib.hash import sha256_crypt
from functools import wraps
import os

# Our Scripts
from custom_views import *
from database_class import *
from exception_classes import *
from queries import *
from custom_forms import *


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
    """
    Helper function to initialise DB
    :return: None
    """
    init_db()
    print('Database Created')


@app.cli.command('initdb_with_csv')
@click.argument('filename')
def convert_csv_to_sqlite_command(filename):
    """
    Helper function to convert
    :param filename:
    :return: None
    """
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
    """
    Serves the registeration page

    :return: The login page if POST the Registeration page if GET
    """
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
    """
    Serves the login page.

    :return: returns the Login.html
    """
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
            return render_template('Login.html', error=error)

    return render_template('Login.html')


# Check if user logged in
def is_logged_in(f):
    """
    This is a function decoration we have written to check if the user is
    logged in.

    :param f: function to decorate with this check
    :return: returns the wrapped function
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
    """
    Deletes a session to log a user out.

    :return: the Login Page.
    """
    session.clear()
    flash('Logged out!', 'success')
    return redirect(url_for('login'))


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    """
    HTML for a 401 error during Login

    :param e: The thrown error
    :return: An HTML with "Login failed"
    """
    return Response('<p>Login failed!</p>')


# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    """
    Obtains the information to send to the dashboard.html such as info
    on the various chat rooms that the user is a part of.

    :return:
    """

    data = get_chat_rooms(get_user_id(session['username']))

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
@is_logged_in
def chat_room(id):
    """
    Obtains the information to send to the chat_room.html such as info
    on the chat room name, etc, the messages in the chat room, and a form
    to enter new messages.

    :param id: The chat room id
    :return: if GET or POST -- returns the chat_room.html
    """
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
    """
    Allows the user to add a new chat. The name of the chat, and the
    participants of the chat are acquired via a HTML form.

    :return: if GET -- returns the add_chat.html
             if POST -- if valid users added to chat dashboard.html
                        if invalid users added then returns the add_chat.html
    """
    form = ChatRoomForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        participants = form.participants.data
        participant_list = participants.split(",")
        participant_list[:] = [p.replace(' ', '') for p in participant_list]

        # user creating the chat must be in the chat
        participant_list.append(session['username'])

        result = insert_chat_room(title, participant_list)
        result_status = str(result).isdigit()

        if result_status:
            flash('Chat room \"{}\" created!'.
                  format(str(get_chat_room_name(result))),
                  'success')
            return redirect(url_for('dashboard'))
        else:
            flash('User \"{}\" does not exist. '
                  'Could not create chat.'.format(str(result)),
                  'danger')
            return redirect(url_for('add_chat'))

    return render_template('add_chat.html', form=form)


# Delete chat room
@app.route('/delete_chat/<string:id>', methods=['POST'])
@is_logged_in
def delete_chat(id):
    """
    Allows the user with ID to leave the chat room

    :param id: The user id
    :return: Returns the updated dashboard.html
    """

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
    the WooMessages Database.

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
