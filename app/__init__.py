
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import app_config
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token

# Initialise SQL-Alchemy
database = SQLAlchemy()

# Initialise Restful API
api = Api()

# Initialize the app


def create_application(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Register endpoints
    from .resources import resources as bucketlist_blueprint
    app.register_blueprint(bucketlist_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.models import User
    global jwt
    jwt = JWTManager(app)

    # Make app a restful api
    api.init_app(app)
    database.init_app(app)

    return app



