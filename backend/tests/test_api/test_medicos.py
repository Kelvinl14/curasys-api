# import requests
# import uuid
#
# BASE_URL = "http://127.0.0.1:5000/medicos"
# ids = []
#
#
# def test_1_post_medicos():
#     medicos = [
#         {"crm": str(uuid.uuid4())[:5], "nome": "Medico A", "especialidade": "Cardiologia", "cpf": str(uuid.uuid4())[:9], "telefone": "234312523", "email": "affa@mail"},
#         {"crm": str(uuid.uuid4())[:5], "nome": "Medico B", "especialidade": "Ortopedia", "cpf": str(uuid.uuid4())[:9], "telefone": "234312523", "email": "affa@mail"},
#         {"crm": str(uuid.uuid4())[:5], "nome": "Medico C", "especialidade": "Dermatologia", "cpf": str(uuid.uuid4())[:9], "telefone": "234312523", "email": "affa@mail"},
#     ]
#
#     for medico in medicos:
#         response = requests.post(BASE_URL, json=medico)
#         assert response.status_code == 201
#
#
# def test_2_get_medicos():
#     response = requests.get(BASE_URL)
#     assert response.status_code == 200
#
#     data = response.json()
#     assert isinstance(data, list)
#
#     for item in data[-3:]:
#         ids.append(item["id"])
#
#     assert len(ids) == 3
#
#
# def test_3_put_medico():
#     medico_id = ids[1]
#     update_data = {"crm": str(uuid.uuid4())[:5], "nome": "Medico B Atualizado", "especialidade": "Neurologia", "cpf": str(uuid.uuid4())[:9], "telefone": "234312523", "email": "affa@mail"}
#
#     response = requests.put(f"{BASE_URL}/{medico_id}", json=update_data)
#     assert response.status_code == 200
#
#
# def test_4_delete_medico():
#     medico_id = ids[2]
#     response = requests.delete(f"{BASE_URL}/{medico_id}")
#     assert response.status_code == 200

import pytest
import sqlite3
from flask import Flask
from werkzeug.security import check_password_hash

# importa o blueprint
from ...src.blueprints.routes.medicos import medico_db
from ...database import get_dbd


@pytest.fixture
def app(tmp_path):
    """
    Cria uma aplicação Flask isolada para rodar os testes
    com um banco de dados SQLite em memória (ou arquivo temporário).
    """
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(medico_db, url_prefix="/medicos")

    # inicializa um banco só para testes
    db_path = tmp_path / "test_m.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # Cria a tabela medicos
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS medicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crm TEXT NOT NULL UNIQUE,
            nome TEXT NOT NULL,
            especialidade TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL,
            criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
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

cpf_medico = str(uuid.uuid4().int)[:11]
cpf_atualizado = str(uuid.uuid4().int)[:11]
crm_medico = "CRM" + str(uuid.uuid4().int)[:5]
crm_atualizado = "CRM" + str(uuid.uuid4().int)[:5]

def test_criar_medico(client):
    resp = client.post("/medicos/", json={
        "crm": crm_medico,
        "nome": "Dra. Ana",
        "especialidade": "Cardiologia",
        "cpf": cpf_medico,
        "telefone": "99999-1111",
        "email": "ana@hospital.com"
    })
    assert resp.status_code == 201
    assert resp.get_json()["status"] == "ok"


def test_listar_medicos(client):
    resp = client.get("/medicos/")
    assert resp.status_code == 200
    medicos = resp.get_json()
    assert isinstance(medicos, list)
    assert len(medicos) > 0


def test_atualizar_medico(client):
    medico_id = client.get("/medicos/").get_json()[0]["id"]

    resp = client.put(f"/medicos/{medico_id}", json={
        "crm": crm_atualizado,
        "nome": "Dra. Ana Atualizada",
        "especialidade": "Clínica Geral",
        "cpf": cpf_atualizado,
        "telefone": "99999-2222",
        "email": "ana@novo.com"
    })
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "atualizado"


def test_deletar_medico(client):
    medico_id = client.get("/medicos/").get_json()[0]["id"]
    resp = client.delete(f"/medicos/{medico_id}")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "deletado"

    resp = client.get(f"/medicos/{medico_id}")
    assert resp.status_code == 404

@pytest.fixture(autouse=True)
def limpar_banco(tmp_path):
    db_path = tmp_path / "test_m.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript("""
        DROP TABLE IF EXISTS consultas;
        DROP TABLE IF EXISTS medicos;
        DROP TABLE IF EXISTS pacientes;
    """)
    conn.commit()
    conn.close()
