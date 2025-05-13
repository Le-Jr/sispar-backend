from flask import Blueprint, jsonify, request
from src.model.reembolso_model import Refund
from src.model import db
from flasgger import swag_from
from sqlalchemy.exc import IntegrityError

bp_refund = Blueprint("reembolso", __name__, url_prefix="/reembolso")




@bp_refund.route("/solicita-reembolso", methods = ["POST"])
@swag_from("../docs/reembolso/solicita_reembolso.yml")
def refund():
    requisition_data = request.get_json()
    
    new_refund = Refund(
        employee = requisition_data.get("employee"),
        company = requisition_data.get("company"),
        installment_num = requisition_data.get("installment_num"),
        description = requisition_data.get("description"),
        date_request = requisition_data.get("date_request"),
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

@bp_refund.route("ver-reembolso/<int:installment_num>", methods = ["GET"])
@swag_from("../docs/reembolso/ver_reembolso.yml")
def refund_view(installment_num):
    
    
    refund = db.session.execute(
        db.select(Refund).where(Refund.installment_num == installment_num)  
    ).scalar()
  
    if not refund:
        return jsonify({"message": "Reembolso não encontrado"}), 404
  
    
    return jsonify(refund.to_dict()), 200


@bp_refund.route("/atualiza-reembolso/<int:installment_num>", methods=["PUT"])
@swag_from("../docs/reembolso/atualizar_reembolso.yml") 
def update_refund(installment_num):
    refund = db.session.execute(db.select(Refund).where(Refund.installment_num == installment_num)).scalar()
    if not refund:
        return jsonify({"mensagem": "Reembolso não encontrado"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"mensagem": "Nenhum dado recebido"}), 400

    # Atualiza os campos se existirem no JSON
    for key in data:
        if hasattr(refund, key):
            setattr(refund, key, data[key])

    db.session.commit()
    return jsonify({"mensagem": "Reembolso atualizado com sucesso"}), 200
 
 

@bp_refund.route("/apagar-reembolso/<int:id>", methods=["DELETE"])
@swag_from("../docs/reembolso/apagar_reembolso.yml")  
def delete_refund(id):
    refund = Refund.query.get(id)
    if not refund:
        return jsonify({"mensagem": "Reembolso não encontrado"}), 404

    try:
        db.session.delete(refund)
        db.session.commit()
        return jsonify({"mensagem": "Reembolso deletado com sucesso"}), 200

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"erro": "Não foi possível deletar. Verifique dependências."}), 409

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500
