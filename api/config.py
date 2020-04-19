import os

class Config(object):
    DEBUG = True
    SECRET = os.getenv('SECRET')


class DevelopConfig(Config):
    DEBUG = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True

class StagingConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopConfig,
    'testing': TestConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
