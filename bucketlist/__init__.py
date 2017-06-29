
from flask import Flask
from flask_bootstrap import Bootstrap
from config import app_config

# Initialize the app
app = Flask(__name__, instance_relative_config=True)
Bootstrap(app)
from bucketlist import views

# Load the config file
app.config.from_object(app_config['development'])

#app.config['SECRET_KEY'] = "q38FGSFDsyrefbhj54"
