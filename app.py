
import os
import redis
from rq import Queue
from dotenv import load_dotenv
from flask import Flask,jsonify
from flask_smorest import abort
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from resources.user import blp as UserBlueprint
from db import db
import models
from rq import Queue




def create_app(db_url=None):
    app = Flask(__name__)
   
    load_dotenv()
    redis_url = os.getenv("REDIS_URL")
    connection = redis.from_url(redis_url)

    # Create a queue for background tasks
    app.queue = Queue("emails", connection=connection)
    
   
   

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "flask2"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
  
    api = Api(app)


    with app.app_context():
        db.create_all()

    api.register_blueprint(UserBlueprint)

    return app
