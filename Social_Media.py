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
        DROP TABLE IF EXISTS login;
        DROP TABLE IF EXISTS user;
        DROP TABLE IF EXISTS chat_rel;
        DROP TABLE IF EXISTS chat;
        DROP TABLE IF EXISTS message;
        CREATE TABLE login(
            id INTEGER PRIMARY KEY,
            user_name TEXT UNIQUE,
            password TEXT
        );
        CREATE TABLE user (
            id INTEGER PRIMARY KEY,
            name TEXT,
            login_id INTEGER,
            FOREIGN KEY(login_id) REFERENCES login(id)           
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
    conn = get_db()
    cur = conn.cursor()

    query = '''
        INSERT INTO message(message, time, user_id) VALUES(?, ?, ?)
    '''

    cur.execute(query, (message, get_date(), user_id))
    conn.commit()

    cur.execute('SELECT * FROM message WHERE id = ?', (cur.lastrowid,))

    return dict(cur.fetchone())


def update_message(text, user_id, message_id):
    conn = get_db()
    cur = conn.cursor()

    query = '''
        UPDATE message SET text = ? AND user_id = ? WHERE id = ?
    '''

    cur.execute(query, (text, user_id, message_id))
    conn.commit()

    cur.execute('SELECT * FROM message WHERE id = ?', (message_id,))

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


class MessageView(MethodView):
    def get(self, message_id):
        """
        Handle GET requests.

        Returns JSON representing all of the message if message_id is None, or a
        single message if message_id is not None.

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

    def post(self, user_id):
        """
        Handles a message request to insert a new city. Returns a JSON
        response representing the new message.

        The message name must be provided in the requests's form data.

        :return: a response containing the JSON representation of the message
        """
        if 'text' not in request.form:
            raise RequestError(422, 'text of message required')
        else:
            response = jsonify(insert_message(request.form['text'], user_id))
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
                    new_name = request.form['text']

                new_user = messages['user_id']
                if 'user' in request.form:
                    new_user = request.form['user']

                update_message(message_id, new_text, new_user)
                messages = query_by_id('messages', message_id)
                return jsonify(messages)



# Register MessageView as the handler for all the /message/ requests. For
# more info
# about what is going on here, see http://flask.pocoo.org/docs/0.12/views/
message_view = MessageView.as_view('message_view')
app.add_url_rule('/message/', defaults={'message_id': None},
                 view_func=message_view, methods=['GET'])
app.add_url_rule('/message/<int:user_id>', view_func=message_view,
                 methods=['message'])
app.add_url_rule('/message/<int:message_id>', view_func=message_view,
                 methods=['GET'])
app.add_url_rule('/message/<int:message_id>', view_func=message_view,
                 methods=['DELETE'])
app.add_url_rule('/message/<int:message_id>', view_func=message_view,
                 methods=['PUT'])
app.add_url_rule('/message/<int:message_id>', view_func=message_view,
                 methods=['PATCH'])