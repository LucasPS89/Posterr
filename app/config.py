import os
import yaml
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import mysql.connector

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
config_obj = yaml.load(open('config.yaml'), Loader=yaml.Loader)

# override the environment variables
database_url = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = config_obj['SQLALCHEMY_DATABASE_URI'] if database_url is None else database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#MySQL Connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="posterr"
)

migrate = Migrate(app, db)