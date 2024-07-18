from flask_app import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_employer = db.Column(db.Boolean, default=False)
    bio = db.Column(db.Text, nullable=True)
    
    # Отношения для отзывов
    reviews_written = db.relationship('Review', foreign_keys='Review.client_id', backref='author', lazy=True)
    reviews_received = db.relationship('Review', foreign_keys='Review.employer_id', backref='recipient', lazy=True)
    
    # Отношения для встреч
    appointments_client = db.relationship('Appointment', foreign_keys='Appointment.client_id', backref='client', lazy=True)
    appointments_employer = db.relationship('Appointment', foreign_keys='Appointment.employer_id', backref='employer', lazy=True)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='Pending')

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
