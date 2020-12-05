import os
from pathlib import Path
from easydict import EasyDict

general_config = EasyDict()
general_config.root = Path(__file__).parent
general_config.celery = EasyDict()
general_config.celery.broker = "redis://redis:6379/0"
general_config.celery.backend = "redis://redis:6379/0"

general_config.first_host = os.environ.get("FIRST_HOST_NAME", '172.19.0.1')
general_config.first_port = os.environ.get("FIRST_HOST_PORT", 5001)
general_config.first_hosts = f"{general_config.first_host}:{general_config.first_port}"

general_config.second_host = os.environ.get("SECOND_HOST_NAME", '172.19.0.1')
general_config.second_port = os.environ.get("SECOND_HOST_PORT", 5002)
general_config.second_hosts = f"{general_config.second_host}:{general_config.second_port}"


class Config(object):
    BUNDLE_ERRORS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


config_map = {
            'development': DevelopmentConfig,
            'testing': TestingConfig,
            'production': ProductionConfig,
            'default': DevelopmentConfig
}
