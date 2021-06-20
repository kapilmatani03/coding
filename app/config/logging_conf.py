# coding=utf-8
"""
LOGGING CONF
"""
import os


def configure_logging(app):
    """
    Logging Setup
    :param app:
    :return:
    """
    import logging.config
    environment = os.environ.get('APP_ENV', 'local')

    logging_conf = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            },
            'logstash': {
                '()': 'logstash_formatter.LogstashFormatterV1'
            }
        },
        'handlers': {
            'null': {
                'level': 'DEBUG', 'class': 'logging.NullHandler',
            },
            'console': {
                'level': 'DEBUG', 'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
            'team_config': {
                'level': 'DEBUG',
                'class': 'logging.handlers.WatchedFileHandler',
                'filename': app.config['LOG_ROOT'] + '/team.log',
                'formatter': 'logstash' if environment == 'production' else 'verbose',
            },
            'request': {
                'level': 'DEBUG',
                'class': 'logging.handlers.WatchedFileHandler',
                'filename': app.config['LOG_ROOT'] + '/request.log',
                'formatter': 'logstash' if environment == 'production' else 'verbose',
            }
        },
        'loggers': {
            'team': {
                'handlers': ['console', 'team_config'],
                'level': 'INFO' if environment == 'production' else 'DEBUG',
                'propagate': False
            },
            '': {
                'handlers': ['console', 'team_config'],
                'level': 'ERROR',
            },
            'treebo_commons.request_tracing': {
                'handlers': ['console', 'team_config'],
                'level': 'INFO',
                'propagate': False
            },
            'request_handler': {
                'handlers': ['console', 'request'],
                'level': 'INFO' if environment == 'production' else 'DEBUG',
                'propagate': False
            }
        }
    }
    logging.config.dictConfig(logging_conf)
