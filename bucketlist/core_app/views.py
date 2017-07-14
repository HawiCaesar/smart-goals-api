from flask import request, make_response, url_for, jsonify
from bucketlist.models import Bucketlist, User
from flask.views import MethodView
import datetime
from bucketlist import get_jwt_identity, jwt_required


class BucketlistAPI(MethodView):
    """ Create Read Update Delete Bucketlist """

    now = datetime.datetime.now()
    @jwt_required
    def post(self):
        data = request.get_json()

        current_user = get_jwt_identity()

        if current_user:

            bucketlist = Bucketlist(name=data.get('name'), created_by=current_user)
            bucketlist.save()  # Save bucketlist name

            response = jsonify({
                'status': "Success",
                'message': "Bucketlist Created"
            })

            response.status_code = 201
            return make_response(response)

        else:

            response = {
                'message': "You have no access token to use this resource"
            }
            return make_response(jsonify(response)), 401

    @jwt_required
    def get(self, id=None):

        current_user = get_jwt_identity()

        if id and current_user:

            bucketlist = Bucketlist.query.filter_by(id=id).first()

            if not bucketlist:
                response = jsonify({
                    'status': 'Fail',
                    'message': 'Bucketlist Does Not Exist'
                })
                response.status_code = 404

            else:
                response = jsonify({
                    'id': bucketlist.id,
                    'name': bucketlist.name
                })

                response.status_code = 200

        elif current_user:

            bucketlists = Bucketlist.get_all()
            results = []

            for bucketlist in bucketlists:
                obj = {
                    'id': bucketlist.id,
                    'name': bucketlist.name
                }
                results.append(obj)

            response = jsonify(results)
            response.status_code = 200

        return make_response(response)

    def put(self, id=None):
        if id:
            bucketlist = Bucketlist.query.filter_by(id=id).first()
            data = request.get_json()

            if bucketlist:
                bucketlist.name = data.get("name")
                bucketlist.save()
                response = jsonify({
                    'id': bucketlist.id,
                    'name': bucketlist.name
                })

                response.status_code = 200

            else:
                response = jsonify({
                    'status': "Fail",
                    'message': "Bucketlist name does not exist"
                })

                response.status_code = 404

        return make_response(response)

    def delete(self, id=None):

        if id:
            bucketlist = Bucketlist.query.filter_by(id=id).first()

            if bucketlist:
                bucketlist.delete()
                response = jsonify({
                    "status": "Success",
                    "message": "Bucketlist {} deleted".format(bucketlist.id)
                })

                response.status_code = 200

            else:
                response = jsonify({
                    "status": "Fail",
                    "message": "Bucketlist does not exist"
                })
                response.status_code = 404

        return make_response(response)

class BucketlistItemAPI(MethodView):
    pass