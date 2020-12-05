from __future__ import absolute_import, unicode_literals
import requests

from app.celery.app import app
from logger_tools import setup_logger
from general_config import general_config

logger = setup_logger("Replicate_task")


@app.task(bind=True)
def replicate_task(self, data, hosts, mode):
    instance_map = {True: 'first instance', False: 'second instance'}
    mode_map = {'append': 'post', 'delete': 'delete'}
    node = 'secondary'

    instance = instance_map[hosts == general_config.first_hosts]
    url = f'http://{hosts}/api/v1/{node}/{mode_map[mode]}'
    header = {'content-type': 'application/json'}
    body = {'data': data}

    logger.info(f'URL {url}')
    logger.info(f'Body {body}')
    logger.info(f'Header {header}')

    logger.info(f'Making request for {instance}')
    if mode_map[mode] == 'post':
        request = requests.post(url, json=body, headers=header).json()
    elif mode_map[mode] == 'delete':
        request = requests.delete(url, headers=header).json()
    if request['status'] != 'success':
        return request
    return {'status': 'success', 'current_state': 'Task completed!'}
