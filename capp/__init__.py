from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

application = Flask(__name__)

application.config['SECRET_KEY'] = os.environ['SECRET_KEY']
# application.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

# database-configurations
# application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
# application.config["SQLALCHEMY_BINDS"] = {"transport" : "sqlite:///transport.db"}
# application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # removes error-message


DBVAR = f"postgresql://{os.environ['RDS_USERNAME']}:{os.environ['RDS_PASSWORD']}@{os.environ['RDS_HOSTNAME']}/{os.environ['RDS_DB_NAME']}"
# DBVAR = 'postgresql://postgres:123456789@awseb-e-2ipvud5qgq-stack-awsebrdsdatabase-ylzlkxcf8cju.cdys4seamvnp.eu-north-1.rds.amazonaws.com:5432/ebdb'
application.config['SQLALCHEMY_DATABASE_URI'] = DBVAR 
application.config['SQLALCHEMY_BINDS'] ={'transport': DBVAR}

db = SQLAlchemy(application)

# encrypting passwords in database
bcrypt = Bcrypt(application)

# flask login-manager
login_manager= LoginManager(application)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from capp.home.routes import home
from capp.methodology.routes import methodology
from capp.carbon_calc.routes import carbon_calc
from capp.users.routes import users
from capp.carbon_interface.routes import carbon_interface

application.register_blueprint(home)
application.register_blueprint(methodology)
application.register_blueprint(carbon_calc)
application.register_blueprint(users)
application.register_blueprint(carbon_interface)
