import os

BASE_DIR= os.path.dirname(__file__)
TESTING = True
CSRF_ENABLED = False
ON_MISSING_ROLE = {'admin': None, 'login': 401}