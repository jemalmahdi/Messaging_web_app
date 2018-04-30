
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


class User:


class ChatRel: