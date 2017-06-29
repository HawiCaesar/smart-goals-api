
# Instance configuartions for the flask application are done here
class Config(object):
    # Some Common Configurations
    DEBUG = True

class DevelopmentConfig(Config):
    # Development configurations

    SECRET_KEY = "q38FGSFDsyrefbhj54"

class ProductionConfig():
    # Production configurations
    DEBUG = False



app_config = {
    "development": DevelopmentConfig(),
    "production": ProductionConfig()
}

