from flask_restx import Api

def init_api(app):
    api = Api(
        app,
        version='1.0',
        title='REST API',
        description='Документація REST API для системи опитувань експертів',
        doc='/docs'
    )
    return api
