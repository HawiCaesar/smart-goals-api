
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from bucketlist import auth
from config import app_config

# Initialise SQL-Alchemy
database = SQLAlchemy()

# Initialize the app


def create_application(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    database.init_app(app)

    return app



