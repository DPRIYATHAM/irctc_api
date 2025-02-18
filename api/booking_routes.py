from flask import Blueprint, request, jsonify
from models import Booking, Train, Users
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from sqlalchemy.orm import joinedload  # For optimized querying

booking_routes = Blueprint('booking_routes', __name__)

# Book a Seat
@booking_routes.route('/book_seat', methods=['POST'])
@jwt_required()  # Protect the route with JWT
def book_seat():
    current_user = get_jwt_identity()

    # Get the data sent by the user for booking a seat
    data = request.get_json()
    train_number = data.get('train_number')  # Using train_number instead of train_id
    seats_to_book = data.get('seats_to_book')

    # Validate seats_to_book
    if seats_to_book <= 0:
        return jsonify({"message": "Invalid seat count. Please book at least one seat."}), 400

    # Fetch the train by train_number
    train = Train.query.filter_by(train_number=train_number).first()  # Query by train_number

    if not train:
        return jsonify({"message": "Train not found."}), 404

    # Check if there are enough available seats
    if train.available_seats < seats_to_book:
        return jsonify({"message": "Not enough available seats."}), 400

    user = Users.query.filter_by(username=current_user).first()
    userid = user.id

    # Create a new booking
    booking = Booking(
        user_id=userid,  # Get user ID from JWT
        train_id=train.id,  # We use train_id here since that's how we relate bookings to trains
        no_of_seats=seats_to_book
    )

    # Update the available seats for the train
    train.available_seats -= seats_to_book

    # Commit the transaction
    db.session.add(booking)
    db.session.commit()

    return jsonify({"message": f"Booking successful! {seats_to_book} seat(s) booked on {train.name}."}), 201


# Get Specific Booking Details (All bookings of the logged-in user)
@booking_routes.route('/booking_details', methods=['GET'])
@jwt_required()  # Protect the route with JWT
def get_booking_details():
    current_user = get_jwt_identity()

    # Retrieve all bookings for the current user with optimized query (using joinedload)
    user = Users.query.filter_by(username=current_user).first()
    userid = user.id
    bookings = Booking.query.options(joinedload(Booking.train)).filter_by(user_id=userid).all()

    if not bookings:
        return jsonify({"message": "No bookings found."}), 404

    user_bookings = []
    for booking in bookings:
        train = booking.train  # This is already loaded due to the joinedload
        user_bookings.append({
            "train_id": train.id,
            "train_name": train.name,
            "train_number": train.train_number,
            "source": train.source,
            "destination": train.destination,
            "seats_booked": booking.no_of_seats,
            "booked_at": booking.booked_at
        })

    return jsonify(user_bookings), 200
