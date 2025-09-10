from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "1234":
        return jsonify({"token": "fake-jwt-token"})
    return jsonify({"error": "Credenciais inválidas"}), 401
