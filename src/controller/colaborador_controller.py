from flask import Blueprint, jsonify, request
from src.security.security import check_password, hash_password
from src.model.colaborador_model import Employee
from src.model import db
from flasgger import swag_from
from sqlalchemy.exc import IntegrityError


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




@bp_employee.route('/atualizar/<int:id>', methods=['PUT'])
@swag_from("../docs/colaborador/atualizar_colaborador.yml")
def update_employee_data(id):
    requisition_data = request.get_json()

    if not requisition_data:
        return jsonify({"erro": "Dados da requisição estão vazios"}), 400

    employee = Employee.query.get(id)

    if not employee:
        return jsonify({"mensagem": "Usuário não encontrado"}), 404

    # if 'badge' in requisition_data:
    #     novo_badge = requisition_data['badge']
    #     badge_exists = Employee.query.filter(Employee.badge == novo_badge, Employee.id != id).first()
    #     if badge_exists:
    #         return jsonify({"erro": "Crachá já existe"}), 400
    #     employee.badge = novo_badge

    if 'name' in requisition_data:
        employee.name = requisition_data['name']
    if 'job' in requisition_data:
        employee.job = requisition_data['job']
    if 'email' in requisition_data:
        employee.email = requisition_data['email']
    if 'salary' in requisition_data:
        employee.salary = requisition_data['salary']
    if 'password' in requisition_data:
        employee.password = hash_password(requisition_data['password'])

    db.session.commit()
    return jsonify({'mensagem': f"Colaborador número {id} atualizado com sucesos"}), 200
 
    


@bp_employee.route('/apagar/<int:id>', methods=['DELETE'])
def erase_employee(id):
    try:
        employee = Employee.query.get(id)

        if not employee:
            return jsonify({"mensagem": "Usuário não encontrado"}), 404

        db.session.delete(employee)
        db.session.commit()
        return jsonify({'mensagem': 'Deletado com Sucesso'}), 200

    except IntegrityError as e:
        db.session.rollback()
        if "foreign key constraint fails" in str(e.orig):
            return jsonify({
                'erro': 'Não é possível deletar esse funcionário. Existem registros relacionados a ele.'
            }), 409
        return jsonify({'erro': str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500
