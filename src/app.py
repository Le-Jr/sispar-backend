from flask import Flask, jsonify
from src.controller.colaborador_controller import bp_employee


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp_employee)
    return app
