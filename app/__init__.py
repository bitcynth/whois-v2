import os
from flask import Flask

from app import config_data

app_version = 'dev'

config_data.load_data()
app = Flask(__name__)

with open(os.path.join(app.root_path, 'version.txt')) as version_file:
    app_version = version_file.readline()

from app import routes, compat_routes

def create_app():
    return app