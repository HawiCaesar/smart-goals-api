from flask import request, make_response, url_for, jsonify
from bucketlist.models import Bucketlist, User, BucketlistItem
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

        bucketlist = Bucketlist(name=data.get('name'), created_by=current_user)
        bucketlist.save()  # Save bucketlist name

        response = jsonify({
            'status': "Success",
            'message': "Bucketlist Created"
        })

        response.status_code = 201
        return make_response(response)

    @jwt_required
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

    @jwt_required
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

    @jwt_required
    def delete(self, id):

        if id:
            bucketlist = Bucketlist.query.filter_by(id=id).first()

            if bucketlist:
                response = jsonify({
                    "status": "Success",
                    "message": "Bucketlist {} deleted".format(bucketlist.id)
                })

                response.status_code = 200

                bucketlist.delete()

            else:
                response = jsonify({
                    "status": "Fail",
                    "message": "Bucketlist does not exist"
                })
                response.status_code = 404

        return make_response(response)

class BucketlistItemAPI(MethodView):

    """ Create Read Update Bucketlist items """

    now = datetime.datetime.now()

    @jwt_required
    def post(self, id):
        data = request.get_json()

        bucketlist = Bucketlist.query.filter_by(id=id).first()
        bucketlist_item = BucketlistItem.query.filter_by(item_name=data.get('item_name')).first()

        if not bucketlist_item:

            new_item = BucketlistItem(item_name=data.get('item_name'), bucketlist=bucketlist.id,
                                      done=data.get('done'), complete_by=data.get('complete_by'))
            new_item.save()

            response = jsonify({
                'status': "Success",
                'message': "Bucketlist Item Created"
            })

            response.status_code = 201

        else:
            response = jsonify({
                'status': "Success",
                'message': "Bucketlist Item Already Exists"
            })

            response.status_code = 200

        return make_response(response)
    #
    #
    # def get(self):
    #     pass
    #
    # def put(self):
    #     pass
    #
    # def delete(self):
    #     pass