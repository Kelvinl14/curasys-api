from flask import Blueprint, request, jsonify
from ....database import get_dbd

medico_db = Blueprint("medicos", __name__)

@medico_db.route("/", methods=["POST"])
def set_medico():
    """
    Função usada para criar uma rota do tipo POST para cadastro dos medicos no sistema

    :return: faz o cadastro do medico no banco de dados
    """
    data = request.json
    conn = get_dbd()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO medicos (crm, nome, especialidade, cpf, telefone, email) VALUES (?, ?, ?, ?, ?, ?)",
        (data["crm"], data["nome"], data["especialidade"], data["cpf"], data["telefone"], data["email"])
    )
    conn.commit()
    medico_id = cursor.lastrowid
    return jsonify({"status": "ok", "id": medico_id}), 201

@medico_db.route("/", methods=["GET"])
def get_medicos():
    """
    Função usada para criar uma rota do tipo GET para listar os medicos do sistema

    :return: retorna os medicos do banco de dados
    """
    conn = get_dbd()
    medicos = conn.execute("SELECT * FROM medicos").fetchall()
    return jsonify([dict(m) for m in medicos])

@medico_db.route("/<int:id>", methods=["GET"])
def get_medico(id: int):
    """
    Função usada para criar uma rota do tipo GET para listar os medicos do sistema

    :param id: idetificador do medico

    :return: retorna os medicos do banco de dados
    """
    conn = get_dbd()
    medicos = conn.execute("SELECT * FROM medicos WHERE id=?", (id,)).fetchall()
    return jsonify(dict(medicos)) if medicos else (jsonify({"error": "Medico não encotrado"}), 404)

@medico_db.route("/<int:id>", methods=["PUT"])
def put_medicos(id: int):
    """
    Função usada para criar uma rota do tipo PUT para atualizar os medicos do sistema

    :param id: idetificador do medico

    :return: faz a atualizacao do medico no banco de dados
    """
    data = request.json
    conn = get_dbd()
    conn.execute(
        "UPDATE medicos SET crm=?, nome=?, especialidade=?, cpf=?, telefone=?, email=? WHERE id=?",
        (data["crm"], data["nome"], data["especialidade"], data["cpf"], data["telefone"], data["email"], id)
    )
    conn.commit()
    return jsonify({"status": "atualizado"})

@medico_db.route("/<int:id>", methods=["DELETE"])
def del_medicos(id: int):
    """
    Função usada para criar uma rota do tipo DELETE para excluir os medicos do sistema

    :param id: idetificador do medico

    :return: exclui o cadastro do medico no banco de dados
    """
    conn = get_dbd()
    conn.execute("DELETE FROM medicos WHERE id=?", (id,))
    conn.commit()
    return jsonify({"status": "deletado"})