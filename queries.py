"""
WooMessages
CS 232
Final Project
AVI VAJPEYI, JEMAL JEMAL, ISAAC WEISS, MORGAN THOMPSON

A file containing functions for quering the WooMessages database.
"""

from database import *
from exception_classes import *
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
    :return: a dictionary of the user
    """
    # Create cursor
    conn = get_db()
    cur = conn.cursor()

    # Get user by username
    cur.execute('SELECT * FROM user WHERE username = ?', (username,))
    results = cur.fetchall()

    if len(results) > 0:
        print("get_user_by_username(username)")
        print(results[0]['username'])
        return dict(results[0])
    else:
        return None  # if none flash red


def get_user_id(username):
    """
    gets the user_id based off of their unique username

    :param username: the username of the user to get their id
    :return: the id of the user, or a request error if user doesn't exist
    """

    conn = get_db()
    cur = conn.cursor()

    query = '''
        SELECT id FROM user WHERE username = ?
    '''

    cur.execute(query, (username,))

    user_id = cur.fetchone()[0]

    if user_id is None:
        raise RequestError(422, 'User does not exist')
    else:
        return user_id


def get_messages_in_chatroom(chat_id):
    """
    Gets all of the messages in a chatroom, ordered by time

    :param chat_id: the id of the chat with the messages
    :return: an ordered dictionary with the messages.
    """

    conn = get_db()
    cur = conn.cursor()

    list_of_messages = OrderedDict()

    query = '''
        SELECT user.name AS "name", message.message AS "message",
        message.time AS "time", chat.title AS "title", chat.time AS "created"
        FROM user, message, chat
        WHERE chat.id = ? AND message.chat_id = ? AND user.id = message.user_id
        ORDER BY time
    '''

    for row in cur.execute(query, (chat_id, chat_id)):

        message = row['message']
        name = row['name']
        time = row['time']

        if message not in list_of_messages:
            list_of_messages[name, message, time] = []

        list_of_messages[name, message, time].append(row)

    return list_of_messages


def get_chat_room_name(chat_id):
    """
    A function that finds the name of a chat room given a specific id

    :param chat_id: the id of a chat
    :return: the name of the chatroom
    """

    conn = get_db()
    cur = conn.cursor()

    query = '''
        SELECT chat.title AS "chat_title"
        FROM chat
        WHERE chat.id = ?
    '''

    cur.execute(query, (chat_id,))

    result = cur.fetchone()[0]

    if result is None:
        raise RequestError(422, 'chat does not exist')
    else:
        return result


def get_chat_rooms(user_id):
    """
    gets all of the chat rooms that a user is in

    :param user_id: the id of the user with which to query to get all of the
        chat rooms
    :return: an ordered dictionary containing the chat rooms
    """

    conn = get_db()
    cur = conn.cursor()

    room_data = OrderedDict()

    query = '''
        SELECT chat.title AS "title", user.name AS "participants",
        chat.time AS "create_date", chat.id AS "id"
        FROM chat, chat_rel, user
        WHERE chat_rel.user_id = user.id
        AND chat_rel.chat_id = chat.id
        AND user.id = ?
        ORDER BY chat.time, chat.title;
    '''

    for row in cur.execute(query, (user_id,)):
        room_name = row['title']
        room_date = row['create_date']
        room_id = row['id']

        if room_name not in room_data:
            room_data[room_name, room_date, room_id] = []

        room_data[room_name, room_date, room_id].append(row)

    return room_data


def get_participants_in_chat(chat_id):
    """
    A function that will return an ordered dictionary of participants in a chat

    :param chat_id: the id of the chat to find participants in
    :return: an ordered dictionary of participants
    """

    conn = get_db()
    cur = conn.cursor()

    participant_data = OrderedDict()

    query = '''
        SELECT user.name AS "name" FROM user, chat_rel
        WHERE user.id = chat_rel.user_id AND chat_rel.chat_id = ?
        ORDER BY name
    '''

    for row in cur.execute(query, (chat_id,)):
        participant = row['name']

        if participant not in participant_data:
            participant_data[participant] = []

        participant_data[participant].append(row)

    return participant_data


def get_room_info(chatroom_id):
    """
    Will get the title and time of creation for a chatroom based off of an id

    :param chatroom_id: the id of the chatroom to collect info for
    :return: an ordered dictionary of the chatroom information
    """

    conn = get_db()
    cur = conn.cursor()

    room_data = OrderedDict()

    query = '''
        SELECT chat.title AS "title", chat.time AS "time"
        FROM chat WHERE chat.id = ? ORDER BY time
    '''

    for row in cur.execute(query, (chatroom_id,)):
        room_date = row['time']
        room_title = row['title']

        if room_date not in room_data:
            room_data[room_title, room_date] = []

        room_data[room_title, room_date].append(row)

    return room_data


def delete_user_from_chat(username, chat_id):
    """
    This function removes a user from a chat. If there are no users in a chat,
    the chat will also be deleted.

    :param username: the username of the user to be deleted
    :param chat_id: that chat id from which to delete a user
    """

    conn = get_db()
    cur = conn.cursor()

    user_id = get_user_id(username)

    cur.execute('DELETE FROM chat_rel WHERE user_id = ? AND chat_id = ?',
                (user_id, chat_id))
    conn.commit()


def insert_chat_room(title, username_list):
    """
    will take information from the HTML to create a new chatroom

    :param title: the title of the chat
    :param username_list: a list of usernames to be added
    :return: null
    """

    # check if all users are valid users
    verified_user = []
    for username in username_list:
        search_result = get_user_by_username(username)
        if search_result is not None:
            verified_user.append(username)
        else:
            return username  # return invalid username

    # since valid users, add chat and add users to chat
    chat = insert_chat(title, get_date())
    chat_id = chat['id']
    for username in verified_user:
        insert_chat_rel(get_user_id(username), chat_id)

    return chat_id  # no error!


def delete_user_from_chat(username, chat_id):
    """
    This function removes a user from a chat. If there are no users in a chat,
    the chat will also be deleted.

    :param username: the username of the user to be deleted
    :param chat_id: the id of the chat
    """

    conn = get_db()
    cur = conn.cursor()

    user_id = get_user_id(username)

    cur.execute('DELETE FROM chat_rel WHERE user_id = ? AND chat_id = ?',
                (user_id, chat_id))
    conn.commit()


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
