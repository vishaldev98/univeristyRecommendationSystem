import warnings
from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Corrected the usage of __name__
app = Flask(__name__)

app.secret_key = 'sessionKey'

app.config['SQLALCHEMY_ECHO'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Geethadevi%409@localhost:3306/universityrecomendationsystem'
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0

db = SQLAlchemy(app)

from base.com.vo.login_vo import LoginVO  # Ensure this import path is correct

import base.com.controller  # Ensure this import path is correct

# Correct placement for app context
with app.app_context():
    db.create_all()

# Corrected the main guard
if __name__ == '__main__':
    app.run(debug=True)
