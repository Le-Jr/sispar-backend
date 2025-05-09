from flask import Blueprint, jsonify, request
from src.model.colaborador_model import Employee
from src.model import db

bp_employee = Blueprint('colaborador', __name__, url_prefix='/colaborador')

data = [
    {'id': 1, 'nome': 'Samuel Silvério', 'cargo': 'Desenvolvedor Back-end', 'cracha': 'BE12310'},
    {'id': 2, 'nome': 'Karynne Moreira', 'cargo': 'Desenvolvedora Front-end', 'cracha': 'FE21310'},
    {'id': 3, 'nome': 'Joy Assis', 'cargo': 'Desenvolvedora Fullstack', 'cracha': 'FS12110'},
]

@bp_employee.route('todos-colaboradores')
def get_data():
    employees = db.session.execute(
        db.select(Employee)
    ).scalars().all()
    
    employees = [employee.all_data() for employee in employees]
    
    return jsonify(employees), 200


@bp_employee.route('/criar', methods=["POST"])
def create_employee():
    requisition_data = request.get_json()

    new_employee = Employee(
        name=requisition_data['name'],
        email=requisition_data['email'],
        password=requisition_data['password'],
        job=requisition_data['job'],
        salary=requisition_data['salary']
    )

    db.session.add(new_employee)
    db.session.commit()

    if not requisition_data:
        return jsonify({"Erro": "Insira todos os dados"}), 400

    # Verifica se já existe um crachá igual
    for employee in data:
        if employee['badge'] == requisition_data.get('badge'):
            return jsonify({"Erro": "Crachá já existe"}), 400


    data.append(new_employee)
    return jsonify({"message": "colaborador criado com sucesso"}), 201



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
        novo_cracha = requisition_data['badge']
        for employee in data:
            if employee['badge'] == novo_cracha and employee['id'] != id_employee:
                return jsonify({"Erro": "Crachá já existe"}), 400
        employee_encontrado['badge'] = novo_cracha

    if 'name' in requisition_data:
        employee_encontrado['name'] = requisition_data['name']
    if 'job' in requisition_data:
        employee_encontrado['job'] = requisition_data['job']

    return jsonify({'mensagem': 'Dados do colaborador atualizados com sucesso'}), 200
