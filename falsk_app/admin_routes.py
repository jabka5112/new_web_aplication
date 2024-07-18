from flask_admin.contrib.sqla import ModelView
from flask_app import db
from flask_app.models import User, Appointment, Review

def initialize_admin(admin):
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Appointment, db.session))
    admin.add_view(ModelView(Review, db.session))
