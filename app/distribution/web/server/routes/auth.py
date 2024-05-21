from flask import request
from werkzeug.exceptions import BadRequest
from app.application.services.auth_service import AuthService
from flask_restx import Namespace, Resource
from app.domain.api_models.auth_api_model import create_auth_model

auth_ns = Namespace('api', description='Test operations')
auth_model = create_auth_model(auth_ns)

@auth_ns.route("")
class AuthRoutes(Resource):
    @auth_ns.expect(auth_model)
    @auth_ns.response(200, 'Login Success')
    @auth_ns.response(400, 'Invalid JSON payload')
    @auth_ns.response(401, 'Invalid username or password')
    def post(self):
        """
        Authenticates a user by checking their credentials against the database.
        Returns:
            - If the authentication is successful, a JSON response with a success message and a token is returned.
            - If the authentication fails, a JSON response with an error message is returned.
            - If the request payload is invalid, a JSON response with an error message is returned.
        Raises:
            - BadRequest: If the request payload is invalid.
        """
        try:
            auth_service = AuthService()
            auth = request.get_json()
            token = auth_service.create_token(auth)
            if token:
                return {'msg': 'Login Success', 'token': token}, 200
            else:
                return {'msg': 'Invalid username or password'}, 401
        except BadRequest:
            return {'msg': 'Invalid JSON payload'}, 400
