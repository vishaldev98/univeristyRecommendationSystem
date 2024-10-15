import warnings
from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Ignore specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Initialize Flask app
app = Flask(__name__)

# Application configurations
app.secret_key = 'klrtyhb7890ertcvbnmqwe4561asdfvc'
app.config['SQLALCHEMY_ECHO'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mohith1234@localhost:3306/UniversityRecommendation'
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import models after initializing the app
import base.com.controller

# Create tables within application context
with app.app_context():
    db.create_all()
