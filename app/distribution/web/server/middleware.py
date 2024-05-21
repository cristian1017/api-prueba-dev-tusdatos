from flask import request, g
from functools import wraps
from datetime import datetime, timedelta
import jwt
from app.config import jwt_secret_key, user_login_success


def token_required(f):
    """
    Decorator function that requires a valid token to access a resource.

    This function takes a function `f` as input and returns a decorated function. The decorated function checks if a token is present in the request headers. If the token is missing, it returns a JSON response with an error message and a status code of 401. If the token is present, it decodes the token using the `jwt_secret_key` from the `app.config` module. If the token is invalid or expired, it returns a JSON response with an error message and a status code of 401. If the token is valid, it checks if the username in the token matches the username in `user_login_success` from the `app.config` module. If the usernames do not match, it returns a JSON response with an error message and a status code of 401. If the token is valid and the usernames match, it calls the original function `f` with the provided arguments and returns its result.

    Parameters:
    - f (function): The function to be decorated.

    Returns:
    - function: The decorated function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            if 'Bearer' in token:
                token = token.split(" ")[1]

        if not token:
            return {'message': 'Authentication token is missing. Please provide a valid token to access this resource.'}, 401
        try:
            data = jwt.decode(token, jwt_secret_key, algorithms=["HS256"])
            if data['username'] != user_login_success['username']:
                return {'message': 'Invalid token, user not authorized!'}, 401

        except jwt.ExpiredSignatureError:
            return {'message': 'Token has expired!'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Invalid token, user not authorized!'}, 401
        return f(*args, **kwargs)
    return decorated_function
