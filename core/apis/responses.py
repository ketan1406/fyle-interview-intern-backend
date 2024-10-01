from flask import Response, jsonify, make_response

class APIResponse(Response):
    @classmethod
    def respond(cls, data, status_code=200):
        # General success response with optional status code
        return make_response(jsonify(data=data), status_code)
    
    @classmethod
    def respond_error(cls, error_type, message, status_code=400):
        # General error response, includes error type and message
        return make_response(jsonify(error=error_type, message=message), status_code)
