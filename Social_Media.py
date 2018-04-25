from flask import Flask, g, jsonify, request, render_template
from flask.views import MethodView
import os
import csv
import sqlite3
import datetime
from collections import OrderedDict

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.root_path, 'Social.sqlite')


def init_db():
    """
    This will initialize the database
    """
    conn = get_db()

    query = '''
        DROP TABLE IF EXISTS user;
        DROP TABLE IF EXISTS chat_rel;
        DROP TABLE IF EXISTS chat;
        DROP TABLE IF EXISTS message;
        CREATE TABLE user (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT UNIQUE,
            username TEXT UNIQUE,
            password TEXT
        );
        CREATE TABLE chat_rel(
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            chat_id INTEGER UNIQUE,
            FOREIGN KEY(user_id) REFERENCES user(id)
        );
        CREATE TABLE chat(
            message_id INTEGER PRIMARY KEY,
            time TEXT,
            id INTEGER,
            FOREIGN KEY(id) REFERENCES chat_rel(chat_id)
        );
        CREATE TABLE message (
            message TEXT,
            time TEXT,
            user_id INTEGER,
            id INTEGER,
            FOREIGN KEY(user_id) REFERENCES user(id),
            FOREIGN KEY(id) REFERENCES chat(id)
        );                    
    '''

    conn.cursor().executescript(query)


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Database Created')


def connect_db():
    """
    Returns a sqlite connection object associated with the application's
    database file.
    """

    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row

    return conn


def get_db():
    """
    Returns a database connection. If a connection has already been created,
    the existing connection is used, otherwise it creates a new connection.
    """

    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()

    return g.sqlite_db


def get_date():
    """
    Returns the current date and time in yyyy/mm/dd  h/m format
    """
    now = datetime.datetime.now()

    return now.strftime("%Y-%m-%d %H:%M")


def query_by_id(table_name, item_id):
    """
    Get a row from a table that has a primary key attribute named id.
    Returns None of there is no such row.
    :param table_name: name of the table to query
    :param item_id: id of the row
    :return: a dictionary representing the row
    """
    conn = get_db()
    cur = conn.cursor()

    query = 'SELECT * FROM {} WHERE id = ?'.format(table_name)

    cur.execute(query, (item_id,))

    row = cur.fetchone()

    if row is not None:
        return dict(row)
    else:
        return None


def get_all_rows(table_name):
    """
    Returns all of the rows from a table as a list of dictionaries. This is
    suitable for passing to jsonify().
    :param table_name: name of the table
    :return: list of dictionaries representing the table's rows
    """

    conn = get_db()
    cur = conn.cursor()

    query = 'SELECT * FROM {}'.format(table_name)

    results = []

    for row in cur.execute(query):
        results.append(dict(row))

    return results


def insert_message(message, user_id):
    """
    Will insert a new message into the message database. it will indicate which
    user had sent the message, as indicated by the user_id.

    :param message: the message to be added into the database
    :param user_id: the id of the user sending the message
    :return: a list of dictionaries representing the message recently sent
    """

    conn = get_db()
    cur = conn.cursor()

    query = '''
        INSERT INTO message(message, time, user_id) VALUES(?, ?, ?)
    '''

    cur.execute(query, (message, get_date(), user_id))
    conn.commit()

    cur.execute('SELECT * FROM message WHERE id = ?', (cur.lastrowid,))

    return dict(cur.fetchone())


def insert_user(name, login_id):
    """
    Will insert a new user into the database. This is given by a new login_id.

    :param name: the username of the new user
    :param login_id: the login_id of the user
    :return: a list of dictionaries representing the new user.
    """

    conn = get_db()
    cur = conn.cursor()

    query = '''
        INSERT INTO user(name, login_id) VALUES(?, ?)
    '''

    cur .execute(query, (name, login_id))
    conn.commit()

    cur.execute('SELECT * FROM user WHERE id = ?', (cur.lastrowid,))

    return dict(cur.fetchone())


