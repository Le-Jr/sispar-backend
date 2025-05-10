from flask import Blueprint, jsonify, request
from src.security.security import check_password, hash_password
from src.model.colaborador_model import Employee
from src.model import db
from flasgger import swag_from


bp_employee = Blueprint('colaborador', __name__, url_prefix='/colaborador')

data = "" 

@bp_employee.route('todos-colaboradores', methods = ["GET"])
@swag_from("../docs/colaborador/pegar_colaboradores.yml")
def get_data():
    employees = db.session.execute(
        db.select(Employee)
    ).scalars().all()
    
    employees = [employee.all_data() for employee in employees]
    
    if not employees:
        return jsonify({"message": "Sem colaboradores na lista"}),404
    
    
    return jsonify(employees), 200


@bp_employee.route('/criar', methods=["POST"])
@swag_from('../docs/colaborador/cadastrar_colaborador.yml')
def create_employee():
    requisition_data = request.get_json()
    password = hash_password(requisition_data['password'])

    new_employee = Employee(
        name=requisition_data['name'],
        email=requisition_data['email'],
        password=password,
        job=requisition_data['job'],
        salary=requisition_data['salary']
    )

    db.session.add(new_employee)
    db.session.commit()

    if not requisition_data:
        return jsonify({"Erro": "Insira todos os dados"}), 400

    # Verifica se já existe um crachá igual
    # for employee in data:
    #     if employee['badge'] == requisition_data.get('badge'):
    #         return jsonify({"Erro": "Crachá já existe"}), 400


    # data.append(new_employee)
    return jsonify({"message": "colaborador criado com sucesso"}), 201




@bp_employee.route('login', methods = ["POST"])
@swag_from("../docs/colaborador/login_colaborador.yml")
def login():
    
    requisition_data = request.get_json()
    email = requisition_data.get('email')
    password = requisition_data.get('password')
    
    if not email or not password:
        return jsonify({"message": "preencha todos os campos de login"}), 400
    
    employee = db.session.execute(db.select(Employee).where(Employee.email == email)).scalar()
    
    if not employee:
        return jsonify({"message": "Usuário não encontrado"}), 404
    
    employee = employee.to_dict()
    
    if check_password(password, employee.get('password')):
        return jsonify({"message":  "Login realizado com sucesso"}), 200
    else:
        return jsonify({"message": "Senha incorreta"}),401




@bp_employee.route('/atualizar/<int:id_employee>', methods=['PUT'])
def update_employe_data(id_employee):
    requisition_data = request.get_json()

    employee_encontrado = None
    for employee in data:
        if employee['id'] == id_employee:
            employee_encontrado = employee
            break

    if not employee_encontrado:
        return jsonify({"mensagem": "Usuario não encontrado"}), 404

    # Verifica duplicação de crachá, se ele for alterado
    if 'badge' in requisition_data:
        novo_badge = requisition_data['badge']
        for employee in data:
            if employee['badge'] == novo_badge and employee['id'] != id_employee:
                return jsonify({"Erro": "Crachá já existe"}), 400
        employee_encontrado['badge'] = novo_badge

    if 'name' in requisition_data:
        employee_encontrado['name'] = requisition_data['name']
    if 'job' in requisition_data:
        employee_encontrado['job'] = requisition_data['job']

    return jsonify({'mensagem': 'Dados do colaborador atualizados com sucesso'}), 200
