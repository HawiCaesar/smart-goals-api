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
        bucketlist.save()  # Save bucketlist name

        response = jsonify({
            'status': "Success",
            'message': "Bucketlist Created"
        })

        response.status_code = 201
        return make_response(response)

    def get(self, id=None):

        if id:

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

        # else:
        #     response = jsonify({
        #         'status': 'Error',
        #         'message': 'Please provide an id'
        #     })
        #
        #     response.status_code = 405

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

        # else:
        #     response = jsonify({
        #         'status': "Fail",
        #         'message': "Please provide a bucketlist id"
        #     })
        #     response.status_code = 405

        return make_response(response)
