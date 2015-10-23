# encoding: utf-8

import json
import requests

from .exceptions import PagarmeApiError

class AbstractResource(object):
    def __init__(self):
        raise NotImplementedError

    def handle_response(self, data):
        self.data.update(data)

    def error(self, response):
        data = json.loads(response)
        e = data['errors'][0]
        error_string = e['type'] + ' - ' + e['message']
        raise PagarmeApiError(error_string)

    def create(self, callback=None, callback_error=None):
        url = self.BASE_URL
        pagarme_response = requests.post(url, data=self.get_data())
        if pagarme_response.status_code == 200:
            self.handle_response(json.loads(pagarme_response.content))
            if callback is not None:
                callback(pagarme_response)
        else:
            self.error(pagarme_response.content)
            if callback_error is not None:
                callback_error(pagarme_response)

    def get_data(self):
        return self.data
