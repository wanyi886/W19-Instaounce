import os



from flask import Flask
from flask_migrate import Migrate
# from .config import Configuration
from app.models import db

app = Flask(__name__)
db.init_app(app)
migrate = Migrate(app, db)
app.config.from_mapping({
  "SQLALCHEMY_DATABASE_URI": os.environ.get("DATABASE_URL"),
  "SQLALCHEMY_TRACK_MODIFICATIONS":False
})
