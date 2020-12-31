from flask_restplus import Resource
from flask import request

from app.api.decorators import post_response, get_response, delete_response
from app.celery.replicate import replicate_task
from app.api.master.models import api, request_append_model, response_apppend_model, response_get_model

from logger_tools import setup_logger
from general_config import general_config
INMEMORY_LIST = dict()
READ_ONLY = False

logger = setup_logger("Master")


@api.header('Content-Type', 'application/json')
class POST(Resource):
    @api.expect(request_append_model)
    @api.response(200, 'Success', response_apppend_model)
    @post_response
    def post(self):
        global INMEMORY_LIST
        global READ_ONLY
        logger.info('Parsing post data')
        post_data = request.get_json(force=True, silent=True) or {}
        data = post_data.get('data')
        concern_count = post_data.get('write_concern', 1)

        if not READ_ONLY:
            task_fst_response = replicate_task.apply_async((data, general_config.first_hosts, INMEMORY_LIST))
            task_scnd_response = replicate_task.apply_async((data, general_config.second_hosts, INMEMORY_LIST))

            logger.info('Adding to memory list in master')
            key = f'{task_fst_response.id}:{len(list(INMEMORY_LIST.values()))}'
            INMEMORY_LIST[key] = data
            self.monitoring([task_fst_response, task_scnd_response], concern_count)
            logger.info(f'{concern_count - 1} instance(s) replicated')

            return {'status': 'success'}
        return {'status': 'fail', 'message': 'No one from secondaries are available read only mode'}

    def monitoring(self, tasks, concern_count):
        concern_reached = 1
        global READ_ONLY

        while concern_reached < concern_count:
            unresponse_instances = 0
            for task in tasks:
                task_response = replicate_task.AsyncResult(task.id)

                if task_response:
                    status = task_response.state
                    health = task_response.info['health'] if task_response.info else 'undefined'

                if health == 'UNHEALTHY':
                    unresponse_instances += 1
                if unresponse_instances == 2:
                    logger.info(f'{unresponse_instances} INSTANCES DO NOT RESPONSE, SWAPPED TO READ_ONLY MODE')
                    READ_ONLY = True
                if status == 'SUCCESS':
                    concern_reached = concern_reached + 1
                    logger.info(f'Task with id {task.id} finished')
                elif status == 'FAILURE':
                    logger.info(task_response.traceback)
                    return


@api.header('Content-Type', 'application/json')
class GET(Resource):
    @api.response(200, 'Success', response_get_model)
    @get_response
    def get(self):
        return {'status': 'success', 'data': list(INMEMORY_LIST.values())}
