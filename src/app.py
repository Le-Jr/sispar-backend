from flask import Flask, jsonify
from src.controller.colaborador_controller import bp_employee
from src.model import db
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    app.register_blueprint(bp_employee)
    return app
