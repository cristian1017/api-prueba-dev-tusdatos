from app.config import user_login_success
from datetime import datetime, timedelta, timezone
from app.config import jwt_secret_key
import jwt


class AuthService:

    def create_token(self, auth):
        """
        Creates a JWT token for authentication.
        Args:
            auth (dict): A dictionary containing the username and password for authentication.
        Returns:
            str or tuple: If the authentication is successful, a JWT token is returned. If the authentication fails,
            a JSON response with a message and a status code of 400 is returned.
        Raises:
            Exception: If an error occurs during the token creation process, an exception is raised.
        """
        try:
            if auth and auth['username'] == user_login_success['username'] and auth['password'] == user_login_success['password']:
                token = jwt.encode({
                    'username': auth['username'],
                    'exp': datetime.now(timezone.utc) + timedelta(days=1)
                }, jwt_secret_key, algorithm="HS256")
                return token
            return False
        except:
            return {'msg': 'Could not verify!'}, 400
