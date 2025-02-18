from flask import Blueprint, request, jsonify
from models import Train, Users
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db

train_routes = Blueprint('train_routes', __name__)

# Add a New Train (Admin only)
@train_routes.route('/add_train', methods=['POST'])
@jwt_required()  # Protect the route with JWT
def add_train():
    username = get_jwt_identity()
    user = Users.query.filter_by(username=username).first()
    
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Check the user's role
    if user.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403
    
    data = request.get_json()

    # Check if all required fields are provided in the request
    required_fields = ['train_name', 'train_number', 'source', 'destination', 'total_seats']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Missing {field} in request"}), 400

    # Retrieve the data
    train_name = data['train_name']
    train_number = data['train_number']
    source = data['source']
    destination = data['destination']
    total_seats = data['total_seats']

    # Validate the data (e.g., ensure total_seats is a positive number)
    if not isinstance(total_seats, int) or total_seats <= 0:
        return jsonify({"message": "Total seats must be a positive integer"}), 400

    # Check if a train with the same train_number already exists
    existing_train = Train.query.filter_by(train_number=train_number).first()
    if existing_train:
        return jsonify({"message": "A train with this train number already exists"}), 400

    # Create new Train object
    new_train = Train(
        name=train_name,
        train_number=train_number,
        source=source,
        destination=destination,
        total_seats=total_seats,
        available_seats=total_seats  # Initially set available seats to total seats
    )

    # Add the new train to the database
    db.session.add(new_train)
    db.session.commit()

    return jsonify({"message": f"Train {train_name} added successfully!"}), 201 

# Get Seat Availability (Available trains between source and destination)
@train_routes.route('/seat_availability', methods=['GET'])
def get_seat_availability():
    source = request.args.get('source')
    destination = request.args.get('destination')
    print(source, destination)

    # Find all trains between the given source and destination
    trains = Train.query.filter_by(source=source, destination=destination).all()

    if not trains:
        return jsonify({"message": "No trains found for this route."}), 404

    available_trains = []
    for train in trains:
        available_trains.append({
            "train_id": train.id,
            "train_name": train.name,
            "train_number": train.train_number,
            "source": train.source,
            "destination": train.destination,
            "available_seats": train.available_seats
        })

    return jsonify(available_trains), 200
