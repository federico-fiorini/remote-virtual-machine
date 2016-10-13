from app import app
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery

PROJECT_NAME = app.config['GOOGLE_ENGINE_PROJECT_NAME']
ZONE = app.config['GOOGLE_ENGINE_ZONE']


class GoogleComputeEngine:
    def __init__(self):
        credentials = GoogleCredentials.get_application_default()
        self.compute = discovery.build('compute', 'v1', credentials=credentials)

    def list_instances(self):
        response = self.compute.instances().list(project=PROJECT_NAME, zone=ZONE).execute()
        return response['items']

    def get_instance(self, instance_name):
        response = self.compute.instances().get(project=PROJECT_NAME, zone=ZONE, instance=instance_name).execute()
        return response

    def start_instance(self, instance_name):
        request = self.compute.instances().start(project=PROJECT_NAME, zone=ZONE, instance=instance_name)
        response = request.execute()
        return response

    def stop_instance(self, instance_name):
        request = self.compute.instances().stop(project=PROJECT_NAME, zone=ZONE, instance=instance_name)
        response = request.execute()
        return response
