"""
WooMessages
CS 232
Final Project
AVI VAJPEYI, JEMAL JEMAL, ISAAC WEISS, MORGAN THOMPSON



A file containing the declarations and definitions of custom MethodViews.
There are three customMethodViews: ArtistView, AlbumView and TrackView.

Each of them have GET, POST, PATCH, PUT and DELETE requests implemented.
"""
from flask.views import MethodView, request
from flask import Flask, g, jsonify
from queries import *
from exception_classes import *
from database import *


class ChatRelView(MethodView):
    """
    This view handles all the /chatrel/ requests.
    """

    def get(self, id):
        """
        Handle GET requests.
        Returns JSON representing all of the logins if login_id is None, or a
        single login if login_id is not None.
        :param id: id of a login, or None for all logins
        :return: JSON response
        """
        if id is None:
            chatrel = get_all_rows('chat_rel')
            return jsonify(chatrel)
        else:
            chatrel = query_by_id('chat_rel', id)

            if chatrel is not None:
                response = jsonify(chatrel)
            else:
                raise RequestError(404, 'chat relation not found')

            return response

    def post(self):
        """
        Handles a POST request to insert a new login. Returns a JSON
        response representing the new login.
        The username must be provided in the requests's form data.
        :return: a response containing the JSON representation of the login
        """
        # Still working this one out.
        if 'user_id' not in request.form:
            raise RequestError(422, 'user_id required')
        if 'chat_id' not in request.form:
            raise RequestError(422, 'chat_id required')
        else:
            response = jsonify(insert_chat_rel(request.form['user_id'],
                                               request.form['chat_id']))
        return response

    def delete(self, id):
        """
        Handles a DELETE request given a certain login_id
        :param id: the id of the login to delete
        :return: a response containing the JSON representation of the
            old login
        """

        if id is None:
            raise RequestError(422, 'chatrel_id required')
        else:
            chat = query_by_id('chat_rel', id)

            if chat is not None:
                delete_item('chat_rel', id)
            else:
                raise RequestError(404, 'Chat rel not found')
        return jsonify(chat)


class MessageView(MethodView):
    def get(self, id):
        """
        Handle GET requests.
        Returns JSON representing all of the message if message_id is None, or
        a single message if message_id is not None.
        :param id: id of a message, or None for all messages
        :return: JSON response
        """
        if id is None:
            messages = get_all_rows('message')
            return jsonify(messages)
        else:
            messages = query_by_id('message', id)

            if messages is not None:
                response = jsonify(messages)
            else:
                raise RequestError(404, 'message not found')

            return response

    # The user_id should be provided through form data, not URL data. I
    # updated it to fix that -Morgan
    def post(self):
        """
        Handles a message request to insert a new city. Returns a JSON
        response representing the new message.
        The message name must be provided in the requests's form data.
        :return: a response containing the JSON representation of the message
        """
        if 'message' not in request.form:
            raise RequestError(422, 'text of message required')
        if 'time' not in request.form:
            raise RequestError(422, 'time of message required')
        if 'user_id' not in request.form:
            raise RequestError(422, 'user_id of message required')
        if 'chat_id' not in request.form:
            raise RequestError(422, 'chat_id of message required')
        else:
            response = jsonify(insert_message(request.form['message'],
                                              request.form['time'],
                                              request.form['user_id'],
                                              request.form['chat_id']))
        return response

    def delete(self, id):
        """
        Handles a DELETE request given a certain message_id
        :return: a response containing the JSON representation of the
            old message
        """

        if id is None:
            raise RequestError(422, 'message id required')
        else:
            messages = query_by_id('message', id)

            if messages is not None:
                delete_item('message', id)
            else:
                raise RequestError(404, 'message not found')
        return jsonify(messages)


class UserView(MethodView):
    """
    This view handles all the /user/ requests.
    """

    def get(self, id):
        """
        Handle GET requests.
        Returns JSON representing all of the users if user_id is None, or a
        single user if user_id is not None.
        :param id: id of a user, or None for all users
        :return: JSON response
        """
        if id is None:
            user = get_all_rows('user')
            return jsonify(user)
        else:
            user = query_by_id('user', id)
            if user is not None:
                response = jsonify(user)
            else:
                raise RequestError(404, 'user not found')

            return response

    def post(self):
        """
        Handles a POST request to insert a new user. Returns a JSON
        response representing the new user.
        The user name must be provided in the requests's form data.
        :return: a response containing the JSON representation of the user
        """
        if 'name' not in request.form:
            raise RequestError(422, 'user name required')
        if 'email' not in request.form:
            raise RequestError(422, 'user email required')
        if 'username' not in request.form:
            raise RequestError(422, 'user username required')
        if 'password' not in request.form:
            raise RequestError(422, 'user password required')

        else:
            response = jsonify(insert_user(request.form['name'],
                                           request.form['email'],
                                           request.form['username'],
                                           request.form['password']))

            # response = jsonify(insert_user(request.form['name'], 1))
            # response = jsonify(insert_user(request.form['name'], login_id))
            # Need to get login_id

        return response

    def delete(self, id):
        """
        Handles a DELETE request given a certain user_id
        :param id: the id of the user to delete
        :return: a response containing the JSON representation of the
            old user
        """

        if id is None:
            raise RequestError(422, 'user name required')
        else:
            user = query_by_id('user', id)

            if user is not None:
                delete_item('user', id)
            else:
                raise RequestError(404, 'user not found')
        return jsonify(user)


class ChatView(MethodView):
    def get(self, id):
        """
        Handle GET requests.
        Returns JSON representing all of the message if chat_id is None, or a
        single chat if chat_id is not None.
        :param id: id of a chat, or None for all chats
        :return: JSON response
        """
        if id is None:
            chat = get_all_rows('chat')
            return jsonify(chat)
        else:
            chat = query_by_id('chat', id)

            if chat is not None:
                response = jsonify(chat)
            else:
                raise RequestError(404, 'chat not found')

            return response

    def post(self):
        """
        Handles a message request to insert a new chat. Returns a JSON
        response representing the new chat.
        The must be provided in the requests's form data.
        :param user_id: the id of the user creating the chat.
        :return: a response containing the JSON representation of the message
        """
        if 'title' not in request.form:
            raise RequestError(422, 'chat title required')
        if 'time' not in request.form:
            raise RequestError(422, 'chat time required')
        else:
            response = jsonify(insert_chat(request.form['title'],
                                           request.form['time']))
            # FIND SOMETHING THAT WORKS HERE
            # response = jsonify(insert_message(request.form['text'], user_id))
        return response

    def delete(self, id):
        """
        Handles a DELETE request given a certain chat_id
        :param id: the id of the chat to be deleted
        :return: a response containing the JSON representation of the
            old message
        """

        if id is None:
            raise RequestError(422, 'chat id required')
        else:
            chat = query_by_id('chat', id)

            if chat is not None:
                delete_item('chat', id)
            else:
                raise RequestError(404, 'chat not found')
        return jsonify(chat)
