from flask_restplus import fields
from app.api.namespaces import master as api

request_append_model = api.model('requestModelAppend', {
    'data': fields.String(description='The data which we append', required=True),
    'write_concern': fields.Integer(description='Minimum count of instances where data should be saved')
})

response_apppend_model = api.model('responseModelAppend', {
    'status':  fields.String()
})

delete_response_model = api.model('responseModelDelete', {
    'status':  fields.String()
})


response_get_model = api.model('responseModelGet', {
    'status':  fields.String(),
    'data':  fields.List(fields.String())
})

