from flask import Blueprint, request, jsonify
from ....database import get_dbd

paciente_db = Blueprint("pacientes", __name__)

@paciente_db.route("/", methods=["POST"])
def set_paciente():
    """
    Função usada para criar uma rota do tipo POST para cadastro dos pacientes no sistema

    :return: faz o cadastro do paciente no banco de dados
    """
    data = request.json
    conn = get_dbd()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pacientes (nome, data_nascimento, cpf, telefone, email) VALUES (?, ?, ?, ?, ?)",
        (data["nome"], data["data_nascimento"], data["cpf"], data["telefone"], data["email"])
    )
    conn.commit()
    paciente_id = cursor.lastrowid
    return jsonify({"status": "ok", "id": paciente_id}), 201

@paciente_db.route("/", methods=["GET"])
def get_pacientes():
    """
    Função usada para criar uma rota do tipo GET para listar os pacientes do sistema

    :return: retorna os pacientes do banco de dados
    """
    conn = get_dbd()
    pacientes = conn.execute("SELECT * FROM pacientes").fetchall()
    return jsonify([dict(p) for p in pacientes])

@paciente_db.route("/<int:id>", methods=["GET"])
def get_paciente(id: int):
    """
    Função usada para criar uma rota do tipo GET para detalhar um paciente do sistema

    :param id: idetificador do paciente

    :return: retorna o paciente do banco de dados
    """
    conn = get_dbd()
    paciente = conn.execute("SELECT * FROM pacientes WHERE id=?", (id,)).fetchone()
    return jsonify(dict(paciente)) if paciente else (jsonify({"error": "Paciente não encotrado"}), 404)

@paciente_db.route("/<int:id>", methods=["PUT"])
def put_paciente(id: int):
    """
    Função usada para criar uma rota do tipo PUT para atualizar os pacientes do sistema

    :param id: idetificador do paciente

    :return: faz a atualizacao do paciente no banco de dados
    """
    data = request.json
    conn = get_dbd()
    conn.execute(
        "UPDATE pacientes SET nome=?, data_nascimento=?, cpf=?, telefone=?, email=? WHERE id=?",
        (data["nome"], data["data_nascimento"], data["cpf"], data["telefone"], data["email"], id)
    )
    conn.commit()
    return jsonify({"status": "atualizado"})


@paciente_db.route("/<int:id>", methods=["DELETE"])
def del_paciente(id: int):
    """
    Função usada para criar uma rota do tipo DELETE para excluir os pacientes do sistema

    :param id: idetificador do paciente

    :return: exclui o cadastro do paciente no banco de dados
    """
    conn = get_dbd()
    conn.execute("DELETE FROM pacientes WHERE id=?", (id,))
    conn.commit()
    return jsonify({"status": "deletado"})