def insert_login(username, password):
    """
    Will insert a new user into the database and check to ensure the username
    isn't taken. Also calls hash_and_salt() which will hash and salt the
    password.

    :param username: the username of a new user
    :param password: the password of a new user
    :return: a dictionary of the new user
    """
    conn = get_db()
    cur = conn.cursor()

    query = '''
        SELECT * FROM login WHERE user_name = ?
    '''

    execute(query, (username,))

    if cur.fetchone() is not None:
        raise RequestError(422, "Username is taken")
    else:
        password = hash_and_salt(password)
        cur.execute('INSERT INTO login(user_name, password) VALUES(?, ?)',
                    (username, password))
        conn.commit()

    cur.execute('SELECT * FROM login WHERE user_name = ?', (username,))

    return dict(cur.fetchone())


def update_message(message, user_id, message_id):
    """
    will update a message that was sent and needs to be fixed, as indicated by
    a specific user

    :param message: the message which is updated
    :param user_id: the user who is changing the message
    :param message_id: the id of the message to be changed
    :return: a dictionary representing the new message
    """

    conn = get_db()
    cur = conn.cursor()

    query = '''
        UPDATE message SET text = ? AND user_id = ? WHERE id = ?
    '''

    cur.execute(query, (message, user_id, message_id))
    conn.commit()

    cur.execute('SELECT * FROM message WHERE id = ?', (message_id,))

    return dict(cur.fetchone())


def update_user(user_id, name):
    """
    Wil update a username given a specific user_id

    :param user_id: the id of the user to be updated
    :param name: the updated username
    :return: a dictionary representing the new, updated user
    """

    conn = get_db()
    cur = conn.cursor()

    query = '''
        UPDATE user SET name = ? WHERE id = ?
    '''

    cur.execute(query, (name, user_id))
    conn.commit()

    cur.execute('SELECT * FROM user WHERE id = ?', (user_id,))

    return dict(cur.fetchone())

def delete_item(table_name, item_id):
    """
    This function deletes items with item_id from table_name
    :param table_name: the table which has an item to delete
    :param item_id: it item which to delte
    :return: NONE
    """
    conn = get_db()
    cur = conn.cursor()

    query = 'DELETE FROM {} WHERE id = ?'.format(table_name)

    cur.execute(query, (item_id,))
    conn.commit()

    return None


# START: Taken from homework 18
class RequestError(Exception):
    """
    Custom exception class for handling errors in a request.
    """

    def __init__(self, status_code, error_message):
        Exception.__init__(self)

        self.status_code = str(status_code)
        self.error_message = str(error_message)

    def to_response(self):
        response = jsonify({'error': self.error_message})
        response.status = self.status_code
        return response


@app.errorhandler(RequestError)
def handle_invalid_usage(error):
    """
    Returns a JSON response built from RequestError.

    :param error: the RequestError
    :return: a response containing the error message
    """
    return error.to_response()


# END: Taken from homework 18


@app.route('/')
def home_page():
    """
    Serves as a home page
    """
    return render_template('HomePage.html')


@app.route('/login')
def login():
    """
    Serves as a login page
    """

    return render_template('Login.html')


@app.route('/register')
def new_user():
    """
    Serves as a page to register a new account
    """

    return render_template('New_User.html')


