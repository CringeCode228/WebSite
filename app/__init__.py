from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import config

from flask_login import LoginManager
from flask_migrate import Migrate


application = Flask(__name__, template_folder="templates", static_folder="static")
application.config.from_object(config)
db = SQLAlchemy(application)
db.create_all()
loginManager = LoginManager()
loginManager.init_app(application)
migrate = Migrate(application, db, render_as_batch=True)
