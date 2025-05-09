from flask import Blueprint, jsonify, request

bp_employee = Blueprint('colaborador', __name__, url_prefix='/colaborador')

data = [
    {'id': 1, 'name': 'Samuel Silvério', 'job': 'Desenvolvedor Back-end', 'badge': 'BE12310'},
    {'id': 2, 'name': 'Karynne Moreira', 'job': 'Desenvolvedora Front-end', 'badge': 'FE21310'},
    {'id': 3, 'name': 'Joy Assis', 'job': 'Desenvolvedora Fullstack', 'badge': 'FS12110'},
]

@bp_employee.route('/pegar-dados')
def get_data():
    
    return jsonify(data)


@bp_employee.route('/criar', methods=["POST"])
def create_employee():
    requisition_data = request.get_json()

    if not requisition_data:
        return jsonify({"Erro": "Insira todos os dados"}), 400

    # Verifica se já existe um crachá igual
    for employee in data:
        if employee['badge'] == requisition_data.get('badge'):
            return jsonify({"Erro": "Crachá já existe"}), 400

    new_employee = {
        'id': len(data) + 1,
        'name': requisition_data['name'],
        'job': requisition_data['job'],
        'badge': requisition_data['badge'],
    }

    data.append(new_employee)
    return jsonify({"message": "employee criado com sucesso"}), 201



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
