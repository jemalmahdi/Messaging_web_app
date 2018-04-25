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



class MessageView(MethodView):
    def get(self, message_id):
        """
        Handle GET requests.

        Returns JSON representing all of the message if message_id is None, or a
        single message if message_id is not None.

        :param message_id: id of a message, or None for all messages
        :return: JSON response
        """
        if message_id is None:
            messages = get_all_rows('message')
            return jsonify(messages)
        else:
            messages = query_by_id('message', message_id)

            if messages is not None:
                response = jsonify(messages)
            else:
                raise RequestError(404, 'message not found')

            return response

    def post(self, user_id):
        """
        Handles a message request to insert a new city. Returns a JSON
        response representing the new message.

        The message name must be provided in the requests's form data.

        :return: a response containing the JSON representation of the message
        """
        if 'text' not in request.form:
            raise RequestError(422, 'text of message required')
        else:
            response = jsonify(insert_message(request.form['text'], user_id))
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

    def put(self, message_id):
        """
        Handles a PUT request given a certain message_id
        :return:a response containing the JSON representation of the
            new message
        """

        if message_id is None:
            raise RequestError(422, 'message id is required')
        else:
            if 'text' not in request.form:
                raise RequestError(422, 'message text is required')
            else:
                message = query_by_id('message', message_id)

                if message is not None:
                    update_message(request.form['text'],
                                  request.form['user'], message_id)
                else:
                    raise RequestError(404, 'message not found')

                message = query_by_id('message', message_id)
                return jsonify(message)

    def patch(self, message_id):
        """
        Handles the PATCH request given a certain message_id
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
                    new_name = request.form['text']

                new_user = messages['user_id']
                if 'user' in request.form:
                    new_user = request.form['user']

                update_message(message_id, new_text, new_user)
                messages = query_by_id('messages', message_id)
                return jsonify(messages)

