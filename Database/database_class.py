__author__ = 'Vajpeyi'



class WooMessageDB:
    """
    Car Store Database Class

    This class provides an interface for interacting with a database of
    car stores.

    Methods
    -------
    __init__(self, file)
        the Car Store Database class constructor
    create_tables(self)
        returns Model object name
    insert_model(self, model_name, model_type):
        returns Model object type
    insert_car(self, model_id, colour, year)
        inserts a car into the database
    insert_store(self, store_name, store_address, manufacturer_id, car_id)
        inserts a store into the database
    insert_manufacturer(self, manufacturer_name)
        inserts a manufacturer into the database
    insert_table_info(self, model_name, model_type, colour, year,
    manufacturer_name, store_name, store_address )
        Helper function to call methods to insert data into database
    get_store_cars_by_store_name(self, name)
        Queries for the cars in a store
    """

    ##CONSTRUCTOR##############################################################

    def __init__(self, filename):
        """
        Constructor for Car Store Database object.

        Constructor for the Car Store Database. Provided a car store database
        filename, the constructor creates a cursor in the database. If a
        database file does not exist, the constructor creates a file and
        generates the care store tables in it. Also turns foreign keys on.

        :param filename: File name of the car store database.
        :return: None.
        """
        if not os.path.isfile(filename):
            print("{} does not exist, creating it now.".format(filename))
            self._conn = sqlite3.connect(filename)
            self.create_tables()
        else:
            self._conn = sqlite3.connect(filename)
        cur = self._conn.cursor()
        cur.execute('PRAGMA foreign_keys = ON')

    ##CREATE TABLES############################################################

    def create_tables(self):
        """Creates tables for our database.

        Creates the Manufacturer, Store, Car and Model tables if they do not
        already exist.

        :return: None
        """
        cur = self._conn.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS Manufacturer
                        (
                        id INTEGER PRIMARY KEY,
                        name TEXT
                        );""")

        # cur.execute("""CREATE TABLE Supplier
        #                 (
        #                 id INTEGER PRIMARY KEY,
        #                 name TEXT UNIQUE,
        #                 );""")

        cur.execute("""CREATE TABLE IF NOT EXISTS Model
                        (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        type TEXT
                        );""")

        cur.execute("""CREATE TABLE IF NOT EXISTS Car
                        (
                        id INTEGER PRIMARY KEY,
                        model_id INTEGER,
                        colour TEXT,
                        year INTEGER,
                        FOREIGN KEY(model_id) REFERENCES Model(id)
                        );""")

        cur.execute("""CREATE TABLE IF NOT EXISTS Store
                        (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        address TEXT,
                        manufacturer_id INTEGER,
                        car_id INTEGER,
                        FOREIGN KEY(manufacturer_id) REFERENCES
                        Manufacturer(id),
                        FOREIGN KEY(car_id) REFERENCES Car(id)
                        );""")
        self._conn.commit()

    ##INSERTS##################################################################

    def insert_user(self, name, email, username, password):
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
        cur = self._conn.cursor()

        # Execute query
        cur.execute('INSERT OR IGNORE INTO '
                    'user(name, email, username, password)'
                    'VALUES(?, ?, ?, ?)', (name, email, username, password))

        # Commit to DB
        conn.commit()

        cur.execute('SELECT * FROM user WHERE username = ?', (username,))

        return dict(cur.fetchone())


    def insert_message(self, message, time, user_id, chat_id):
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
	cur = self._conn.cursor()

        cur.execute('INSERT OR IGNORE INTO '
                    'message(message, time, user_id, chat_id)'
                    'VALUES(?, ?, ?, ?)', (message, time, user_id, chat_id))

        conn.commit()

        message_id = cur.lastrowid

        cur.execute('SELECT * FROM message WHERE id = ?', (message_id,))

        return dict(cur.fetchone())


    def insert_chat(self, title, time):
        """
        Insert a chat into the database ONLY IF a chat with the same title does
        not already exist.

        Returns a dictionary representing the newly inserted row.

        :param title: chat title
        :param time: time the first message was sent in this chat
        :return: inserted row as a dictionary
        """
	cur = self._conn.cursor()

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


    def insert_chat_rel(self, user_id, chat_id):
        """
        Insert a chat relationship into the database that will link which user
        belongs to which chat

        :param user_id: ID of the user
        :param chat_id: ID of the chat
        :return: inserted row as a dictionary
        """
	cur = self._conn.cursor()

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


    def insert_chat_room(self, title, username_list):
        """
        Takes information from the HTML to create a new chat room

        :param title: the title of the chat
        :param username_list: a list of username's to be added
        :return: ID of the chat room
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

    def insert_table_info(self, username, password, name, email,
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

    ##UPDATES##################################################################

    def update_message(self, text, user_id, message_id):
        """
        Updates the contents of a message. Provides the ability to change the
        user id of where the message is delivered to.

        :param text: the contents of a message
        :param user_id: ID of the message receiver
        :param message_id: ID of the message
        :return: dictionary containing updated message
        """
	cur = self._conn.cursor()

        query = '''
            UPDATE message SET message = ?, user_id = ? WHERE id = ?
        '''

        cur.execute(query, (text, user_id, message_id))
        conn.commit()

        cur.execute('SELECT * FROM message WHERE id = ?', (message_id,))

        return dict(cur.fetchone())


    def update_user(self, user_id, name):
        """
        Updates a username given a specific user_id

        :param user_id: the id of the user to be updated
        :param name: the updated username
        :return: a dictionary representing the new, updated user
        """

	cur = self._conn.cursor()

        query = '''
            UPDATE user SET name = ? WHERE id = ?
        '''

        cur.execute(query, (name, user_id))
        conn.commit()

        cur.execute('SELECT * FROM user WHERE id = ?', (user_id,))

        return dict(cur.fetchone())


    def update_chat(self, chat_id, title):
        """
        Updates a chat title given a specific chat_id

        :param chat_id: the id of the chat to be updated
        :param title: the updated chat title
        :return: a dictionary representing the updated chat title
        """

	cur = self._conn.cursor()

        query = '''
            UPDATE chat SET title = ? WHERE id = ?
        '''

        cur.execute(query, (title, chat_id))
        conn.commit()

        cur.execute('SELECT * FROM chat WHERE id = ?', (chat_id,))

        return dict(cur.fetchone())

    ##DELETES##################################################################

    def delete_user_from_chat(self, username, chat_id):
        """
        This function removes a user from a chat. If there are no users in a chat,
        the chat will also be deleted.

        :param username: the username of the user to be deleted
        :param chat_id: that chat id from which to delete a user
        """

	cur = self._conn.cursor()

        user_id = get_user_id(username)

        cur.execute('DELETE FROM chat_rel WHERE user_id = ? AND chat_id = ?',
                    (user_id, chat_id))
        conn.commit()


    def delete_user_from_chat(self, username, chat_id):
        """
        This function removes a user from a chat. If there are no users in a chat,
        the chat will also be deleted.

        :param username: the username of the user to be deleted
        :param chat_id: the id of the chat
        """

	cur = self._conn.cursor()

        user_id = get_user_id(username)

        cur.execute('DELETE FROM chat_rel WHERE user_id = ? AND chat_id = ?',
                    (user_id, chat_id))
        conn.commit()


    def delete_item(self, table_name, item_id):
        """
        This function deletes items with item_id from table_name

        :param table_name: the table which has an item to delete
        :param item_id: it item which to delte
        :return: NONE
        """
	cur = self._conn.cursor()

        query = 'DELETE FROM {} WHERE id = ?'.format(table_name)

        cur.execute(query, (item_id,))
        conn.commit()

        return None

    ##QUERIES##################################################################

    def query_by_id(self, table_name, item_id):
        """
        Get a row from a table that has a primary key attribute named id.

        Returns None of there is no such row.

        :param table_name: name of the table to query
        :param item_id: id of the row
        :return: a dictionary representing the row, and None if there is no row
        """
	cur = self._conn.cursor()

        query = 'SELECT * FROM {} WHERE id = ?'.format(table_name)

        cur.execute(query, (item_id,))

        row = cur.fetchone()

        if row is not None:
            return dict(row)
        else:
            return None


    def get_all_rows(self, table_name):
        """
        Returns all of the rows from a table as a list of dictionaries. This is
        suitable for passing to jsonify().

        :param table_name: name of the table
        :return: list of dictionaries representing the table's rows
        """

	cur = self._conn.cursor()

        query = 'SELECT * FROM {}'.format(table_name)

        results = []

        for row in cur.execute(query):
            results.append(dict(row))

        return results


    def get_user_by_username(self, username):
        """
        Returns a dictionary of one user's details

        :param username: the username of the user being searched for
        :return: a dictionary of the user's details
        """
        # Create cursor
	cur = self._conn.cursor()

        # Get user by username
        cur.execute('SELECT * FROM user WHERE username = ?', (username,))
        results = cur.fetchall()

        if len(results) > 0:
            return dict(results[0])
        else:
            return None  # if none flash red on the HTML


    def get_user_id(self, username):
        """
        Gets the user_id of a user from the username that is passed

        :param username: the username of the user to get their id
        :return: the id of the user, or a request error if user doesn't exist
        """

	cur = self._conn.cursor()

        query = '''
            SELECT id FROM user WHERE username = ?
        '''

        cur.execute(query, (username,))

        user_id = cur.fetchone()[0]

        if user_id is None:
            raise RequestError(422, 'User does not exist')
        else:
            return user_id


    def get_messages_in_chatroom(self, chat_id):
        """
        Gets all of the messages in a chatroom, ordered by time

        :param chat_id: the id of the chat with the messages
        :return: an ordered dictionary with the messages.
        """

	cur = self._conn.cursor()

        list_of_messages = OrderedDict()

        query = '''
            SELECT user.name AS "name", message.message AS "message",
            message.time AS "time", chat.title AS "title", chat.time AS "created"
            FROM user, message, chat
            WHERE chat.id = ? AND message.chat_id = ? AND
            user.id = message.user_id ORDER BY time
        '''

        for row in cur.execute(query, (chat_id, chat_id)):

            message = row['message']
            name = row['name']
            time = row['time']

            if message not in list_of_messages:
                list_of_messages[name, message, time] = []

            list_of_messages[name, message, time].append(row)

        return list_of_messages


    def get_chat_room_name(self, chat_id):
        """
        This function finds the name of a chat room given a specific chat id

        :param chat_id: ID of a chat
        :return: name of the chat room
        """

	cur = self._conn.cursor()

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


    def get_chat_rooms(self, user_id):
        """
        Gets all of the chat rooms that a user is a part of

        :param user_id: ID of the user
        :return: an ordered dictionary containing the chat rooms
        """

	cur = self._conn.cursor()

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


    def get_participants_in_chat(self, chat_id):
        """
        A function that returns an ordered dictionary of participants in a chat

        :param chat_id: ID of a chat
        :return: an ordered dictionary of participants
        """

	cur = self._conn.cursor()

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


    def get_room_info(self, chatroom_id):
        """
        Gets the title and time of creation for a chat room based on a chatroom_id

        :param chatroom_id: ID of the chat room to collect info for
        :return: an ordered dictionary of the chat room information
        """

	cur = self._conn.cursor()

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

    ##HELPERS##################################################################

    def check_chat(self, title):
        """
        This function will only be called when filling a csv. That is to ensure
        that multiple chats aren't created when originally populating the database

        :param title: the title of a chat
        :return: None if the chat doesn't exist. Returns the chat id otherwise.
        """

	cur = self._conn.cursor()

        query = '''
        SELECT * FROM chat WHERE title = ?
        '''

        cur.execute(query, (title,))

        content = cur.fetchone()
        if content is not None:
            return content['id']
        else:
            return None  # none instead of 0 because 0 might be a chat_id


    def check_chat_rel(self, user_id, chat_id):
        """
        Given a user_id and chat_id, this function returns the chat relationship
        id of the chat that a user belongs to

        Returns none if the user is not in the chat

        :param user_id: ID of the user
        :param chat_id: ID of the chat
        :return: chat_rel_id if the given user is in a given chat, none if user
                 is not in the chat
        """

	cur = self._conn.cursor()

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
