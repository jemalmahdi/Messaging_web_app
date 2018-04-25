


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


@app.errorhandler(RequestError)
def handle_invalid_usage(error):
    """
    Returns a JSON response built from RequestError.

    :param error: the RequestError
    :return: a response containing the error message
    """
    return error.to_response()


# END: Taken from homework 18