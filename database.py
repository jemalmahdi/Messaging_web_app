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
        );
        CREATE TABLE chat(
            title TEXT,
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
        insert_table_info(artist_name=row['Artist_Name'],
                          artist_age=row['Artist_Age'],
                          album_name=row['Album_Name'],
                          track_name=row['Track_Name'],
                          track_duration=row['Track_Duration'], )


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
