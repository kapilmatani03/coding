import functools
import logging
from datetime import datetime
from enum import Enum

from flask import request
from marshmallow import Schema
from werkzeug.exceptions import UnsupportedMediaType

from app.exceptions import ApiValidationException

logger = logging.getLogger(__name__)


class RequestTypes(Enum):
    JSON = 'json'
    ARGS = 'args'
    FORM = 'form'


def prepare_error_list(marshmallow_errors):
    errors = []
    for k, v in marshmallow_errors.items():
        if isinstance(v, dict):
            error_list = prepare_error_list(v)
            error_list = [{"field": "{parent_field}.{child_field}".format(parent_field=k, child_field=error["field"]),
                           "error": error["error"]} for
                          error in error_list]
            errors.extend(error_list)
        else:
            v = v[0] if isinstance(v, list) else v
            errors.append({"field": k, "error": "[{}] -> {}".format(k.replace("_", " ").title(), v)})
    return errors


def parse_data_and_version(schema: Schema, request_attr: RequestTypes, has_version: bool, many: bool):
    """
        @request_attr is 'args' for GET APIs
                         'form' for POST APIs
                         'json' for POST APIs content-type application/json
    """

    def parse_data_and_version_inner(func):
        """
        validate_decorator
        :param func:
        :return:
        """

        def wrapper(*args, **kwargs):
            """
            wrapper
            :param args:
            :param kwargs:
            :return:
            """

            if request_attr == RequestTypes.JSON:
                if 'application/json' not in request.content_type:
                    raise UnsupportedMediaType()
            if request_attr == RequestTypes.JSON and request.content_length == 0:
                data = dict()
            else:
                data = getattr(request, request_attr.value)

            if request_attr in [RequestTypes.ARGS, RequestTypes.FORM]:
                data = dict(data=data.to_dict())

            data['request_time'] = data.get('request_time', datetime.now())

            parsed_data = schema().load(data.get('data', dict()), many=many)
            if parsed_data.errors:
                logger.info("APIValidationError: %s", parsed_data.errors)
                error_messages = prepare_error_list(parsed_data.errors)
                raise ApiValidationException(error_messages=error_messages)

            kwargs['parsed_request'] = parsed_data.data
            if has_version:
                if 'resource_version' not in data:
                    error_messages = [
                        {"field": "resource_version", "error": "[Resource Version] -> This is a required field"}]
                    raise ApiValidationException(error_messages=error_messages)
                kwargs['resource_version'] = data.get('resource_version')
            return func(*args, **kwargs)

        return functools.update_wrapper(wrapper, func)

    return parse_data_and_version_inner


def schema_wrapper_and_version_parser(schema: Schema, many: bool = False, param_type: RequestTypes = RequestTypes.JSON):
    """

    Args:
        schema:
        many:
        param_type:

    Returns:

    """
    return parse_data_and_version(schema, param_type, has_version=True, many=many)


def schema_wrapper_parser(schema: Schema, many: bool = False, param_type: RequestTypes = RequestTypes.JSON):
    """

    Args:
        schema:
        many:
        param_type: json, form, args

    Returns:

    """
    return parse_data_and_version(schema, param_type, has_version=False, many=many)
