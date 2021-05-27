import os


class BaseConfig:
    """ Base configuration """
    TESTING = False
    DEBUG = True
    ELASTIC_URL = os.environ.get('ELASTIC_URL')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


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
