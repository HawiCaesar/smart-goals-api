from flask import request, make_response, url_for, jsonify
from bucketlist import database
from bucketlist.models import Bucketlist
from flask.views import MethodView
import datetime


class BucketlistAPI(MethodView):
    """ Create Read Update Delete Bucketlist """

    now = datetime.datetime.now()

    def post(self):
        data = request.get_json()

        bucketlist = Bucketlist(name=data.get('name'))
        bucketlist.save()
        response = jsonify({
            'id': bucketlist.id,
            'name': bucketlist.name
        })
        response.status_code = 201
        return make_response(response)

    def get(self, id=None):

        response = {}

        if id:

            bucketlist = Bucketlist.query.filter_by(id=id).first()

            if not bucketlist:
                response = {
                    'status': 'Fail',
                    'message': 'Bucketlist does not exist'
                }
                return make_response(jsonify(response)), 404

            else:
                response = jsonify({
                    'id': bucketlist.id,
                    'name': bucketlist.name
                })

                return make_response(response), 200

        else:

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