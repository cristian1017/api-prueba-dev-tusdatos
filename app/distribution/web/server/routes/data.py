from app.application.services.data_service import DataService
from app.distribution.web.server.middleware import token_required
from flask_restx import Namespace, Resource

authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"'
    }
}

data_ns = Namespace('api', description='Test operations',
                    authorizations=authorizations)


@data_ns.route("")
class DataList(Resource):
    @data_ns.doc(security='Bearer')
    @data_ns.response(200, 'Success')
    @data_ns.response(401, 'Invalid token, user not authorized!')
    @token_required
    def get(self):
        """
        Retrieves data from the data service using the specified authentication token.

        This function is decorated with the `@data_ns.doc` decorator, which provides documentation for the API endpoint. The `security` parameter is set to 'Bearer', indicating that the endpoint requires a valid authentication token.

        The function is also decorated with the `@data_ns.response` decorator, which specifies the possible HTTP response codes and their corresponding messages. The response codes 200 and 401 are defined, indicating a successful retrieval of data or an unauthorized access, respectively.

        The `@token_required` decorator ensures that only authenticated requests with a valid token can access the endpoint.

        Parameters:
            self: The instance of the class.

        Returns:
            List of ID's save info in data.json

        Raises:
            None.
        """
        data_service = DataService()
        return data_service.get_info_data()


@data_ns.route("/<id>")
class DataRoutes(Resource):
    @data_ns.doc(security='Bearer')
    @data_ns.response(200, 'Success')
    @data_ns.response(401, 'Invalid token, user not authorized!')
    @data_ns.response(404, 'ID not found')
    @token_required
    def get(sefl, id):
        """
        Retrieves data associated with a given ID from the data repository and returns it in a JSON response.
        This endpoint is protected by the `token_required` decorator, which ensures that only authenticated
        requests with a valid JWT token can access the resource. The token must be included in the `Authorization`
        header as a Bearer token.

        :param id: The ID of the data to retrieve.
        :type id: str

        :return: A JSON response containing the data associated with the given ID, including the ID itself, the total number of data items, and either the entire data list or separate lists for demandados and demandantes, along with the counts of each. If the ID is not found, a JSON response with a message and a status code of 404 is returned.
        :rtype: flask.Response
        """
        data_service = DataService()
        return data_service.get_data_id(id)
