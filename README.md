# IRCTC (Railway Management System)

### Problem Statement:
Hey there, Mr. X. You have been appointed to design a railway management system like IRCTC, where users can come on the platform and check if there are any trains available between 2 stations. The app will also display how many seats are available between any 2 stations and the user can book a seat if the availability > 0 after logging in. Since this has to be real-time and multiple users can book seats simultaneously, your code must be optimized enough to handle large traffic and should not fail while doing any bookings. If more than 1 users simultaneously try to book seats, only either one of the users should be able to book. Handle such race conditions while booking.

There is a Role Based Access provision and 2 types of users would exist :
1. Admin - can perform all operations like adding trains, updating total seats in a train, etc.
2. Login users - can check availability of trains, seat availability, book seats, get booking details, etc.

### Tech Stack
- Flask (Server)
- Flask-JWT-Extended (Authentication)
- Flask-SQLAlchemy (ORM)
- PostgreSQL (Database)
- Postman (API Testing)

### Requirements
1. Register User (Public)
2. Login User (Public)
3. Add a New Train (Admin)
4. Get Seat Availability (Public)
5. Book a Seat (User)
6. Get Specific Booking Details (User)

- Protect admin API endpoints with API Key
- Booking Seat, Getting Booking details - send Authorized Token (received at Login Endpoint)

### PostgreSQL Database:
- `psql -h localhost -U postgres -d postgres -p 5432`
- `CREATE DATABASE irctc_db;`
- `CREATE USER irctc_user WITH PASSWORD 'IRCTC321';`
- `GRANT ALL PRIVILEGES ON DATABASE irctc_db TO irctc_user;`
- `\q`

### Project Structure

```
irctc/
│
├── app.py                          # Main entry point of the Flask app
├── models.py                       # SQLAlchemy models for database tables (User, Train, Booking)
├── requirements.txt                # List of dependencies
├── migrations/                     # Database migration scripts (if using Flask-Migrate)
│
├── api/                            # API-specific logic
│   ├── __init__.py                 # Initializes the api package
│   ├── user_routes.py              # Routes related to user actions (register, login, etc.)
│   ├── train_routes.py             # Routes related to train actions (add train, get availability)
│   ├── booking_routes.py           # Routes related to booking actions (book seat, get booking details)
│
├── utils/                          # Utility functions (e.g., JWT token generation, role-based access checks)
│   ├── __init__.py
│   ├── auth.py                     # Handles JWT authentication and authorization
│   ├── helpers.py                  # Helper functions for the app (e.g., error handling, validations)
│
└── README.md                       # Project overview and setup instructions
```

### API Endpoints
- POST /register: Register a new user.
![](images/register.png)
- POST /login: Log in to receive a JWT token.
![](images/login.png)
- GET /seat_availability: Get available seats for a route.
![](images/seatavailability.png)
- POST /add_train: Admin endpoint to add a new train.
![](images/addtrain.png)
- POST /book_seat: Book a seat on a train.
![](images/seatsbooked.png)
- GET /booking_details: Get booking details for a user.
![](images/bookingdetails.png)

### Database Migrations
- `flask db init`
- `flask db migrate -m "Initial migration"`
- `flask db upgrade`
- alembic.ini => `sqlalchemy.url = postgresql://postgres:Postgres%40SQL@localhost/irctc_db`

### Run 
- `pip install requriements.txt`
- `flask run --port=8000`



### DARISI PRIYATHAM