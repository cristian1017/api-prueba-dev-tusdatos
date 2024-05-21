from flask_restx import fields

def create_auth_model(api):
    return api.model('AuthModel', {
        'username': fields.String(required=True, description='The user\'s username'),
        'password': fields.String(required=True, description='The user\'s password')
    })
