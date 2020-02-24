import os


class Operations:
    CONFIRM = "confirm"
    RESET_PASSWORD = "reset-password"
    CHANGE_EMAIL = "change-email"


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    MONGODB_URI = ""


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