class ChatRelView(MethodView):
    """
    This view handles all the /chatrel/ requests.
    """

    def get(self, chatrel_id):
        """
        Handle GET requests.

        Returns JSON representing all of the logins if login_id is None, or a
        single login if login_id is not None.

        :param chatrel_id: id of a login, or None for all logins
        :return: JSON response
        """
        if chatrel_id is None:
            chatrel = get_all_rows('chat_rel')
            return jsonify(chatrel)
        else:
            chatrel = query_by_id('chat_rel', chatrel_id)

            if chatrel is not None:
                response = jsonify(chatrel)
            else:
                raise RequestError(404, 'chat relation not found')

            return response

    def post(self):
        """
        Handles a POST request to insert a new login. Returns a JSON
        response representing the new login.

        The username must be provided in the requests's form data.

        :return: a response containing the JSON representation of the login
        """
        #Still working this one out.
        if 'username' not in request.form:
            raise RequestError(422, 'username required')
        else:
            if 'password' not in request.form:
                raise RequestError(422, 'password required')
            else:
                response = jsonify(insert_login(request.form['username'],
                                                request.form['password']))

        return response

    def delete(self, chatrel_id):
        """
        Handles a DELETE request given a certain login_id

        :param login_id: the id of the login to delete
        :return: a response containing the JSON representation of the
            old login
        """

        if chatrel_id is None:
            raise RequestError(422, 'chatrel_id required')
        else:
            chat = query_by_id('chat_rel', chatrel_id)

            if chat is not None:
                delete_item('chat_rel', chatrel_id)
            else:
                raise RequestError(404, 'Chat rel not found')
        return jsonify(chat)

    def put(self, chatrel_id):
        """
        Handles a PUT request given a certain login_id

        :param login_id: the id of the login to be put
        :return: a response containing the JSON representation of the
            new login
        """

        if chatrel_id is None:
            raise RequestError(422, 'chatrel_id is required')
        else:
            if 'user_id' not in request.form:
                raise RequestError(422, 'User_id is required')
            else:
                chat = query_by_id('chat_rel', chatrel_id)

                if chat is not None:
                    #Need new function
                    update_user(chatrel_id, request.form['user_id'])
                else:
                    raise RequestError(404, 'chat not found')
                chat = query_by_id('chat_rel', chatrel_id)
                return jsonify(chat)

    def patch(self, chatrel_id):
        """
        Handles the PATCH request given a certain login_id

        :param login_id: the id of the login to be patched
        :return:a response containing the JSON representation of the
            new login
        """

        if chatrel_id is None:
            raise RequestError(422, 'chatrel_id is required')
        else:
            if 'user_id' not in request.form:
                raise RequestError(422, 'User_id is required')
            else:
                chat = query_by_id('chat_rel', chatrel_id)

                if chat is not None:
                    #Need new function
                    update_user(chatrel_id, request.form['user_id'])
                else:
                    raise RequestError(404, 'chat not found')
                chat = query_by_id('chat_rel', chatrel_id)
                return jsonify(chat)


class MessageView(MethodView):
    def get(self, message_id):
        """
        Handle GET requests.
        Returns JSON representing all of the message if message_id is None, or
        a single message if message_id is not None.
        :param message_id: id of a message, or None for all messages
        :return: JSON response
        """
        if message_id is None:
            messages = get_all_rows('message')
            return jsonify(messages)
        else:
            messages = query_by_id('message', message_id)

            if messages is not None:
                response = jsonify(messages)
            else:
                raise RequestError(404, 'message not found')

            return response

    # The user_id should be provided through form data, not URL data. I
    # updated it to fix that -Morgan
    def post(self):
        """
        Handles a message request to insert a new city. Returns a JSON
        response representing the new message.
        The message name must be provided in the requests's form data.
        :return: a response containing the JSON representation of the message
        """
        if 'text' not in request.form:
            raise RequestError(422, 'text of message required')
        elif 'user_id' not in request.form:
            raise RequestError(422, 'user id required')
        else:
            response = jsonify(insert_message(request.form['text'],
                                              request.form['user_id']))
        return response

    def delete(self, message_id):
        """
        Handles a DELETE request given a certain message_id
        :return: a response containing the JSON representation of the
            old message
        """

        if message_id is None:
            raise RequestError(422, 'message id required')
        else:
            messages = query_by_id('message', message_id)

            if messages is not None:
                delete_item('message', message_id)
            else:
                raise RequestError(404, 'message not found')
        return jsonify(messages)

    def put(self, message_id):
        """
        Handles a PUT request given a certain message_id

        :param message_id: the id of the message to be put
        :return:a response containing the JSON representation of the
            new message
        """

        if message_id is None:
            raise RequestError(422, 'message id is required')
        else:
            if 'text' not in request.form:
                raise RequestError(422, 'message text is required')
            else:
                message = query_by_id('message', message_id)

                if message is not None:
                    update_message(request.form['text'],
                                  request.form['user'], message_id)
                else:
                    raise RequestError(404, 'message not found')

                message = query_by_id('message', message_id)
                return jsonify(message)

    def patch(self, message_id):
        """
        Handles the PATCH request given a certain message_id

        :param message_id: the id of the message to be patched
        :return:a response containing the JSON representation of the
            old message
        """

        if message_id is None:
            raise RequestError(422, 'message id is required')
        else:
            messages = query_by_id('message', message_id)

            if messages is None:
                raise RequestError(404, 'message not found')
            else:

                new_text = messages['text']
                if 'text' in request.form:
                    new_text = request.form['text']

                new_user = messages['user_id']
                if 'user' in request.form:
                    new_user = request.form['user']

                update_message(message_id, new_text, new_user)
                messages = query_by_id('messages', message_id)
                return jsonify(messages)


