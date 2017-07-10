from flask import Blueprint

from . import views

core_app = Blueprint('core_app', __name__)

bucketlist_view = views.BucketlistAPI.as_view('bucketlist_api')

core_app.add_url_rule('/v1/api/bucketlists/',
                      view_func=bucketlist_view,
                      methods=['POST', 'GET'])

core_app.add_url_rule('/v1/api/bucketlists/<int:id>',
                      view_func=bucketlist_view,
                      methods=['PUT', 'DELETE', 'GET']
)