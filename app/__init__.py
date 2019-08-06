import os
from flask import Flask

from app import config_data

app_version = 'dev'
app_supporters = []

config_data.load_data()
app = Flask(__name__)

with open(os.path.join(app.root_path, 'version.txt')) as version_file:
    app_version = version_file.readline()

if os.path.exists(os.path.join(app.root_path, 'data/supporters.txt')):
    with open(os.path.join(app.root_path, 'data/supporters.txt')) as supporters_file:
        lines = supporters_file.readlines()
        for line in lines:
            line = config_data.COMMENTS_REGEX.sub('', line)
            if line == '':
                continue
            app_supporters.append(line)

from app import routes, compat_routes

def create_app():
    return app