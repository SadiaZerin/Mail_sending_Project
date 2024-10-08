from sqlite3 import OperationalError
from flask.views import MethodView
import base64
import json
from flask import current_app
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from db import db
from models import UserModel
from schemas import UserSchema
from tasks import createAndSend_email_message
from validate_email import validate_email
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from rq import Retry

blp = Blueprint("Users", "users", description="Operations on users")


# to register user at POST/register end point and add them in a database

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
     
            is_validate = validate_email(user_data["email"],verify=True)
            # Check if the user with the provided email already exists
            if UserModel.query.filter(UserModel.email == user_data["email"]).first():
              abort(409, message="A user with that email already exists.")
            if not is_validate:
                abort(409, message="Email invalid")

             try:
                with open('token.json') as token_file:
                    token_data = json.load(token_file)
                    if 'https://www.googleapis.com/auth/gmail.send' in token_data.get('scopes', []):
                        # Gmail API token detected
                        pass 
                    else:
                        # Non-Gmail API token detected
                        abort(403, message="The provided token does not represent a Gmail API.")
            except FileNotFoundError:
                abort(403, message="token.json is empty or missing. Please provide valid Gmail API credentials.")
            

            # Create a new user with the provided email
            user = UserModel(
                first_name= user_data['first_name'],
                last_name = user_data['last_name'],
                email=user_data["email"]

            )
            
            if db:
                db.session.add(user)
                try:
                    db.session.commit()
                    current_app.queue.enqueue(
                            create_email_message, user_data["email"], user_data['first_name'], user_data['last_name'],retry=Retry(
                                max=3,interval=[30,2*3600,6*3600]
                            )
                        )
                    if create_email_message(user_data["email"],user_data['first_name'], user_data['last_name']):
                        return {"message": "Email sent successfully"}, 201
                except:
                    db.session.rollback
                    abort(409, message="An error occurred while sending the email. Try again later")

            else:
                abort(409, message="Database connection failure")
       


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):

        # Retrieve the user from the database by user_id or return a 404 Not Found error if not found
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):

        # Retrieve the user from the database by user_id or return a 404 Not Found error if not found
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200


