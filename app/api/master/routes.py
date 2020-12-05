from flask_restplus import Resource
from flask import request

from app.api.decorators import post_response, get_response, delete_response
from app.celery.replicate import replicate_task
from app.api.master.models import api, request_append_model, response_apppend_model, response_get_model, \
    delete_response_model

from logger_tools import setup_logger
from general_config import general_config
INMEMORY_LIST = list()

logger = setup_logger("Master")


@api.header('Content-Type', 'application/json')
class POST(Resource):
    @api.expect(request_append_model)
    @api.response(200, 'Success', response_apppend_model)
    @post_response
    def post(self):
        global INMEMORY_LIST
        logger.info('Parsing post data')
        post_data = request.get_json(force=True, silent=True) or {}
        data = post_data.get('data')

        task_fst_response = replicate_task.apply((data, general_config.first_hosts, 'append'))

        if task_fst_response.result['status'] != 'success':
            return task_fst_response.result
        logger.info('First instance replicated')

        task_scnd_response = replicate_task.apply((data, general_config.second_hosts, 'append'))
        if task_scnd_response.result['status'] != 'success':
           return task_scnd_response.result
        logger.info('Second instance replicated')

        logger.info('Adding to memory list in master')
        INMEMORY_LIST.append(data)

        return {'status': 'success'}


@api.header('Content-Type', 'application/json')
class GET(Resource):
    @api.response(200, 'Success', response_get_model)
    @get_response
    def get(self):
        return {'status': 'success', 'data': INMEMORY_LIST}


@api.header('Content-Type', 'application/json')
class Delete(Resource):
    @api.response(200, 'Success', delete_response_model)
    @delete_response
    def delete(self):
        global INMEMORY_LIST
        if not len(INMEMORY_LIST):
            logger.info('Instance not replicated')
            return {"status": "fail", "message":  f"List is empty"}

        task_fst_response = replicate_task.apply((None, general_config.first_hosts, 'delete'))
        if task_fst_response.result['status'] != 'success':
            logger.info('First instance not replicated')
            return task_fst_response
        logger.info('First instance replicated')

        task_scnd_response = replicate_task.apply((None, general_config.second_hosts, 'delete'))
        if task_scnd_response.result['status'] != 'success':
           logger.info('Second instance not replicated')
           return task_scnd_response
        logger.info('Second instance replicated')

        INMEMORY_LIST.pop(-1)
        return {"status": "success"}
