from flask import Flask, jsonify
from src.controller.colaborador_controller import bp_employee
from src.controller.reembolso_controller import bp_refund
from src.model import db
from config import config
from flask_cors import CORS
from flasgger import Swagger
import os

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec", # <-- Da um nome de referencia para a documentacao
            "route": "/apispec.json/", # <- Rota do arquivo JSON para a construção da documentação
            "rule_filter": lambda rule: True, # <-- Todas as rotas/endpoints serão documentados
            "model_filter": lambda tag: True, # <-- Especificar quuais modelos da entidade serão documentados
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')
    
    
    app = Flask(__name__)
    CORS(app, origins="*")
    app.config.from_object(config[config_name])
    
    if hasattr(config[config_name], 'init_app'):
        config[config_name].init_app(app)
    
    db.init_app(app)
    
    Swagger(app, config=swagger_config)
    
    with app.app_context():
        db.create_all()
    
    app.register_blueprint(bp_employee)
    app.register_blueprint(bp_refund)
    
    return app