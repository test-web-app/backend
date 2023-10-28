from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
# from .config import Config
from .models import db
from .schemas import ma
import os


load_dotenv()

app = Flask(__name__)
CORS(app)

# app.config.from_object(Config)
app.config.from_object(os.getenv('APP_SETTINGS'))

db.init_app(app)
ma.init_app(app)

from .routes import *
