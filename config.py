import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(16)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    DB_NAME = "pluto"
    DB_USER = "postgres"
    DB_PASSWORD = "Arsenalfc"
    MAIL_BASE_URL = ""
    MAIL_API_KEY = ""
    MAIL_FROM = "Pluto"
    MAIL_FROM_URL = "<admin@pluto.herokuapp.com>"


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
