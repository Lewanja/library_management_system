from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import Config
import os

db = SQLAlchemy()


def create_library_app():
    current_working_directory = os.getcwd()
    absolute_templates_folder_path = os.path.join(current_working_directory,"templates")
    app = Flask(__name__, template_folder= absolute_templates_folder_path)
    app.config.from_object(Config())

    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app




