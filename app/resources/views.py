import datetime
from flask import request, make_response, jsonify
from flask.views import MethodView
from app import get_jwt_identity, jwt_required
from app.models import Bucketlist, BucketlistItem, database
from app.helpers import PaginationHelper


class BucketlistAPI(MethodView):
    """ Create Read Update Delete Bucketlist """

    @jwt_required
    def post(self):
        now = datetime.datetime.now()
        data = request.get_json()

        current_user = get_jwt_identity()

        bucketlist_exists = Bucketlist.query.filter_by(name=data.get('name'), created_by=current_user).first()

        if not bucketlist_exists:

            bucketlist = Bucketlist(name=data.get('name'), created_by=current_user, date_created=now)
            bucketlist.save()  # Save bucketlist name

            response = jsonify({
                'status': "Success",
                'message': "Bucketlist Created"
            })

            response.status_code = 201

        else:

            response = jsonify({
                'status': "Fail",
                'message': "Bucketlist already exists"
            })

            response.status_code = 409

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

                bucketlist_items = []

                response = {
                    'id': bucketlist.id,
                    'name': bucketlist.name
                }

                if bucketlist.items.all():

                    for item in bucketlist.items.all():
                        bucketlist_items.append({item.item_id: item.item_name})

                    response['items'] = bucketlist_items

                else:
                    response['items'] = []

                response = jsonify(response)
                response.status_code = 200

        else:
            try:

                if start is None:
                    start = 1

                if limit is None:
                    limit = 5

                bucketlist_results = []

                if query is None:
                    bucketlist_results = Bucketlist.get_all_bucketlists(current_user)

                else:
                    searchterm = '%' + query + '%'
                    bucketlist_results = Bucketlist.query.filter(Bucketlist.name.like(searchterm))\
                        .filter_by(created_by=current_user).all()

                if not bucketlist_results:

                    response = jsonify({
                        "status": "Success",
                        "message": "Bucketlists Do Not Exist",
                        "results": []
                    })
                    response.status_code = 200

                    return make_response(response)

                prepared = PaginationHelper('/v1/api/bucketlists/', int(start), int(limit))

                list_results = prepared.paginate_results(bucketlist_results)

                final_list = []

                item_list = []

                for bucket in list_results['results']:
                    result = {
                        'id': bucket.id,
                        'name': bucket.name
                    }

                    if bucket.items.all():

                        for item in bucket.items.all():
                            item_list.append({'item_id': item.item_id, 'item_name': item.item_name})

                        result['items'] = item_list

                    else:
                        result['items'] = []

                    final_list.append(result)

                response = jsonify({"previous": list_results['previous'], "next": list_results['next'],
                                    "results": final_list})
                response.status_code = 200

            except ValueError:

                response = jsonify({
                    "status": "Fail",
                    "message": "Start Page and Limits should be numbers only"
                })
                response.status_code = 500

        return make_response(response)

    @jwt_required
    def put(self, id):
        current_user = get_jwt_identity()

        if id:
            bucketlist = Bucketlist.query.filter_by(id=id, created_by=current_user).first()
            data = request.get_json()

            if bucketlist:
                bucketlist.name = data.get("name")
                bucketlist.save()
                response = jsonify({
                    "status": "Success",
                    "message": "Bucketlist successfully updated"
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
        current_user = get_jwt_identity()

        if id:
            bucketlist = Bucketlist.query.filter_by(id=id, created_by=current_user).first()

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
                'status': "Fail",
                'message': "Bucketlist Item Already Exists"
            })

            response.status_code = 409  # 409 means there is a conflict with db as two of the same resource exists

        return make_response(response)

    @jwt_required
    def get(self, **kwargs):

        start = request.args.get('start')
        limit = request.args.get('limit')
        query = request.args.get('q')

        current_user = get_jwt_identity()

        if kwargs.get('id') is not None and kwargs.get('item_id') is not None:

            buckelist_item = BucketlistItem.get_bucketlist_items(kwargs['id'], kwargs['item_id'], current_user)

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

                response = jsonify({
                    "status": "Fail",
                    "message": "That bucketlist item does not exist in bucketlist"
                })
                response.status_code = 404

        elif kwargs.get('id') is not None:

            try:

                if start is None:
                    start = 1

                if limit is None:
                    limit = 5

                start = int(start)
                limit = int(limit)

            except ValueError:

                response = jsonify({
                    "status": "Fail",
                    "message": "Start Page and Limits should be numbers only"
                })
                response.status_code = 500

                return make_response(response)

            items_returned = []
            item_results = []

            if query is None:

                get_results = Bucketlist.query.filter_by(id=kwargs['id'], created_by=current_user).all()

                if not get_results:
                    response = jsonify({
                        "status": "Fail",
                        "message": "No Bucketlist Items Because Bucketlist Does Not Exist",
                    })
                    response.status_code = 404

                    return make_response(response)

                for bucketlist in get_results:

                    if not bucketlist.items.all():
                        response = jsonify({
                            "status": "Success",
                            "message": "No Bucketlist Items in this Bucketlist",
                            "results": bucketlist.items.all()
                        })
                        response.status_code = 200

                        return make_response(response)

                    items_returned.append(bucketlist.items.all())

                for r in items_returned:
                    for final in r:
                        item_results.append(final)

            else:
                query = '%' + query + '%'

                item_results = BucketlistItem.query.\
                    filter_by(bucketlist_id=kwargs['id']).\
                    filter(BucketlistItem.item_name.like(query)).\
                    join(Bucketlist, BucketlistItem.bucketlist_id == Bucketlist.id).\
                    filter_by(created_by=current_user).all()

                if not item_results:
                    response = jsonify({
                        "status": "Fail",
                        "message": "Bucketlist Item does not exist"
                    })
                    response.status_code = 404

                    return make_response(response)

            prepared = PaginationHelper('/v1/api/bucketlists/'+str(kwargs['id'])+'/items/',
                                        start, limit)

            list_results = prepared.paginate_results(item_results)

            all_items = []
            for buckelist_item in list_results['results']:
                item_response = {
                    'item_name': buckelist_item.item_name,
                    'date_created': buckelist_item.date_created,
                    'date_modified': buckelist_item.date_modified,
                    'done': buckelist_item.done,
                    'complete_by': buckelist_item.complete_by,
                    'bucketlist_id': buckelist_item.bucketlist_id
                }
                all_items.append(item_response)

            response = jsonify({"previous": list_results['previous'], "next": list_results['next'],
                                "results": all_items})
            response.status_code = 200

        return make_response(response)

    @jwt_required
    def put(self, id, item_id):
        data = request.get_json()

        current_user = get_jwt_identity()

        bucketlist_item = BucketlistItem.get_bucketlist_items(id, item_id, current_user)

        if bucketlist_item:
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
                "message": "Bucketlist item does not exist"
            })

            response.status_code = 404

        return make_response(response)

    @jwt_required
    def delete(self, id, item_id):

        current_user = get_jwt_identity()

        bucketlist_item = BucketlistItem.get_bucketlist_items(id, item_id, current_user)

        if bucketlist_item:

            BucketlistItem.delete(bucketlist_item)

            response = jsonify({})

            response.status_code = 204  # Status 204 does not need a message body

        else:
            response = jsonify({
                "status": "Fail",
                "message": "Bucketlist item cannot be deleted as it does not exist"
            })

            response.status_code = 404

        return make_response(response)
