import requests
import uuid

BASE_URL = "http://127.0.0.1:5000/pacientes"
ids = []  # lista para armazenar IDs criados


def test_1_post_pacientes():
    pacientes = [
        {"nome": "Paciente A", "data_nascimento": "1995-10-02", "cpf": str(uuid.uuid4())[:9], "telefone": "(85) 9999-9999",
         "email": "affa@mail"},
        {"nome": "Paciente B", "data_nascimento": "1995-10-02", "cpf": str(uuid.uuid4())[:9], "telefone": "(85) 9999-9998",
         "email": "bffa@mail"},
        {"nome": "Paciente C", "data_nascimento": "1995-10-02", "cpf": str(uuid.uuid4())[:9], "telefone": "(85) 9999-9997",
         "email": "cffa@mail"},
    ]

    for paciente in pacientes:
        response = requests.post(BASE_URL, json=paciente)
        assert response.status_code == 201


def test_2_get_pacientes():
    response = requests.get(BASE_URL)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    # salvar os 3 primeiros IDs criados
    for item in data[-3:]:
        ids.append(item["id"])

    assert len(ids) == 3


def test_3_put_paciente():
    paciente_id = ids[1]  # segundo registro
    update_data = {"nome": "Paciente B Atualizado", "data_nascimento": "1995-10-02", "cpf": str(uuid.uuid4())[:9], "telefone": "(85) 9999-9997", "email": "affa@mail"}

    response = requests.put(f"{BASE_URL}/{paciente_id}", json=update_data)
    assert response.status_code == 200


def test_4_delete_paciente():
    paciente_id = ids[2]  # terceiro registro
    response = requests.delete(f"{BASE_URL}/{paciente_id}")
    assert response.status_code == 200

# import pytest
# import sqlite3
# from flask import Flask
#
# # importa o blueprint
# from ...src.blueprints.routes.pacientes import paciente_db
# from ...database import get_dbd
#
#
# @pytest.fixture
# def app(tmp_path):
#     """
#     Cria uma aplicação Flask isolada para rodar os testes
#     com um banco de dados SQLite em memória (ou arquivo temporário).
#     """
#     app = Flask(__name__)
#     app.config["TESTING"] = True
#     app.register_blueprint(paciente_db, url_prefix="/pacientes")
#
#     # inicializa um banco só para testes
#     db_path = tmp_path / "test_p.db"
#     conn = sqlite3.connect(db_path)
#     conn.row_factory = sqlite3.Row
#
#     # Cria a tabela pacientes
#     conn.execute(
#         '''
#         CREATE TABLE IF NOT EXISTS pacientes (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             nome TEXT NOT NULL,
#             data_nascimento DATE NOT NULL,
#             cpf TEXT NOT NULL UNIQUE,
#             telefone TEXT,
#             email TEXT,
#             criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
#         )
#         '''
#     )
#     conn.commit()
#     conn.close()
#
#     # sobrescreve get_dbd para sempre conectar no db de teste
#     def override_get_dbd():
#         c = sqlite3.connect(db_path)
#         c.row_factory = sqlite3.Row
#         return c
#
#     global get_dbd
#     get_dbd = override_get_dbd
#
#     return app
#
#
# @pytest.fixture
# def client(app):
#     return app.test_client()
#
# import uuid
#
# cpf_paciente = str(uuid.uuid4().int)[:11]
# cpf_atualizado = str(uuid.uuid4().int)[:11]
#
# def test_criar_paciente(client):
#     resp = client.post("/pacientes/", json={
#         "nome": "João da Silva",
#         "data_nascimento": "1990-01-01",
#         "cpf": cpf_paciente,
#         "telefone": "99999-9999",
#         "email": "joao@email.com"
#     })
#     assert resp.status_code == 201
#     assert resp.get_json()["status"] == "ok"
#
#
# def test_listar_pacientes(client):
#     resp = client.get("/pacientes/")
#     assert resp.status_code == 200
#     pacientes = resp.get_json()
#     assert isinstance(pacientes, list)
#     assert len(pacientes) > 0
#
#
# def test_atualizar_paciente(client):
#     paciente_id = client.get("/pacientes/").get_json()[0]["id"]
#
#     resp = client.put(f"/pacientes/{paciente_id}", json={
#         "nome": "João Atualizado",
#         "data_nascimento": "1990-01-01",
#         "cpf": cpf_atualizado,
#         "telefone": "88888-8888",
#         "email": "joao_new@email.com"
#     })
#     assert resp.status_code == 200
#     assert resp.get_json()["status"] == "atualizado"
#
#
# def test_deletar_paciente(client):
#     paciente_id = client.get("/pacientes/").get_json()[0]["id"]
#     resp = client.delete(f"/pacientes/{paciente_id}")
#     assert resp.status_code == 200
#     assert resp.get_json()["status"] == "deletado"
#
#     # garantir que foi removido
#     resp = client.get(f"/pacientes/{paciente_id}")
#     assert resp.status_code == 404
#
# @pytest.fixture(autouse=True)
# def limpar_banco(tmp_path):
#     db_path = tmp_path / "test_m.db"
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     cursor.executescript("""
#         DROP TABLE IF EXISTS consultas;
#         DROP TABLE IF EXISTS medicos;
#         DROP TABLE IF EXISTS pacientes;
#     """)
#     conn.commit()
#     conn.close()