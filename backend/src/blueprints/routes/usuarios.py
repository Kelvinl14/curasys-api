from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ....database import get_dbd  # ajuste o caminho conforme sua estrutura

usuario_db = Blueprint("usuarios", __name__)

@usuario_db.route("/", methods=["POST"])
def set_usuario():
    """
    Cria um novo usuário no sistema.
    - senha é automaticamente convertida para hash antes de salvar
    """
    data = request.json
    conn = get_dbd()

    senha_hash = generate_password_hash(data["senha"])

    try:
        conn.execute(
            "INSERT INTO usuarios (username, senha_hash, role) VALUES (?, ?, ?)",
            (data["username"], senha_hash, data.get("role", "recepcao"))
        )
        conn.commit()
        return jsonify({"status": "ok"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@usuario_db.route("/", methods=["GET"])
def get_usuarios():
    """
    Lista todos os usuários cadastrados no sistema.
    """
    conn = get_dbd()
    usuarios = conn.execute(
        "SELECT id, username, role, criado_em FROM usuarios"
    ).fetchall()
    return jsonify([dict(u) for u in usuarios])


@usuario_db.route("/<int:id>", methods=["GET"])
def get_usuario(id: int):
    """
    Retorna os detalhes de um usuário específico.
    """
    conn = get_dbd()
    usuario = conn.execute(
        "SELECT id, username, role, criado_em FROM usuarios WHERE id=?",
        (id,)
    ).fetchone()

    return jsonify(dict(usuario)) if usuario else (jsonify({"error": "Usuário não encontrado"}), 404)


@usuario_db.route("/<int:id>", methods=["PUT"])
def put_usuario(id: int):
    """
    Atualiza os dados de um usuário existente.
    - Se senha for enviada, será atualizada com hash
    """
    data = request.json
    conn = get_dbd()

    if "senha" in data:
        senha_hash = generate_password_hash(data["senha"])
        conn.execute(
            "UPDATE usuarios SET username=?, senha_hash=?, role=? WHERE id=?",
            (data["username"], senha_hash, data.get("role", "recepcao"), id)
        )
    else:
        conn.execute(
            "UPDATE usuarios SET username=?, role=? WHERE id=?",
            (data["username"], data.get("role", "recepcao"), id)
        )

    conn.commit()
    return jsonify({"status": "atualizado"})


@usuario_db.route("/<int:id>", methods=["DELETE"])
def del_usuario(id: int):
    """
    Exclui um usuário do sistema.
    """
    conn = get_dbd()
    conn.execute("DELETE FROM usuarios WHERE id=?", (id,))
    conn.commit()
    return jsonify({"status": "deletado"})


@usuario_db.route("/login", methods=["POST"])
def login_usuario():
    """
    Rota para autenticar o usuário (login).
    - Verifica username e senha
    """
    data = request.json
    conn = get_dbd()

    usuario = conn.execute(
        "SELECT * FROM usuarios WHERE username=?",
        (data["username"],)
    ).fetchone()

    if usuario and check_password_hash(usuario["senha_hash"], data["senha"]):
        return jsonify({
            "status": "autenticado",
            "id": usuario["id"],
            "username": usuario["username"],
            "role": usuario["role"]
        }), 200

    return jsonify({"error": "Credenciais inválidas"}), 401
