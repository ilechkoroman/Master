from flask import Blueprint
from flask_restplus import Api

from app.api.namespaces import master as master_ns
from app.api.master import routes as master

API_VERSION_V1 = 1
api_v1_bp = Blueprint('api_v1', __name__)
api_v1 = Api(api_v1_bp)

master_ns.add_resource(master.GET, '/get')
master_ns.add_resource(master.POST, '/post')
master_ns.add_resource(master.Delete, '/delete')

api_v1.add_namespace(master_ns, '/master')
