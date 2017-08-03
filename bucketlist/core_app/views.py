from flask import request, make_response, url_for, jsonify
from bucketlist.models import Bucketlist, User, BucketlistItem, database
from flask.views import MethodView
import datetime
from bucketlist import get_jwt_identity, jwt_required

class BucketlistAPI(MethodView):
    """ Create Read Update Delete Bucketlist """

    @jwt_required
    def post(self):
        now = datetime.datetime.now()
        data = request.get_json()

        current_user = get_jwt_identity()

        bucketlist = Bucketlist(name=data.get('name'), created_by=current_user, date_created=now)
        bucketlist.save()  # Save bucketlist name

        response = jsonify({
            'status': "Success",
            'message': "Bucketlist Created"
        })

        response.status_code = 201
        return make_response(response)

    @jwt_required
    def get(self, **kwargs):
        start = request.args.get('start')
        limit = request.args.get('limit')
        query = request.args.get('q')

        current_user = get_jwt_identity()

        if kwargs.get('id') is not None:

            bucketlist = Bucketlist.query.filter_by(id=kwargs['id'], created_by=current_user).first()

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
            if start is None and limit is None:
                start = 1
                limit = 3

            search = Bucketlist.get_paginated_list('/v1/api/bucketlists/', query, current_user, int(start), int(limit))

            final_list = []

            try:
                for bucketlist in search['results']:
                    result = {
                        'id': bucketlist.id,
                        'name': bucketlist.name
                    }
                    final_list.append(result)

                response = jsonify({"previous": search['previous'], "next": search['next'], "results": final_list})
                response.status_code = 200

            except:
                response = jsonify({
                    "status": "Fail",
                    "message": "No Bucketlist matching your query was found"
                })
                response.status_code = 404

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

    @jwt_required
    def post(self, id):
        data = request.get_json()
        now = datetime.datetime.now()

        bucketlist = Bucketlist.query.filter_by(id=id).first()
        bucketlist_item = BucketlistItem.query.filter_by(item_name=data.get('item_name')).first()

        if not bucketlist_item:

            new_item = BucketlistItem(item_name=data.get('item_name'), bucketlist_id=bucketlist.id,
                                      date_created=now, date_modified=now,
                                      done=False, complete_by=data.get('complete_by'))
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

            response.status_code = 409  # 409 means there is a conflict with db as two of the same resource exists

        return make_response(response)

    @jwt_required
    def get(self, id, item_id=None):

        if id:
            buckelist_items = BucketlistItem.query.filter_by(bucketlist_id=id).all()

            if buckelist_items:
                buckelist_item = BucketlistItem.get_bucketlist_items(item_id)

                if buckelist_item:

                    response = jsonify({
                        'item_name': buckelist_item.item_name,
                        'date_created': buckelist_item.date_created,
                        'date_modified': buckelist_item.date_modified,
                        'done': buckelist_item.done,
                        'complete_by': buckelist_item.complete_by,
                        'bucketlist_id': buckelist_item.bucketlist_id
                    })
                    response.status_code = 200

                else:
                    all_items = []
                    for item in buckelist_items:
                        item_response = {
                            'item_name': item.item_name,
                            'date_created': item.date_created,
                            'date_modified': item.date_modified,
                            'done': item.done,
                            'complete_by': item.complete_by,
                            'bucketlist_id': item.bucketlist_id
                        }
                        all_items.append(item_response)

                    response = jsonify(all_items)
                    response.status_code = 200

            else:

                response = jsonify({
                    "status": "Fail",
                    "message": "No bucketlist items in bucketlist"
                })
                response.status_code = 404

        return make_response(response)

    @jwt_required
    def put(self, id, item_id):
        data = request.get_json()

        bucketlist_item = BucketlistItem.get_bucketlist_items(item_id)

        if bucketlist_item:
            if bucketlist_item.bucketlist_id == id:
                bucketlist_item.item_name = data.get('item_name')

                if data.get('done') == 'true':

                    bucketlist_item.done = True

                bucketlist_item.date_modified = datetime.datetime.now()
                database.session.commit()  # update new changes

                response = jsonify({
                    "status": "Success",
                    "message": "Bucketlist item successfully updated"
                })

                response.status_code = 200

            else:
                response = jsonify({
                    "status": "Fail",
                    "message": "Bucketlist item does not belong to bucketlist"
                })

                response.status_code = 404

        else:
            response = jsonify({
                "status": "Fail",
                "message": "Bucketlist item does not exist"
            })

            response.status_code = 404

        return make_response(response)

    @jwt_required
    def delete(self, id, item_id):

        bucketlist_item = BucketlistItem.get_bucketlist_items(item_id)

        if bucketlist_item:
            if bucketlist_item.bucketlist_id == id:

                database.session.delete(bucketlist_item)
                database.session.commit()

                response = jsonify({})

                response.status_code = 204  # Status 204 does not need a message body
            else:
                response = jsonify({
                    "status": "Fail",
                    "message": "Bucketlist item does not belong to bucketlist"
                })

                response.status_code = 404
        else:
            response = jsonify({
                "status": "Fail",
                "message": "Bucketlist item cannot be deleted as it does not exist"
            })

            response.status_code = 404

        return make_response(response)
