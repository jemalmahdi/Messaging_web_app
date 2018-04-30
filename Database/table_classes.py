
class Message:
    """
    An object from this class represents a message. In particular it stores the
    message content, the user sender, the time and chat the message is sent to.
    """

    def __init__(self, message, time, chat, user):
        """
        Construct a Message object using its message content,
        the sender user, and the chat and time the message is sent.

        :param message: message content being sent
        :param time: time the message is sent
        :param chat: chat the message is sent in
        :param user: the user sending the message
        """
        self._message = message
        self._time = time
        self._chat = chat
        self._user = user

    def __repr__(self):
        """
        Create a string representation of a message.

        The format is as follows:

           <user>: "<message>" @ <time> in <chat>

        :return: the string representation of the message
        """
        return '{}: \"{}\" @ {} in {}'.format(self._user, self._message,
                                              self._time, self._chat)

    def get_user(self):
        return self._user

    def get_message(self):
        return self._message

    def get_time(self):
        return self._time

    def get_chat(self):
        return self._chat




class Chat:
    """
    An object from this class represents a chat. In particular it stores the
    title and time of a chat.
    """

    def __init__(self, title, time):
        """
        Construct a Chat object using its title and time of creation

        :param title: title of chat
        :param time: time of creation for chat
        """
        self._title = title
        self._time = time

    def __repr__(self):
        """
        Create a string representation of a chat.

        The format is as follows:

           <title>, a chat created on <time>

        :return: the string representation of the chat
        """
        return '{}, a chat created on {}'.format(self._title, self._time)

    def get_title(self):
        return self._title

    def get_time(self):
        return self._time


class User:
    """
    An object from this class represents a user. In particular it stores the
    name, email, username and password (ENRYPTED) of the user.
    """

    def __init__(self, name, email, username, password):
        """
        Construct a User object using its name, email, username, password.

        :param name: name of the user
        :param email: email of the user
        :param username: unique username of the user
        :param password: the password of the user
        """
        self._name = name
        self._email = email
        self._username = username
        self._password = password

    def __repr__(self):
        """
        Create a string representation of a user.

        The format is as follows:

           <username>: <name> whose email is <email> and password is <password>

        :return: the string representation of the user
        """
        return '<username>: <name> whose email is <email>' \
               ' and password is <password>'.format(self._username, self._name,
                                              self._email, self._password)

    def get_username(self):
        return self._username

    def get_name(self):
        return self._name

    def get_email(self):
        return self._email

    def get_password(self):
        return self._password


class ChatRel:
    """
    An object from this class represents a chat relationship. In particular
    it stores the ID's that represent which user belongs to which chat
    """

    def __init__(self, user, chat):
        """
        Construct a Chat Relationship object using user id and chat id

        :param user: ID of user
        :param chat: ID of chat
        """
        self._user = user
        self._chat = chat

    def __repr__(self):
        """
        Create a string representation of a chat relationship.

        The format is as follows:

           <user> belongs to <chat>

        :return: the string representation of the chat relationship
        """
        return '{} belongs to {}'.format(self._user, self._chat)

    def get_user_id(self):
        return self._user

    def get_chat_id(self):
        return self._chat
    
