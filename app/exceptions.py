

class TeamException(Exception):
    error_code = "0000"
    message = "Something went wrong."

    def __init__(self, description=None, extra_payload=None, message=None):
        self.description = description
        self.extra_payload = extra_payload
        if message is not None:
            self.message = message

    def __str__(self):
        return str(dict(error_code=self.error_code, message=self.message, description=self.description,
                        extra_payload=self.extra_payload))

    def with_description(self, description):
        self.description = description
        return self

    def code(self):
        pod_code = "07"
        app_code = "01"
        return "{pod_code}{app_code}{error_code}".format(pod_code=pod_code, app_code=app_code,
                                                         error_code=self.error_code)


class ApiValidationException(TeamException):
    error_code = "0001"
    message = "API Validation error"

    def __init__(self, error_messages=None):
        self.error_messages = error_messages
        super(ApiValidationException, self).__init__(description=None, extra_payload=None)

    def __str__(self):
        return str(dict(error_code=self.error_code, message=self.message, description=self.description,
                        extra_payload=self.extra_payload, error_messages=self.error_messages))
