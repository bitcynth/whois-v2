from flask import Flask

from app import config_data

config_data.load_data()
app = Flask(__name__)

from app import routes
#from app.parsing import icann_parser