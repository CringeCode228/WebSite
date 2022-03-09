from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import config
from flask_login import LoginManager
from flask_migrate import Migrate

application = Flask(__name__, template_folder="templates")
application.config.from_object(config)
db = SQLAlchemy(application)
loginManager = LoginManager()
loginManager.init_app(application)
migrate = Migrate(application, db, render_as_batch=True)
