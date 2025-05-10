from flask import Blueprint, jsonify, request
from src.model.reembolso_model import Refund
from src.model import db

bp_refund = Blueprint("reembolso", __name__, url_prefix="/reembolso")
data = ""

@bp_refund.route("/teste")
def initial():
    return jsonify({"message": "Hello world!"})


@bp_refund.route("/solicita-reembolso", methods = ["POST"])
def refund():
    requisition_data = request.get_json()
    
    new_refund = Refund(
        employee = requisition_data.get("employee"),
        company = requisition_data.get("company"),
        installment_num = requisition_data.get("installment_num"),
        description = requisition_data.get("description"),
        date = requisition_data.get("date"),
        refund_type = requisition_data.get("refund_type"),
        cost_center = requisition_data.get("cost_center"),
        intern_order = requisition_data.get("intern_order"),
        division = requisition_data.get("division"),
        pep = requisition_data.get("pep"),
        currency = requisition_data.get("currency"),
        km_distance = requisition_data.get("km_distance"),
        km_value = requisition_data.get("km_value"),
        incoming_value = requisition_data.get("incoming_value"),
        expenses = requisition_data.get("expenses"),
        id_employee = requisition_data.get("id_employee"),
        status = requisition_data.get("status"),
    )
    
    db.session.add(new_refund)
    db.session.commit()
    
    if not requisition_data:
        return jsonify({"message": "Insira todos os dados"}), 400
    
    
    return jsonify({"message": "Solicitação reembolso feita com sucesso"}),201