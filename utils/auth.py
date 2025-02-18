from models import Users
from flask_jwt_extended import JWTManager

def setup_jwt(app):
    jwt = JWTManager(app)

    # This part remains unchanged; you're setting up how to get the user identity (e.g., username)
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user

    # The new approach: Replace user_claims_loader with user_lookup_loader
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        # print("JWT Data", jwt_data)
        username = jwt_data["sub"]  # Now, identity is the username
        user = Users.query.filter_by(username=username).first()  # Query the user by username
        return user
    
    # If you need to add custom claims to the JWT (like role), do it when generating the JWT (typically in your login route)
