from flask import jsonify

# START: Taken from homework 18
class RequestError(Exception):
    """
    Custom exception class for handling errors in a request.
    """

    def __init__(self, status_code, error_message):
        Exception.__init__(self)

        self.status_code = str(status_code)
        self.error_message = str(error_message)

    def to_response(self):
        response = jsonify({'error': self.error_message})
        response.status = self.status_code
        return response





# END: Taken from homework 18