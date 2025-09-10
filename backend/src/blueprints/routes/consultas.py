from flask import Blueprint, request, jsonify
from ....database import get_dbd

consulta_db = Blueprint("consultas", __name__)

@consulta_db.route("/", methods=["POST"])
def set_cosulta():
    """
    Função usada para criar uma rota do tipo POST para o paciente marcar uma consulta com o medico no sistema

    :return: regitra a consulta do paciente com o medico no banco de dados
    """
    data = request.json
    conn = get_dbd()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO consultas (id_paciente, id_medico, data_consulta, status) VALUES (?, ?, ?, ?)",
        (data["id_paciente"], data["id_medico"], data["data_consulta"], "agendada")
    )
    conn.commit()
    consulta_id = cursor.lastrowid
    return jsonify({"status": "ok", "id": consulta_id}), 201

@consulta_db.route("/", methods=["GET"])
def get_consultas():
    """
    Função usada para criar uma rota do tipo GET para listar as consultas marcadas no sistema

    :return: retorna as consultas do banco de dados
    """
    conn = get_dbd()
    consultas = conn.execute("SELECT * FROM consultas").fetchall()
    return jsonify([dict(c) for c in consultas])

@consulta_db.route("/<int:id>", methods=["GET"])
def get_consulta(id):
    """
    Função usada para criar uma rota do tipo GET para detalhar uma consulta marcada no sistema

    :param id: idetificador da consulta

    :return: retorna a consulta do banco de dados
    """
    conn = get_dbd()
    consultas = conn.execute("SELECT * FROM consultas WHERE id=?", (id,)).fetchone()
    return jsonify(dict(consultas)) if consultas else (jsonify({"error": "Consulta não encotrado"}), 404)

@consulta_db.route("/<int:id>", methods=["PUT"])
def put_consultas(id):
    """
    Função usada para criar uma rota do tipo PUT para atualizar o status ou data da consulta no sistema

    :param id: idetificador da consulta

    :return: faz a atualizacao da consulta no banco de dados
    """
    data = request.json
    conn = get_dbd()

    # Atualizar status
    if "status" in data:
        if data["status"] not in ["agendada", "realizada", "cancelada"]:
            return jsonify({"error": "Status inválido"}), 400
        conn.execute(
            "UPDATE consultas SET status=? WHERE id=?",
            (data["status"], id)
        )

    # Atualizar data
    if "data_consulta" in data:
        conn.execute(
            "UPDATE consultas SET data_consulta=? WHERE id=?",
            (data["data_consulta"], id)
        )

    conn.commit()
    return jsonify({"status": "atualizado"})

@consulta_db.route("/paciente/<int:id_paciente>", methods=["GET"])
def get_consultas_paciente(id_paciente):
    """
    Faz a pequisa de consultas por paciente
    :param id_paciente: indentificador do paciente
    :return: retorna a lista de consultas desse paciente
    """
    conn = get_dbd()
    consultas = conn.execute("SELECT * FROM consultas WHERE id_paciente=?", (id_paciente,)).fetchall()
    return jsonify([dict(c) for c in consultas])

@consulta_db.route("/medico/<int:id_medico>", methods=["GET"])
def get_consultas_medico(id_medico):
    """
    Faz a pequisa de consultas por medico
    :param id_medico: indentificador do medico
    :return: retorna a lista de consultas desse medico
    """
    conn = get_dbd()
    consultas = conn.execute("SELECT * FROM consultas WHERE id_medico=?", (id_medico,)).fetchall()
    return jsonify([dict(c) for c in consultas])

@consulta_db.route("/<int:id>", methods=["DELETE"])
def del_consultas(id: int):
    """
    Função usada para criar uma rota do tipo DELETE para excluir as consultas do sistema

    :param id: idetificador da consulta

    :return: exclui a cosulta do paciente no banco de dados
    """
    conn = get_dbd()
    conn.execute("DELETE FROM consultas WHERE id=?", (id,))
    conn.commit()
    return jsonify({"status": "deletado"})