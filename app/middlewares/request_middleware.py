# coding=utf-8
"""
Middlewares
"""
import logging
import re

import flask
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound

from app.api import ApiResponse

logger = logging.getLogger(__name__)


def get_http_status_code_from_exception(exception) -> int:
    return 500


def need_error_logging(error):
    if isinstance(error, NotFound):
        return False
    return True


def exception_handler(error, from_consumer=False):
    """
    Exception handler
    :param error:
    :param from_consumer:
    :return:
    """
    # populate status code
    status_code = get_http_status_code_from_exception(error)
    if getattr(error, "status_code", None):
        status_code = error.status_code
    if getattr(error, "code", None):
        status_code = error.code

    if isinstance(error, ValidationError):
        status_code = 400

    if not re.search(r'^[1-5]\d{2}$', str(status_code)):
        status_code = 500

    error_code = None
    # populate error dict
    error_dict = dict(code=status_code)
    # TODO:: causing JSON serializer error for unknown types. Need to find a cleaner solution for this.
    # error_dict['extra_payload'] = error.args if hasattr(error, 'args') else None
    error_dict['extra_payload'] = dict()
    error_dict['message'] = error.message if hasattr(error, 'message') else 'Exception occurred.'
    error_dict['developer_message'] = error.description if hasattr(error, 'description') else str(error)
    error_dict['request_id'] = '' if not from_consumer else None

    response = ApiResponse.build(errors=[error_dict], status_code=status_code)

    if need_error_logging(error):
        if not from_consumer:
            request = flask.request
            request_url = request.url
            request_headers = dict(request.headers)

            if request.is_json:
                request_data = request.json if request.get_json(silent=True) else request.get_data(as_text=True)
            else:
                request_data = request.get_data(as_text=True)

            logger.exception("Exception in api: %s. Request Payload: %s", error, request_data,
                             extra=dict(error_code=error_code, status_code=status_code, request_url=request_url,
                                        request_headers=request_headers, request_data=request_data,
                                        request_method=request.method))
        else:
            logger.exception("Exception in consumer: %s", error, extra=dict(error_code=error_code))

    return response
