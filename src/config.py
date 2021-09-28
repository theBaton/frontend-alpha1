import os
import datetime

class Development(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    JWT_TOKEN_LOCATION = ["cookies", "headers", "query_string"]
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=2)
    JWT_SECRET_KEY = os.environ['SECRET_KEY']
    JWT_COOKIE_SECURE = False
    JWT_SESSION_COOKIE = False
    JWT_QUERY_STRING_NAME = "token"

    JWT_COOKIE_SAMESITE = "Strict"

class Production(object):
    """
    Production environment configurations
    """
    uri = os.environ['DATABASE_URL']
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI = uri
    SECRET_KEY = os.environ['SECRET_KEY']

    JWT_TOKEN_LOCATION = ["cookies", "headers", "query_string"]
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=2)
    JWT_SECRET_KEY = os.environ['SECRET_KEY']
    JWT_COOKIE_SECURE = True
    JWT_SESSION_COOKIE = False
    JWT_QUERY_STRING_NAME = "token"

    JWT_COOKIE_SAMESITE = "Strict"

app_config = {
    'development': Development,
    'production': Production
}