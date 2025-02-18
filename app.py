from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from models import db, Users, Train, Booking
from flask_migrate import Migrate
from api.user_routes import user_routes
from api.train_routes import train_routes
from api.booking_routes import booking_routes
from utils.auth import setup_jwt
from dotenv import load_dotenv
from os import getenv

def create_app():
    load_dotenv('secrets.env')

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = getenv('JWT_SECRET_KEY')
    app.config['ADMIN_API_KEY'] = getenv('ADMIN_API_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600

    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    setup_jwt(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'status': 401,
            'sub_status': 42,
            'message': 'The token has expired. Please log in again.'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'status': 401,
            'sub_status': 43,
            'message': 'Invalid token. Please log in again.'
        }), 401

    app.register_blueprint(user_routes, url_prefix='/api/users')
    app.register_blueprint(train_routes, url_prefix='/api/trains')
    app.register_blueprint(booking_routes, url_prefix='/api/bookings')

    return app

app = create_app()

# with app.app_context():
#     db.drop_all()
#     db.create_all()
#     print("Tables created successfully!")

if __name__ == '__main__':
    app.run(debug=True)