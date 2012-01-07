from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import Mail


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('application.cfg')

db = SQLAlchemy(app)
mail = Mail(app)

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = 'login'
