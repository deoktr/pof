# ruff: noqa: FBT003

import os


def env_bool(var, default=None):
    return os.environ.get(var, str(default)) in ["True", "true", "1"]


class Config:
    INPUT_SIZE_LIMIT = int(os.environ.get("INPUT_SIZE_LIMIT", str(200 * 1024)))
    ENABLE_BLACK_FORMAT = env_bool("ENABLE_BLACK_FORMAT", True)
    ENABLE_PYGMENT = env_bool("ENABLE_PYGMENT", True)


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "default": ProductionConfig,
}
