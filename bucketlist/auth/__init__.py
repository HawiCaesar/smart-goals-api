from flask import Blueprint

from . import views

auth = Blueprint('auth', __name__)

auth_users = views.UserRegistrationAPI.as_view('auth_users_api')
auth_login = views.LoginAPI.as_view('auth_login_api')

auth.add_url_rule('/v1/api/auth/register', view_func=auth_users, methods=['POST'])

auth.add_url_rule('/v1/api/auth/user/<int:id>', view_func=auth_users, methods=['GET'])

auth.add_url_rule('/v1/api/auth/user/', view_func=auth_users, methods=['GET'])

auth.add_url_rule('/v1/api/auth/login', view_func=auth_login, methods=['POST'])
