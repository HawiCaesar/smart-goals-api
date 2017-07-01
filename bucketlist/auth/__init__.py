from flask import  Blueprint
from .import views

auth = Blueprint('auth', __name__)

auth.add_url_rule(
    '/v1/api/auth/register',
    view_func=views.RegisterUser.as_view('register_user'),
    methods=['POST']
)