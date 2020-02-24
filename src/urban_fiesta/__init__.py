import os

from flask import Flask

from urban_fiesta.settings import config
from urban_fiesta.api import api


__version__ = "0.1.0"


def create_app(config_name=None) -> Flask:
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "development")

    app = Flask("urban_fiesta")

    app.config.from_object(config[config_name])

    register_extentions(app)

    return app


def register_extentions(app: Flask) -> None:
    api.init_app(app)
