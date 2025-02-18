from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, decode_token
import datetime

# Helper function to hash the password
def hash_password(password):
    return generate_password_hash(password)


# Helper function to check password validity (during login)
def check_password(stored_password, provided_password):
    return check_password_hash(stored_password, provided_password)


# Helper function to create JWT token for authentication
def create_jwt_token(user_id, role):
    # Set token expiration time (1 hour)
    expiration = datetime.timedelta(hours=1)
    token = create_access_token(identity={"id": user_id, "role": role}, expires_delta=expiration)
    return token


# Helper function to decode the JWT token and get the user identity
def decode_jwt_token(token):
    try:
        decoded_token = decode_token(token)
        return decoded_token['identity']
    except Exception as e:
        return None


# Utility function to validate if the current user is an admin
def is_admin(user_identity):
    return user_identity.get('role') == 'admin'
