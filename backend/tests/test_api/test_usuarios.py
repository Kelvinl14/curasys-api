import pytest
import sqlite3
from flask import Flask
from werkzeug.security import check_password_hash

# importa o blueprint
from ...src.blueprints.routes.usuarios import usuario_db
from ...database import get_dbd


@pytest.fixture
def app(tmp_path):
    """
    Cria uma aplicação Flask isolada para rodar os testes
    com um banco de dados SQLite em memória (ou arquivo temporário).
    """
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(usuario_db, url_prefix="/usuarios")

    # inicializa um banco só para testes
    db_path = tmp_path / "test_u.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # cria tabela de usuarios
    conn.execute("""
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'recepcao',
            criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

    # sobrescreve get_dbd para sempre conectar no db de teste
    def override_get_dbd():
        c = sqlite3.connect(db_path)
        c.row_factory = sqlite3.Row
        return c

    global get_dbd
    get_dbd = override_get_dbd

    return app


@pytest.fixture
def client(app):
    return app.test_client()



import uuid

def gerar_username(prefix="teste"):
    return f"{prefix}_{uuid.uuid4().hex[:6]}"

def test_criar_usuario(client):
    username = gerar_username()
    resp = client.post("/usuarios/", json={
        "username": username,
        "senha": "123456",
        "role": "admin"
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["status"] == "ok"


def test_listar_usuarios(client):
    username = gerar_username()
    client.post("/usuarios/", json={
        "username": username,
        "senha": "abc123",
        "role": "medico"
    })

    resp = client.get("/usuarios/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert any(u["username"] == username for u in data)


def test_detalhar_usuario(client):
    username = gerar_username()
    client.post("/usuarios/", json={
        "username": username,
        "senha": "xyz123",
        "role": "recepcao"
    })

    resp = client.get("/usuarios/")
    uid = resp.get_json()[-1]["id"]

    resp = client.get(f"/usuarios/{uid}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["username"] == username


def test_atualizar_usuario(client):
    username = gerar_username()
    client.post("/usuarios/", json={
        "username": username,
        "senha": "senha1",
        "role": "recepcao"
    })

    resp = client.get("/usuarios/")
    uid = resp.get_json()[-1]["id"]

    novo_username = gerar_username()
    resp = client.put(f"/usuarios/{uid}", json={
        "username": novo_username,
        "senha": "novaSenha",
        "role": "admin"
    })
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "atualizado"

    resp = client.get(f"/usuarios/{uid}")
    data = resp.get_json()
    assert data["username"] == novo_username
    assert data["role"] == "admin"


def test_login_usuario(client):
    username = gerar_username()
    client.post("/usuarios/", json={
        "username": username,
        "senha": "segredo",
        "role": "medico"
    })

    resp = client.post("/usuarios/login", json={
        "username": username,
        "senha": "segredo"
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "autenticado"
    assert data["role"] == "medico"

    resp = client.post("/usuarios/login", json={
        "username": username,
        "senha": "errado"
    })
    assert resp.status_code == 401


def test_deletar_usuario(client):
    username = gerar_username()
    client.post("/usuarios/", json={
        "username": username,
        "senha": "delete",
        "role": "recepcao"
    })

    resp = client.get("/usuarios/")
    uid = resp.get_json()[-1]["id"]

    resp = client.delete(f"/usuarios/{uid}")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "deletado"

    resp = client.get(f"/usuarios/{uid}")
    assert resp.status_code == 404
