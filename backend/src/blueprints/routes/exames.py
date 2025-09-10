from flask import Blueprint, request, jsonify
from ....database import get_dbd

exames_db = Blueprint("exames", __name__)
table = "exames"

@exames_db.route("/", methods=["POST"])
def set_exames():
    data = request.json
    conn = get_dbd()
    conn.execute(
        f"INSERT INTO {table} (id_paciente, tipo, resultado, arquivo_exame) VALUES (?, ?, ?, ?)",
        (data["id_paciente"], data["tipo"], data["resultado"], data["arquivo_exame"])
    )
    conn.commit()
    return jsonify({"status": "ok"}), 201

@exames_db.route("/", methods=["GET"])
def get_exames():
    conn = get_dbd()
    exames = conn.execute(f"SELECT * FROM {table}").fetchall()
    return jsonify([dict(p) for p in exames])

@exames_db.route("/<int:id>", methods=["GET"])
def get_exame(id: int):
    conn = get_dbd()
    exames = conn.execute(f"SELECT * FROM {table} WHERE id=?", (id,)).fetchone()
    return jsonify(dict(exames)) if exames else (jsonify({"error": "Consulta não encotrado"}), 404)

@exames_db.route("/<int:id>", methods=["PUT"])
def put_exames(id: int):
    data = request.json
    conn = get_dbd()

    if "resultado" in data:
        conn.execute(
            f"UPDATE {table} SET resultado=? WHERE id=?",
            (data["resultado"], id)
        )

    if "arquivo_exame" in data:
        conn.execute(
            f"UPDATE {table} SET arquivo_exame=? WHERE id=?",
            (data["arquivo_exame"], id)
        )

    conn.commit()
    return jsonify({"status": "atualizado"})

@exames_db.route("/<int:id>", methods=["DELETE"])
def del_exames(id: int):
    conn = get_dbd()
    conn.execute(f"DELETE FROM {table} WHERE id=?", (id,))
    conn.commit()
    return jsonify({"status": "deletado"})