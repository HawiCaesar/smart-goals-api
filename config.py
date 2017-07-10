
import os

# Instance configuartions for the flask application are done here


class Config(object):
    # Some Common Configurations
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET")
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    # Development configurations

    DEBUG = True


class TestingConfig():
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'


class ProductionConfig():
    # Production configurations
    DEBUG = False


app_config = {
    "development": DevelopmentConfig(),
    "testing": TestingConfig(),
    "production": ProductionConfig()
}

