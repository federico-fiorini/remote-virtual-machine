import os

# Secret authorization key
AUTHORIZATION_KEY = os.environ.get('AUTHORIZATION_KEY', 'secret_token')
GOOGLE_ENGINE_PROJECT_NAME = os.environ.get('GOOGLE_ENGINE_PROJECT_NAME', 'project_name')
GOOGLE_ENGINE_ZONE = os.environ.get('GOOGLE_ENGINE_ZONE', 'zone')