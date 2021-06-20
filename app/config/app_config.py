import os

app_env = os.environ.get('APP_ENV')


class DefaultConfig(object):
    """
    Base config
    """
    DEBUG = app_env != 'production'
    TESTING = app_env == 'testing'

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_USER = os.environ.get("DB_USER", "postgres")
    DB_MASTER_URL = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB = "teams_app"
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}?application_name=app'.format(
        DB_USER, DB_PASSWORD, DB_MASTER_URL, DB_PORT, DB)


    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'ERROR')
    LOG_ROOT = os.environ.get('LOG_ROOT', '.')

    # Middlewares
    WSGI_MIDDLEWARES = []
    BEFORE_REQUEST_MIDDLEWARES = []
    AFTER_REQUEST_MIDDLEWARES = []

    # URL Paths
    JSONIFY_PRETTYPRINT_REGULAR = False
