from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
admin = Admin(app, template_mode='bootstrap3')
bootstrap = Bootstrap(app)

from flask_app.models import User, Appointment, Review
from flask_app.admin_routes import initialize_admin

initialize_admin(admin)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from flask_app import routes

