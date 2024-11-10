import warnings
from datetime import timedelta

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Ignore specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Initialize Flask app
app = Flask(__name__)

# Application configurations
app.secret_key = 'klrtyhb7890ertcvbnmqwe4561asdfvc'
app.config['SQLALCHEMY_ECHO'] = True  # Enable SQL query logging
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ssgs1970@localhost:3306/universityrecommendation'
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0  # Prevent exceeding the pool size

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import models
from base.com.vo.login_vo import LoginVO  # Import your models here

# Import controllers after db initialization
import base.com.controller




# Create tables within application context
with app.app_context():
    db.create_all()  # This will create all tables based on your models

if __name__ == '__main__':
    app.run(debug=True)  # Optional: Run the app for testing
