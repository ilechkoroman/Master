from __future__ import absolute_import, unicode_literals
import requests
import time

from app.celery.app import app
from logger_tools import setup_logger
from general_config import general_config

logger = setup_logger("Replicate_task")


@app.task(bind=True)
def replicate_task(self, data, hosts, all_data):
    health = 'HEALTHY'
    self.update_state(status='PROGRESS',
                      meta={'current_state': f'started task', 'health':health})
    retry_time_out = 2
    time_failed = 0
    delivered = False

    message_id = f'{self.request.id}:{len(list(all_data.values()))}'

    instance_map = {True: 'first instance', False: 'second instance'}
    node = 'secondary'
    instance = instance_map[hosts == general_config.first_hosts]

    self.update_state(status=f'PROGRESS',
                      meta={'current_state': 'making url and body', 'health':health})
    logger.info(f'{instance} got id {self.request.id}')

    url = f'http://{hosts}/api/v1/{node}/post'
    header = {'content-type': 'application/json'}
    body = {'data': f'{message_id}:{data}'}  # {unique_id}:{position_index}:{message}

    logger.info(f'URL {url}')
    logger.info(f'Body {body}')
    logger.info(f'Header {header}')

    logger.info(f'Making request for {instance}')
    self.update_state(status=f'PROGRESS',
                      meta={'current_state': f'making request for {instance}', 'health':health})

    while not delivered:
        if time_failed > 0:
            logger.info(f'Error occurred, retrying with {retry_time_out} seconds')
            time.sleep(retry_time_out)
            retry_time_out *= 2
        try:
            request = requests.post(url, json=body, headers=header).json()
        except ConnectionError:
            request = {'status': 'fail', 'error': 'ConnectionError'}

        if request['status'] != 'success':
            time_failed += 1
            health = 'SUSPECTED' if time_failed == 1 else 'UNHEALTHY'

            self.update_state(status=f'PROGRESS',
                              meta={'current_state': f'making retry request for {instance}', 'health':health})
            logger.info(request)
        else:
            time_failed = 0
            health = 'HEALTHY'
            delivered = True

    return {'status': f'success', 'current_state': 'Task completed!', 'health':health}
