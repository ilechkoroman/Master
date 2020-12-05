from __future__ import absolute_import, unicode_literals

from celery import Celery
from general_config import general_config

app = Celery('hw',
             broker=general_config.celery.broker,
             backend=general_config.celery.backend,
             include=['app.celery.replicate'])

app.conf.update(
    result_expires=360000,
)

if __name__ == '__main__':
    app.start()
