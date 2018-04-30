
class Message:
    """
    An object from this class represents a dog. In particular it stores the
    name, age, and breed.
    """

    def __init__(self, message, time, chat, user):
        """
        Construct a Message object using its message content,
        the sender user, and the chat and time the message is sent.

        :param message: message 
        :param time: age of the dog
        :param chat: breed of the dog
        :param user:
        """
        self._message = message
        self._time = time
        self._chat = chat
        self._user = user

    def __repr__(self):
        """
        Create a string representation of a dog.

        The format is as follows:

           <name>, a <age> year old <breed>

        :return: the string representation of the dog
        """
        return '{}, a {} year old {}'.format(self._name, self._age,
                                             self._breed)

    def get_name(self):
        return self._name

    def get_age(self):
        return self._age

    def increment_age(self):
        self._age += 1

    def get_breed(self):
        return self._breed



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
