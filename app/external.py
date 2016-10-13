import requests
from app import app
import json


class BackEndService:

    TOKEN_SCHEME = "Bearer"
    LIST_ENDPOINT = '/list'

    def __init__(self):
        self.address = app.config['BACKEND_IP']
        self.headers = {
            'Authorization': '%s %s' % (self.TOKEN_SCHEME, app.config['BACKEND_AUTORIZATION_KEY']),
            'Content-Type': 'application/json'
        }

    def post_request(self, endpoint, data):
        """
        Perform POST request
        :param endpoint:
        :param data:
        :return:
        """
        return requests.post(self.prepend_host(endpoint), json.dumps(data), headers=self.headers)

    def prepend_host(self, endpoint):
        """
        Prepend host to endpoint
        :param endpoint:
        :return:
        """
        return self.address.rstrip('/') + endpoint

    def get_application_list(self, location):
        """
        Calls LIST endpoint to get list of applications by location
        :param location:
        :return:
        """
        body = {
            "location": {
                "latitude": location['lat'],
                "longitude": location['lon']
            }
        }

        response = self.post_request(self.LIST_ENDPOINT, body)
        if response.status_code == 200:
            json_response = response.json()
            return json_response['instances']
        else:
            return []
