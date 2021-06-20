import requests

from object_registry import register_instance


@register_instance(dependencies=[])
class NotificationClient(object):

    def send_notification(self, phone_number):

        data = {
            "phone_number": phone_number,
            "message": "Too many 5xx"
        }
        self.send(data)

    def send(self, data):
        url = "https://run.mocky.io/v3/fd99c100-f88a-4d70-aaf7-393dbbd5d99f"
        response = requests.post(url=url, data=data)
        if response.status_code == 200:
            return response.json
        else:
            raise Exception