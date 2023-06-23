import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv 
import os

app = Flask(__name__)
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from flask_app import routes, models
