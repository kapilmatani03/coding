from decimal import Decimal
from enum import Enum

from flask import jsonify
from flask.helpers import make_response


def make_jsonify_ready(obj):
    if isinstance(obj, list):
        response_list = list()
        for item in obj:
            response_list.append(make_jsonify_ready(item))
        return response_list
    if isinstance(obj, dict):
        response_dict = dict()
        for key, val in obj.items():
            response_dict[key] = make_jsonify_ready(val)
        return response_dict
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, Enum):
        return obj.value
    return obj


class ApiResponse:
    @staticmethod
    def build(status_code, data=None, errors=None, meta=None, resource_version=None):
        if not meta:
            meta = dict()
        if data is None:
            data = dict()
        if not errors:
            errors = list()
        response = dict(data=data, errors=errors, meta=meta)
        if resource_version:
            response['resource_version'] = resource_version
        response = make_jsonify_ready(response)
        return make_response(jsonify(response), status_code)
