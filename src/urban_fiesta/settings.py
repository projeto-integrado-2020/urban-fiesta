import os


class Operations:
    CONFIRM = "confirm"
    RESET_PASSWORD = "reset-password"
    CHANGE_EMAIL = "change-email"


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    MONGODB_URI = ""
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
