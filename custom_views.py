"""
CS232

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

    def delete(self, chatrel_id):
        """
        Handles a DELETE request given a certain login_id
        :param login_id: the id of the login to delete
        :return: a response containing the JSON representation of the
            old login
        """

        if chatrel_id is None:
            raise RequestError(422, 'chatrel_id required')
        else:
            chat = query_by_id('chat_rel', chatrel_id)

            if chat is not None:
                delete_item('chat_rel', chatrel_id)
            else:
                raise RequestError(404, 'Chat rel not found')
        return jsonify(chat)

    def put(self, id):
        """
        Handles a PUT request given a certain login_id
        :param login_id: the id of the login to be put
        :return: a response containing the JSON representation of the
            new login
        """

        if id is None:
            raise RequestError(422, 'chatrel_id is required')
        else:
            if 'user_id' not in request.form:
                raise RequestError(422, 'User_id is required')
            else:
                chat = query_by_id('chat_rel', id)

                if chat is not None:
                    # Need new function
                    update_user(id, request.form['user_id'])
                else:
                    raise RequestError(404, 'chat not found')
                chat = query_by_id('chat_rel', id)
                return jsonify(chat)

    def patch(self, chatrel_id):
        """
        Handles the PATCH request given a certain login_id
        :param login_id: the id of the login to be patched
        :return:a response containing the JSON representation of the
            new login
        """

        if chatrel_id is None:
            raise RequestError(422, 'chatrel_id is required')
        else:
            if 'user_id' not in request.form:
                raise RequestError(422, 'User_id is required')
            else:
                chat = query_by_id('chat_rel', chatrel_id)

                if chat is not None:
                    # Need new function
                    update_user(chatrel_id, request.form['user_id'])
                else:
                    raise RequestError(404, 'chat not found')
                chat = query_by_id('chat_rel', chatrel_id)
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

    def delete(self, message_id):
        """
        Handles a DELETE request given a certain message_id
        :return: a response containing the JSON representation of the
            old message
        """

        if message_id is None:
            raise RequestError(422, 'message id required')
        else:
            messages = query_by_id('message', message_id)

            if messages is not None:
                delete_item('message', message_id)
            else:
                raise RequestError(404, 'message not found')
        return jsonify(messages)

    def put(self, id):
        """
        Handles a PUT request given a certain message_id
        :param id: the id of the message to be put
        :return:a response containing the JSON representation of the
            new message
        """

        if id is None:
            raise RequestError(422, 'message id is required')
        else:
            if 'message' not in request.form:
                raise RequestError(422, 'message text is required')
            else:
                message = query_by_id('message', id)

                if message is not None:
                    update_message()
                else:
                    raise RequestError(404, 'message not found')

                message = query_by_id('message', id)
                return jsonify(message)

    def patch(self, message_id):
        """
        Handles the PATCH request given a certain message_id
        :param message_id: the id of the message to be patched
        :return:a response containing the JSON representation of the
            old message
        """

        if message_id is None:
            raise RequestError(422, 'message id is required')
        else:
            messages = query_by_id('message', message_id)

            if messages is None:
                raise RequestError(404, 'message not found')
            else:

                new_text = messages['text']
                if 'text' in request.form:
                    new_text = request.form['text']

                new_user = messages['user_id']
                if 'user' in request.form:
                    new_user = request.form['user']

                update_message(message_id, new_text, new_user)
                messages = query_by_id('messages', message_id)
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

    def delete(self, user_id):
        """
        Handles a DELETE request given a certain user_id
        :param user_id: the id of the user to delete
        :return: a response containing the JSON representation of the
            old user
        """

        if user_id is None:
            raise RequestError(422, 'user name required')
        else:
            user = query_by_id('user', user_id)

            if user is not None:
                delete_item('user', user_id)
            else:
                raise RequestError(404, 'user not found')
        return jsonify(user)

    def put(self, id):
        """
        Handles a PUT request given a certain user_id
        :param user_id: the id of the user to be put
        :return:a response containing the JSON representation of the
            new user
        """

        if id is None:
            raise RequestError(422, 'User Id is required')
        else:
            if 'name' not in request.form:
                raise RequestError(422, 'User name is required')
            else:
                user = query_by_id('user', id)

                if user is not None:
                    update_user(id, request.form['name'])
                else:
                    raise RequestError(404, 'user not found')
                user = query_by_id('user', id)
                return jsonify(user)

    def patch(self, user_id):
        """
        Handles the PATCH request given a certain user_id
        :param user_id: the id of the user to be patched
        :return:a response containing the JSON representation of the
            new user
        """

        if user_id is None:
            raise RequestError(422, 'User Id is required')
        else:
            user = query_by_id('user', user_id)

            if user is None:
                raise RequestError(404, 'User not found')
            else:

                new_name = user['name']
                if 'name' in request.form:
                    new_name = request.form['name']

                update_user(user_id, new_name)
                user = query_by_id('user', user_id)
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

    def delete(self, chat_id):
        """
        Handles a DELETE request given a certain chat_id
        :param chat_id: the id of the chat to be deleted
        :return: a response containing the JSON representation of the
            old message
        """

        if chat_id is None:
            raise RequestError(422, 'chat id required')
        else:
            chat = query_by_id('chat', chat_id)

            if chat is not None:
                delete_item('chat', chat_id)
            else:
                raise RequestError(404, 'chat not found')
        return jsonify(chat)


# Register MessageView as the handler for all the /message/ requests.
message_view = MessageView.as_view('message_view')
app.add_url_rule('/api/message/', defaults={'message_id': None},
                 view_func=message_view, methods=['GET'])
app.add_url_rule('/api/message/', view_func=message_view,
                 methods=['POST'])
# For this you would need to provide the user_id through the form data. URL
# values are only for message ID -Morgan
# app.add_url_rule('/message/<int:user_id>', view_func=message_view,
#                  methods=['POST'])  # Hey, should this be message? or POST
app.add_url_rule('/api/message/<int:message_id>', view_func=message_view,
                 methods=['GET'])
app.add_url_rule('/api/message/<int:message_id>', view_func=message_view,
                 methods=['DELETE'])
app.add_url_rule('/api/message/<int:message_id>', view_func=message_view,
                 methods=['PUT'])
app.add_url_rule('/api/message/<int:message_id>', view_func=message_view,
                 methods=['PATCH'])


# Register UserView as the handler for all the /user/ requests.
user_view = UserView.as_view('user_view')
app.add_url_rule('/api/user/', defaults={'user_id': None},
                 view_func=user_view, methods=['GET'])
app.add_url_rule('/api/user', view_func=user_view,
                 methods=['POST'])
app.add_url_rule('/api/user/<int:user_id>', view_func=user_view,
                 methods=['GET'])
app.add_url_rule('/api/user/<int:user_id>', view_func=user_view,
                 methods=['DELETE'])
app.add_url_rule('/api/user/<int:user_id>', view_func=user_view,
                 methods=['PUT'])
app.add_url_rule('/api/user/<int:user_id>', view_func=user_view,
                 methods=['PATCH'])


# Register ChatView as the handler for all the /chat/ requests.
chat_view = ChatView.as_view('chat_view')
app.add_url_rule('/api/chat/', defaults={'chat_id': None},
                 view_func=chat_view, methods=['GET'])
app.add_url_rule('/api/chat/', view_func=chat_view,
                 methods=['POST'])
app.add_url_rule('/api/chat/<int:user_id>', view_func=chat_view,
                 methods=['GET'])
app.add_url_rule('/api/chat/<int:chat_id>', view_func=chat_view,
                 methods=['DELETE'])


# Register ChatRelView as the handler for all the /login/ requests.
chatrel_view = ChatRelView.as_view('chatrel_view')
app.add_url_rule('/chatrel/', defaults={'chatrel_id': None},
                 view_func=chatrel_view, methods=['GET'])
app.add_url_rule('/chatrel/', view_func=chatrel_view,
                 methods=['POST'])
app.add_url_rule('/chatrel/<int:chatrel_id>', view_func=chatrel_view,
                 methods=['GET'])
app.add_url_rule('/chatrel/<int:chatrel_id>', view_func=chatrel_view,
                 methods=['DELETE'])
app.add_url_rule('/chatrel/<int:chatrel_id>', view_func=chatrel_view,
                 methods=['PUT'])
app.add_url_rule('/chatrel/<int:chatrel_id>', view_func=chatrel_view,
                 methods=['PATCH'])
