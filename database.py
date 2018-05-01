"""
WooMessages
CS 232
Final Project
AVI VAJPEYI, JEMAL JEMAL, ISAAC WEISS, MORGAN THOMPSON

A file containing functions for database creation and the functions required
for updating/inserting/deleting from the database's tables.
"""

from flask import Flask, g
import os
import sqlite3
import csv
import datetime
# a hash algorithm that encrypts password
from passlib.hash import sha256_crypt


app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.root_path, 'WooMessages.sqlite')


def init_db():
    """
    This will initialize the database and create the following tables: user,
    chat, message, chat_rel
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
            chat_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES user(id)
            FOREIGN KEY(chat_id) REFERENCES chat(id)
        );
        CREATE TABLE chat(
            id INTEGER PRIMARY KEY,
            title TEXT,
            time TEXT
        );
        CREATE TABLE message (
            id INTEGER PRIMARY KEY,
            message TEXT,
            time TEXT,
            user_id INTEGER,
            chat_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES user(id),
            FOREIGN KEY(chat_id) REFERENCES chat(id)
        );
    '''

    conn.cursor().executescript(query)


def convert_csv_to_sqlite(filename):
    """
    Initialises a db if non-existent and populates the db with data from a CSV
    file.

    :param filename: the CSV filename where data is stored. The data must be
    in the columns titled 'Username', 'Password', 'Name', 'Email',
    'Chat_Title', 'Title' and 'Message'
    :return: None
    """

    init_db()  # creates database tables if non-existant

    for row in csv_row_generator(filename):

        insert_table_info(username=row['Username'],
                          password=row['Password'],
                          name=row['Name'],
                          email=row['Email'],
                          chat_title=row['Chat_Title'],
                          message_time=row['Time'],
                          message_content=row['Message'],
                          )


def csv_row_generator(filename):
    """
    Helper function to read row line of the CSV

    :param filename: the CSV filename where data is stored.
    :return: one row of the data
    """
    with open(filename, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


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

    return now.strftime("%m/%d/%Y %H:%M")


def insert_user(name, email, username, password):
    """
    Insert a user into the database.
    Returns a dictionary representing the newly inserted row.

    :param name: user's name
    :param email: user's email
    :param username: user's username
    :param password: user's password
    :return: inserted row as a dictionary
    """

    # hash and salt password
    password = sha256_crypt.encrypt(str(password))

    # Create cursor
    conn = get_db()
    cur = conn.cursor()

    # Execute query
    cur.execute('INSERT OR IGNORE INTO '
                'user(name, email, username, password)'
                'VALUES(?, ?, ?, ?)', (name, email, username, password))

    # Commit to DB
    conn.commit()

    cur.execute('SELECT * FROM user WHERE username = ?', (username,))

    return dict(cur.fetchone())


def insert_message(message, time, user_id, chat_id):
    """
    Insert a message into the database. Keeps track of the user who sent the
    message, the chat in which the message was sent and the time when the
    message was sent.
    Returns a dictionary representing the newly inserted row.

    :param message: The content of the message being sent
    :param time: the time the message was sent
    :param user_id: the ID of the user who sent the message
    :param chat_id: the ID of the chat the message is sent to
    :return:
    """
    conn = get_db()
    cur = conn.cursor()

    cur.execute('INSERT OR IGNORE INTO '
                'message(message, time, user_id, chat_id)'
                'VALUES(?, ?, ?, ?)', (message, time, user_id, chat_id))

    conn.commit()

    message_id = cur.lastrowid

    cur.execute('SELECT * FROM message WHERE id = ?', (message_id,))

    return dict(cur.fetchone())


def insert_chat(title, time):
    """
    Insert a chat into the database ONLY IF a chat with the same title does
    not already exist.

    Returns a dictionary representing the newly inserted row.

    :param title: chat title
    :param time: time the first message was sent in this chat
    :return: inserted row as a dictionary
    """
    conn = get_db()
    cur = conn.cursor()

    chat_id = check_chat(title)  # check if this chat already exists

    if chat_id is None:
        cur.execute('INSERT INTO '
                    'chat(title, time)'
                    'VALUES(?, ?)', (title, time))
        conn.commit()
        chat_id = cur.lastrowid

    cur.execute('SELECT * FROM chat WHERE id = ?', (chat_id,))

    result = dict(cur.fetchone())

    return result


def insert_chat_rel(user_id, chat_id):
    """
    Insert a chat relationship into the database that will link which user
    belongs to which chat

    :param user_id: ID of the user
    :param chat_id: ID of the chat
    :return: inserted row as a dictionary
    """
    conn = get_db()
    cur = conn.cursor()

    chat_rel_id = check_chat_rel(user_id, chat_id)

    if chat_rel_id is None:
        cur.execute('INSERT INTO '
                    'chat_rel(user_id, chat_id) '
                    'VALUES(?, ?)', (user_id, chat_id))
        # we cannot use INSERT OR IGNORE INTO...

        conn.commit()

        chat_rel_id = cur.lastrowid

    cur.execute('SELECT * FROM chat_rel WHERE id = ?', (chat_rel_id,))

    return dict(cur.fetchone())


def insert_table_info(username, password, name, email,
                      chat_title,
                      message_time, message_content):
    """
    Inserts data into tables of our database.

    A helper function that inserts data for a users data and chat data

    :param username: user's username
    :param password: user's password
    :param name: user's name
    :param email: user's email
    :param chat_title: the chat's title
    :param message_time: the timestamp of the message
    :param message_time: the content of the message
    :return: None
    """

    user = insert_user(name, email, username, password)
    chat = insert_chat(chat_title, message_time)

    chat_rel = insert_chat_rel(user["id"], chat["id"])

    message = insert_message(message_content, message_time,
                             user['id'], chat['id'])


def update_message(text, user_id, message_id):
    """
    Updates the contents of a message. Provides the ability to change the
    user id of where the message is delivered to.

    :param text: the contents of a message
    :param user_id: ID of the message receiver
    :param message_id: ID of the message
    :return: dictionary containing updated message
    """
    conn = get_db()
    cur = conn.cursor()

    query = '''
        UPDATE message SET message = ?, user_id = ? WHERE id = ?
    '''

    if cur.execute('SELECT * FROM message WHERE id = ?', (message_id,)) is None:
        raise RequestError(404, 'message not found')
    else:
        cur.execute(query, (text, user_id, message_id))
        conn.commit()

    cur.execute('SELECT * FROM message WHERE id = ?', (message_id,))

    return dict(cur.fetchone())


def update_user(user_id, name, email, username, password):
    """
    Updates a username given a specific user_id

    :param user_id: the id of the user to be updated
    :param name: the updated username
    :param email: the updated email
    :param username: the updated username
    :param password: the updated password
    :return: a dictionary representing the new, updated user
    """

    conn = get_db()
    cur = conn.cursor()

    password = sha256_crypt.encrypt(str(password))

    query = '''
        UPDATE user SET name = ?, email = ?, username = ?, password = ? WHERE 
        id = ?
    '''

    if cur.execute('SELECT * FROM user WHERE id = ?', (user_id,)) is None:
        raise RequestError(404, 'user not found')
    else:
        cur.execute(query, (name, email, username, password, user_id))
        conn.commit()

    cur.execute('SELECT * FROM user WHERE id = ?', (user_id,))

    return dict(cur.fetchone())


def update_chat(chat_id, title):
    """
    Updates a chat title given a specific chat_id

    :param chat_id: the id of the chat to be updated
    :param title: the updated chat title
    :return: a dictionary representing the updated chat title
    """

    conn = get_db()
    cur = conn.cursor()

    query = '''
        UPDATE chat SET title = ? WHERE id = ?
    '''

    if cur.execute('SELECT * FROM chat WHERE id = ?', (chat_id,)) is None:
        raise RequestError(404, 'chat not found')
    else:
        cur.execute(query, (title, chat_id))
        conn.commit()

    cur.execute('SELECT * FROM chat WHERE id = ?', (chat_id,))

    return dict(cur.fetchone())


def delete_item(table_name, item_id):
    """
    This function deletes items from a table based on their item_id

    :param table_name: name of table which has an item to delete
    :param item_id: item which to delete
    :return: NONE
    """
    conn = get_db()
    cur = conn.cursor()

    query = 'DELETE FROM {} WHERE id = ?'.format(table_name)

    cur.execute(query, (item_id,))
    conn.commit()

    return None


def check_chat(title):
    """
    This function will only be called when filling a csv. That is to ensure
    that multiple chats aren't created when originally populating the database

    :param title: the title of a chat
    :return: None if the chat doesn't exist. Returns the chat id otherwise.
    """

    conn = get_db()
    cur = conn.cursor()

    query = '''
    SELECT * FROM chat WHERE title = ?
    '''

    cur.execute(query, (title,))

    content = cur.fetchone()
    if content is not None:
        return content['id']
    else:
        return None  # none instead of 0 because 0 might be a chat_id


def check_chat_rel(user_id, chat_id):
    """
    Given a user_id and chat_id, this function returns the chat relationship
    id of the chat that a user belongs to

    Returns none if the user is not in the chat

    :param user_id: ID of the user
    :param chat_id: ID of the chat
    :return: chat_rel_id if the given user is in a given chat, none if user
             is not in the chat
    """

    conn = get_db()
    cur = conn.cursor()

    query = '''
        SELECT * FROM chat_rel
        WHERE user_id = ?
        AND chat_id = ?;
    '''

    # print("UID:{}, CID:{}".format(user_id, chat_id))
    cur.execute(query, (user_id, chat_id))

    content = cur.fetchone()

    if content is not None:
        return content['id']
    else:
        return None  # none instead of 0 because 0 might be a chat id
