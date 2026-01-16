import logging

from flask import Flask

from . import routes
from .config import config

logger = logging.getLogger(__name__)


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    app.register_blueprint(routes.main_bp)
    app.register_blueprint(routes.pof_bp)

    return app
