from bucketlist import app, classes
from flask.views import MethodView
from flask import jsonify, request, make_response
import json, hashlib

class RegisterUser(MethodView):

    def post(self):

        json_response = json.loads(request.data.decode('utf8'))

        hash_object = hashlib.sha1(json_response['password'].encode())
        self.password = hash_object.hexdigest()

        classes.all_users[json_response['email']] = [json_response['fullname'],
                                                     json_response['email'],
                                                     self.password]

        response = {
            'status':'success',
            'message':'User has been registered'
        }

        return make_response(jsonify(response)), 201
        