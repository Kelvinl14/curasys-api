from flask import Blueprint, request, jsonify
import jwt
import datetime
import os
from functools import wraps

auth_bp = Blueprint("auth", __name__)

# Chave secreta para assinar os tokens
SECRET_KEY = os.getenv("SECRET_KEY", "minha_chave_secreta")

# API Keys válidas (em produção pode vir do banco)
API_KEYS = {"1234567890abcdef", "chave_teste_001"}


# ---------------------------
# Funções auxiliares
# ---------------------------

def token_required(f):
    """Decorator para validar JWT"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token é necessário"}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            return jsonify({"message": f"Token inválido: {str(e)}"}), 401
        return f(*args, **kwargs)
    return decorated


def api_key_required(f):
    """Decorator para validar API Key"""
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("x-api-key")
        if not api_key or api_key not in API_KEYS:
            return jsonify({"message": "API Key inválida"}), 401
        return f(*args, **kwargs)
    return decorated


# ---------------------------
# Rotas
# ---------------------------

@auth_bp.route("/login", methods=["POST"])
def login():
    """Autenticação básica com usuário e senha"""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Exemplo fixo, mas pode vir do banco
    if username == "admin" and password == "123456":
        token = jwt.encode({
            "user": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token})

    return jsonify({"message": "Credenciais inválidas"}), 401


@auth_bp.route("/secure-jwt", methods=["GET"])
@token_required
def secure_jwt():
    """Exemplo de rota protegida por JWT"""
    return jsonify({"message": "Acesso permitido com JWT"})


@auth_bp.route("/secure-apikey", methods=["GET"])
@api_key_required
def secure_apikey():
    """Exemplo de rota protegida por API Key"""
    return jsonify({"message": "Acesso permitido com API Key"})
