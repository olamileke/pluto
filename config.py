import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(16)
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Arsenalfc@localhost:5432/pluto'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    MAIL_BASE_URL = "https://api.mailgun.net/v3/sandboxb3e06f45528541edbc677fe253ca0c00.mailgun.org/messages"
    MAIL_API_KEY = "key-618e6125c452b712ee91e57f028fbd0f"
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
