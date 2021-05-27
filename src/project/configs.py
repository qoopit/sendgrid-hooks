import os


class BaseConfig:
    """ Base configuration """
    TESTING = False
    DEBUG = True
    ELASTIC_URL = os.environ.get('ELASTIC_URL')

class DevelopmentConfig(BaseConfig):
    """ Development configuration """
    SQLALCHEMY_ECHO = True
    pass


class TestingConfig(BaseConfig):
    """ Testing configuration """
    TESTING = True


class StagingConfig(BaseConfig):
    """ Staging configuration """
    pass


class ProductionConfig(BaseConfig):
    """ Production configuration """
    DEBUG = False
