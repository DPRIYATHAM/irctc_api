from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), nullable=False, default="user")
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    bookings = db.relationship('Booking', back_populates='user', lazy=True)

class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    train_number = db.Column(db.Integer, nullable=False)
    source = db.Column(db.String(255), nullable=False)
    destination = db.Column(db.String(255), nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    bookings = db.relationship('Booking', back_populates='train', lazy=True)

    # Set available_seats to total_seats by default
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.total_seats is not None:
            self.available_seats = self.total_seats

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    train_id = db.Column(db.Integer, db.ForeignKey('train.id'), nullable=False)
    no_of_seats = db.Column(db.Integer, nullable=False)
    booked_at = db.Column(db.DateTime, default=datetime.now)
    user = db.relationship('Users', back_populates='bookings')
    train = db.relationship('Train', back_populates='bookings')