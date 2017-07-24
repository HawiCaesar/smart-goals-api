from flask import Blueprint

from . import views

core_app = Blueprint('core_app', __name__)

bucketlist_view = views.BucketlistAPI.as_view('bucketlist_api')
bucketlist_item_view = views.BucketlistItemAPI.as_view('bucketlist_item_api')

core_app.add_url_rule('/v1/api/bucketlists/',
                      view_func=bucketlist_view,
                      methods=['POST', 'GET'])

core_app.add_url_rule('/v1/api/bucketlists/<int:id>',
                      view_func=bucketlist_view,
                      methods=['PUT', 'DELETE', 'GET'])

core_app.add_url_rule('/v1/api/bucketlists/<int:id>/',
                      view_func=bucketlist_item_view,
                      methods=['POST', 'GET'])

core_app.add_url_rule('/v1/api/bucketlists/<int:id>/<int:item_id>',
                      view_func=bucketlist_item_view,
                      methods=['PUT', 'DELETE', 'GET'])
