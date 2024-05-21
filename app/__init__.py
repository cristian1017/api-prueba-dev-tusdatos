from flask import Flask
from flask_restx import Api
from app.distribution.web.server.routes.auth import auth_ns
from app.distribution.web.server.routes.data import data_ns
from app.distribution.web.server.routes.scraper import scraper_ns
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    api = Api(app, doc='/swagger', title='API documentation',
              description='API documentation for App Test tusdatos')

    CORS(api.app)
    api.add_namespace(auth_ns, path='/api/login')
    api.add_namespace(data_ns, path='/api/data')
    api.add_namespace(scraper_ns, path='/api/scraper')

    return app
