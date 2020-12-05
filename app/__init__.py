from flask import Flask

from general_config import config_map


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])
    config_map[config_name].init_app(app)

    from app.api import api_v1_bp, API_VERSION_V1
    app.register_blueprint(api_v1_bp, url_prefix=f"/api/v{API_VERSION_V1}")

    return app
