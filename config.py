from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'da0caa0551505add1e5a786420a19f1a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_web3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


import routes
