from app.application.services.scraper_service import ScraperService
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

scraper_ns = Namespace('api', description='Test operations',
                       authorizations=authorizations)


@scraper_ns.route("")
class ScraperRoutes(Resource):
    @scraper_ns.doc(security='Bearer')
    @scraper_ns.response(200, 'The scraping process has been completed')
    @scraper_ns.response(401, 'Invalid token, user not authorized!')
    @token_required
    def get(self):
        """
        This function is a endpoint with the HTTP method "GET". It requires a valid token to access the resource. 
        The function initializes a ScraperService object and calls its init_scraper() method. The result of the method call is returned as the response.

        Parameters:
            None

        This endpoint is protected by the `token_required` decorator, which ensures that only authenticated

        requests with a valid JWT token can access the resource. The token must be included in the `Authorization`
        header as a Bearer token.

        Returns:
            The result of calling the init_scraper() method of the ScraperService object.
        """
        scraper_service = ScraperService()
        return scraper_service.init_scraper()
