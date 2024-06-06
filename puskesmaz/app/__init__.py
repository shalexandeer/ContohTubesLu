from flask import Flask
from flask_cors import CORS
from .config import Config
from .models import create_db_tables

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object(Config)

    with app.app_context():
        create_db_tables()

    from .routes import users, medicine
    app.register_blueprint(users.api)
    app.register_blueprint(medicine.api)

    return app
