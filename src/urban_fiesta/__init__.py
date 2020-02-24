import os

from flask import Flask

from urban_fiesta.settings import config


def create_app(config_name=None) -> Flask:
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "development")

    app = Flask("urban_fiesta")

    app.config.from_object(config[config_name])

    return app
