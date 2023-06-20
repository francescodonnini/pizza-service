import json

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_file('config.json', load=json.load)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from flask_app import routes, models