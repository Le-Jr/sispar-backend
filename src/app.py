from flask import Flask, jsonify
from src.controller.colaborador_controller import bp_employee
from src.controller.reembolso_controller import bp_refund
from src.model import db
from config import config
import os

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    if hasattr(config[config_name], 'init_app'):
        config[config_name].init_app(app)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    app.register_blueprint(bp_employee)
    app.register_blueprint(bp_refund)
    
    return app