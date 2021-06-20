# coding=utf-8
"""
App Initiate file
"""
import logging
import os

import click
from flask import Flask
from healthcheck import HealthCheck
from healthcheck.healthcheck import rds_available

from app.api.team_api import team_bp
from app.config.app_config import DefaultConfig

from app.config.logging_conf import configure_logging
from app.extensions import db, migrate
from app.middlewares.request_middleware import exception_handler

logger = logging.getLogger(__name__)


def create_app():
    """
    Create App
    :return:
    """
    app = Flask(__name__, instance_relative_config=True,
                instance_path=os.environ.get('FLASK_APP_INSTANCE_PATH'))
    setup_config(app)
    register_extensions(app)
    register_blueprints(app, "")
    register_commands(app)
    app.before_request_funcs = {None: app.config['BEFORE_REQUEST_MIDDLEWARES']}
    app.after_request_funcs = {None: app.config['AFTER_REQUEST_MIDDLEWARES']}
    register_error_handlers(app)
    setup_health_check(app)

    return app


def register_app_services():
    from object_registry import finalize_app_initialization
    finalize_app_initialization()


def register_commands(app):
    """Register Click commands."""
    pass


def setup_health_check(app):
    """

    :param app:
    :return:
    """
    health = HealthCheck(app, '/api/health', ['rds'])
    health.add_check(rds_available)


def register_error_handlers(app):
    """

    :param app:
    :return:
    """
    app.register_error_handler(Exception, exception_handler)


def setup_config(app):
    """"
    """
    environment = os.environ.get('APP_ENV', 'local')
    # load the default config
    app.config.from_object(DefaultConfig)
    # load from config set by the app
    try:
        app.config.from_envvar('CONFIG_FILE_PATH', silent=False)
    except RuntimeError:
        if not os.environ.get('CONFIG_FILE_PATH'):
            click.echo("CONFIG_FILE_PATH environment variable is not set. Default Config will be used")
        else:
            click.echo("Couldn't load config file from: %s" % os.environ.get('CONFIG_FILE_PATH'))

    click.echo("Setting up Flask App: '%s', using environment: '%s', and config file: %s" % (
        __name__, environment, os.environ.get('CONFIG_FILE_PATH', 'DefaultConfig')))
    configure_logging(app)


def register_extensions(app):
    """
    Registering extensions
    :param app:
    :return:
    """
    db.init_app(app)
    migrate.init_app(app)


def register_blueprints(app, url_prefix=None):
    """
    Registering BluePrints
    :param app:
    :param url_prefix:
    :return:
    """
    app.register_blueprint(team_bp,
                           url_prefix=url_prefix + team_bp.url_prefix if url_prefix else team_bp.url_prefix)


