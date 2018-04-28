"""
A file containing functions for quering the WooMessages database.
"""

from database import get_db
from collections import OrderedDict


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


def get_user_by_username(username):
    """
    Returns a dictionary of one user

    :param username: the username of the user being searched for
    :return: a dictinary of the user
    """
    # Create cursor
    conn = get_db()
    cur = conn.cursor()

    # Get user by username
    cur.execute('SELECT * FROM user WHERE username = ?', (username,))
    results = cur.fetchall()

    if len(results) == 1:
        return dict(results[0])
    else:
        return None
