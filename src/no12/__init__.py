import os

from flask import Flask

from .settings import config
from .api import api
from .extensions import db


__version__ = "0.1.0"


def create_app(config_name=None) -> Flask:
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "development")

    app = Flask("No12")

    app.config.from_object(config[config_name])

    register_extentions(app)

    return app


def register_extentions(app: Flask) -> None:
    api.init_app(app)
    db.init_app(app)
