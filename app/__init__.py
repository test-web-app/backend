from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from .models import db
from .schemas import ma
from .routes import setup_routes
import os


def create_app(env):
    load_dotenv(f'.env.{env}')
    
    app = Flask(__name__)

    CORS(app)

    app.config.from_object(os.getenv('APP_SETTINGS'))

    db.init_app(app)
    ma.init_app(app)

    setup_routes(app)
    return app
