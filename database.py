"""

A file containing functions for database creation and the functions required
for updating/inserting/deleting from the database's tables.
"""

from flask import Flask, g
import os
import sqlite3
import csv

import datetime

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.root_path, 'WooMessages.sqlite')


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
    Initialises a db if non-existant and populates the db with data from a CSV
    file.

    :param filename: the CSV filename where data is stored. The data must be in
    the columns titled Artist_Name, Artist_Age, Album_Name Track_Name and
    Track_Duration
    :return: None
    """

    init_db()  # creates database tables if non-existant

    for row in csv_row_generator(filename):
        user_id = insert_user(row['Name'], row['Email'], row['Username'],
                              row['Password'])
        content = user_id.json()
        user_id = content['username']
        if check_chat(row['Title']) is 0:
            chat_id = insert_chat(row['Title'], row['Time'])
            content = chat_id.json()
            chat_id = content['id']
        else:
            chat_id =
        insert_message(row['Message'], row['Time'], user_id, chat_id)
        insert_chat_rel(user_id, chat_id)


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

    return now.strftime("%Y-%m-%d %H:%M")


def insert_user(name, email, username, password):
    conn = get_db()
    cur = conn.cursor()

    cur.execute('INSERT INTO user(name, email, username, password)'
                'VALUES(?, ?, ?, ?)', (name, email, username, password))

    conn.commit()

    user_id = cur.lastrowid

    cur.execute('SELECT * FROM user WHERE id = ?', (user_id,))

    return dict(cur.fetchone())


def insert_message(message, time, user_id, chat_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute('INSERT INTO message(message, time, user_id, chat_id)'
                'VALUES(?, ?, ?, ?)', (message, time, user_id, chat_id))

    conn.commit()

    message_id = cur.lastrowid

    cur.execute('SELECT * FROM message WHERE id = ?', (message_id,))

    return dict(cur.fetchone())


def insert_chat(title, time):
    conn = get_db()
    cur = conn.cursor()

    cur.execute('INSERT INTO chat(title, time)'
                'VALUES(?, ?)', (title, time))

    conn.commit()

    chat_id = cur.lastrowid

    cur.execute('SELECT * FROM chat WHERE id = ?', (chat_id,))

    return dict(cur.fetchone())


def insert_chat_rel(user_id, chat_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute('INSERT INTO chat_rel(user_id, chat_id)'
                'VALUES(?, ?)', (user_id, chat_id))

    conn.commit()

    chat_rel_id = cur.lastrowid

    cur.execute('SELECT * FROM chat_rel WHERE id = ?', (chat_rel_id,))

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


def check_chat(title):
    """
    THis function will only be called when filling a csv. That is to ensure
    that multiple chats aren't created when originally populating the database

    :param title: the title of a chat
    :return: 0 if the chat doesn't exist. the chat id otherwise.
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
        return 0