class UserView(MethodView):
    """
    This view handles all the /user/ requests.
    """

    def get(self, user_id):
        """
        Handle GET requests.

        Returns JSON representing all of the users if user_id is None, or a
        single user if user_id is not None.

        :param user_id: id of a user, or None for all users
        :return: JSON response
        """
        if user_id is None:
            user = get_all_rows('user')
            return jsonify(user)
        else:
            user = query_by_id('user', user_id)

            if user is not None:
                response = jsonify(user)
            else:
                raise RequestError(404, 'user not found')

            return response

    def post(self):
        """
        Handles a POST request to insert a new user. Returns a JSON
        response representing the new user.

        The user name must be provided in the requests's form data.

        :return: a response containing the JSON representation of the user
        """
        if 'name' not in request.form:
            raise RequestError(422, 'user name required')
        else:
            # THIS IS TEMPORARY, THE ACTUAL VERSION IS COMMENTED OUT
            response = jsonify(insert_user(request.form['name'], 1))
            # response = jsonify(insert_user(request.form['name'], login_id))
            # Need to get login_id

        return response

    def delete(self, user_id):
        """
        Handles a DELETE request given a certain user_id

        :param user_id: the id of the user to delete
        :return: a response containing the JSON representation of the
            old user
        """

        if user_id is None:
            raise RequestError(422, 'user name required')
        else:
            user = query_by_id('user', user_id)

            if user is not None:
                delete_item('user', user_id)
            else:
                raise RequestError(404, 'user not found')
        return jsonify(user)

    def put(self, user_id):
        """
        Handles a PUT request given a certain user_id

        :param user_id: the id of the user to be put
        :return:a response containing the JSON representation of the
            new user
        """

        if user_id is None:
            raise RequestError(422, 'User Id is required')
        else:
            if 'name' not in request.form:
                raise RequestError(422, 'User name is required')
            else:
                user = query_by_id('user', user_id)

                if user is not None:
                    update_user(user_id, request.form['name'])
                else:
                    raise RequestError(404, 'user not found')
                user = query_by_id('user', user_id)
                return jsonify(user)

    def patch(self, user_id):
        """
        Handles the PATCH request given a certain user_id

        :param user_id: the id of the user to be patched
        :return:a response containing the JSON representation of the
            new user
        """

        if user_id is None:
            raise RequestError(422, 'User Id is required')
        else:
            user = query_by_id('user', user_id)

            if user is None:
                raise RequestError(404, 'User not found')
            else:

                new_name = user['name']
                if 'name' in request.form:
                    new_name = request.form['name']

                update_user(user_id, new_name)
                user = query_by_id('user', user_id)
                return jsonify(user)


