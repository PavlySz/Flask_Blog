from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '30e1868705bbff6e96f9771f3c2232a6'           # Secret key to prevernt cookies from being stolen
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'             # Database directory
db = SQLAlchemy(app)                                                    # Create a database using SQLAlchemy
bcrypt = Bcrypt(app)                                                    # Used for hashing the user data
login_manager = LoginManager(app)                                       # Login manager 
login_manager.login_view = 'login'                                      # Name of the function in routes.py if the user tried to access a page that requires the user to be logged in, he OR SHE will be redirected to this webpage
login_manager.login_message_category = 'info'                           # Set the Bootstrap class for the login message

# Mail info
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'                       # Gmail as server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('FLASK_BLOG_EMAIL_USER')   # Environment variable - user email
app.config['MAIL_PASSWORD'] = os.environ.get('FLASK_BLOG_EMAIL_PASS')   # Environment variable - user password
mail = Mail(app)

from flaskblog import routes