from bucketlist import app, classes
#from flask.views import MethodView
from flask import jsonify, request, make_response
import json, hashlib


@app.route('/v1/api/auth/register', methods=['POST'])
def api_create_user():

    if request.method == 'POST':

        post_request = json.loads(request.data.decode("utf-8"))

        hash_object = hashlib.sha1(post_request["password"].encode())
        password = hash_object.hexdigest()

        classes.all_users[post_request["email"]] = [post_request["fullname"],
                                                    post_request["email"],
                                                    password]

        response = {
            'status': 'success',
            'message': 'User has been registered'
        }

        return make_response(jsonify(response)), 201

    else:
        response = {
            'status': 'error',
            'message': 'Route not allowed'
        }

        return make_response(jsonify(response)), 500