class ChatView(MethodView):
    def get(self, chat_id):
        """
        Handle GET requests.
        Returns JSON representing all of the message if chat_id is None, or a
        single chat if chat_id is not None.
        :param chat_id: id of a chat, or None for all chats
        :return: JSON response
        """
        if chat_id is None:
            chat = get_all_rows('chat')
            return jsonify(chat)
        else:
            chat = query_by_id('chat', chat_id)

            if chat is not None:
                response = jsonify(chat)
            else:
                raise RequestError(404, 'chat not found')

            return response

    def post(self):
        """
        Handles a message request to insert a new chat. Returns a JSON
        response representing the new chat.
        The must be provided in the requests's form data.

        :param user_id: the id of the user creating the chat.
        :return: a response containing the JSON representation of the message
        """
        if 'user_id' not in request.form:
            raise RequestError(422, 'user id required')
        else:
            #FIND SOMETHING THAT WORKS HERE
            response = jsonify(insert_message(request.form['text'], user_id))
        return response

    def delete(self, chat_id):
        """
        Handles a DELETE request given a certain chat_id

        :param chat_id: the id of the chat to be deleted
        :return: a response containing the JSON representation of the
            old message
        """

        if chat_id is None:
            raise RequestError(422, 'chat id required')
        else:
            chat = query_by_id('chat', chat_id)

            if chat is not None:
                delete_item('chat', chat_id)
            else:
                raise RequestError(404, 'chat not found')
        return jsonify(chat)


# Register MessageView as the handler for all the /message/ requests.
message_view = MessageView.as_view('message_view')
app.add_url_rule('/api/message/', defaults={'message_id': None},
                 view_func=message_view, methods=['GET'])
app.add_url_rule('/api/message/', view_func=message_view,
                 methods=['POST'])
# For this you would need to provide the user_id through the form data. URL
# values are only for message ID -Morgan
# app.add_url_rule('/message/<int:user_id>', view_func=message_view,
#                  methods=['POST'])  # Hey, should this be message? or POST
app.add_url_rule('/api/message/<int:message_id>', view_func=message_view,
                 methods=['GET'])
app.add_url_rule('/api/message/<int:message_id>', view_func=message_view,
                 methods=['DELETE'])
app.add_url_rule('/api/message/<int:message_id>', view_func=message_view,
                 methods=['PUT'])
app.add_url_rule('/api/message/<int:message_id>', view_func=message_view,
                 methods=['PATCH'])


# Register UserView as the handler for all the /user/ requests.
user_view = UserView.as_view('user_view')
app.add_url_rule('/api/user/', defaults={'user_id': None},
                 view_func=user_view, methods=['GET'])
app.add_url_rule('/api/user', view_func=user_view,
                 methods=['POST']) 
app.add_url_rule('/api/user/<int:user_id>', view_func=user_view,
                 methods=['GET'])
app.add_url_rule('/api/user/<int:user_id>', view_func=user_view,
                 methods=['DELETE'])
app.add_url_rule('/api/user/<int:user_id>', view_func=user_view,
                 methods=['PUT'])
app.add_url_rule('/api/user/<int:user_id>', view_func=user_view,
                 methods=['PATCH'])


# Register ChatView as the handler for all the /chat/ requests.
chat_view = ChatView.as_view('chat_view')
app.add_url_rule('/api/chat/', defaults={'chat_id': None},
                 view_func=chat_view, methods=['GET'])
app.add_url_rule('/api/chat/', view_func=chat_view,
                 methods=['POST'])
app.add_url_rule('/api/chat/<int:user_id>', view_func=chat_view,
                 methods=['GET'])
app.add_url_rule('/api/chat/<int:chat_id>', view_func=chat_view,
                 methods=['DELETE'])


# Register ChatRelView as the handler for all the /login/ requests.
chatrel_view = ChatRelView.as_view('chatrel_view')
app.add_url_rule('/chatrel/', defaults={'chatrel_id': None},
                 view_func=chatrel_view, methods=['GET'])
app.add_url_rule('/chatrel/', view_func=chatrel_view,
                 methods=['POST'])
app.add_url_rule('/chatrel/<int:chatrel_id>', view_func=chatrel_view,
                 methods=['GET'])
app.add_url_rule('/chatrel/<int:chatrel_id>', view_func=chatrel_view,
                 methods=['DELETE'])
app.add_url_rule('/chatrel/<int:chatrel_id>', view_func=chatrel_view,
                 methods=['PUT'])
app.add_url_rule('/chatrel/<int:chatrel_id>', view_func=chatrel_view,
                 methods=['PATCH'])