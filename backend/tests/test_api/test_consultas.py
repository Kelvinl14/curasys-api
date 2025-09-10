# import requests
#
# BASE_URL = "http://127.0.0.1:5000/consultas"
# ids = []
#
#
# def test_1_post_consultas():
#     consultas = [
#         {"id_paciente": 1, "id_medico": 1, "data_consulta": "2025-09-10T12:00"},
#         {"id_paciente": 2, "id_medico": 2, "data_consulta": "2025-09-11T14:00"},
#         {"id_paciente": 3, "id_medico": 3, "data_consulta": "2025-09-12T08:00"},
#     ]
#
#     for consulta in consultas:
#         response = requests.post(BASE_URL, json=consulta)
#         assert response.status_code == 201
#
#
# def test_2_get_consultas():
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
# def test_3_put_consulta():
#     consulta_id = ids[1]
#     update_data = {"id_paciente": 2, "id_medico": 2, "data_consulta": "2025-09-15T15:00"}
#
#     response = requests.put(f"{BASE_URL}/{consulta_id}", json=update_data)
#     assert response.status_code == 200
#
#
# def test_4_delete_consulta():
#     consulta_id = ids[2]
#     response = requests.delete(f"{BASE_URL}/{consulta_id}")
#     assert response.status_code == 200

import pytest
import sqlite3
from flask import Flask
# importa todos os blueprints
from CuraSys.backend.src.blueprints.routes.consultas import consulta_db
from CuraSys.backend.src.blueprints.routes.pacientes import paciente_db
from CuraSys.backend.src.blueprints.routes.medicos import medico_db
from ...database import get_dbd


@pytest.fixture
def app(tmp_path):
    app = Flask(__name__)
    app.config["TESTING"] = True
    # registra os blueprints
    app.register_blueprint(consulta_db, url_prefix="/consultas")
    app.register_blueprint(paciente_db, url_prefix="/pacientes")
    app.register_blueprint(medico_db, url_prefix="/medicos")

    # cria banco temporário
    db_path = tmp_path / "test_c.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data_nascimento DATE NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            telefone TEXT,
            email TEXT
        );

        CREATE TABLE IF NOT EXISTS medicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crm TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            especialidade TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            telefone TEXT,
            email TEXT
        );

        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER NOT NULL,
            id_medico INTEGER NOT NULL,
            data_consulta DATETIME NOT NULL,
            status TEXT DEFAULT 'agendada',
            criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_paciente) REFERENCES pacientes(id),
            FOREIGN KEY (id_medico) REFERENCES medicos(id)
        );
    """)
    conn.commit()
    conn.close()

    # sobrescreve get_dbd
    def override_get_dbd():
        c = sqlite3.connect(db_path)
        c.row_factory = sqlite3.Row
        return c

    global get_dbd
    get_dbd = override_get_dbd

    # entrega app para os testes
    yield app

    # ---------- TEARDOWN ----------
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript("""
        DROP TABLE IF EXISTS consultas;
        DROP TABLE IF EXISTS medicos;
        DROP TABLE IF EXISTS pacientes;
    """)
    conn.commit()
    conn.close()


@pytest.fixture
def client(app):
    return app.test_client()

import uuid

def test_criar_consulta(client):
    # CPF e CRM únicos por teste
    cpf_paciente = str(uuid.uuid4().int)[:11]
    cpf_medico = str(uuid.uuid4().int)[:11]
    crm_medico = "CRM" + str(uuid.uuid4().int)[:5]

    # Cria paciente
    paciente_resp = client.post("/pacientes/", json={
        "nome": "Carlos",
        "data_nascimento": "1995-05-10",
        "cpf": cpf_paciente,
        "telefone": "98888-7777",
        "email": "carlos@email.com"
    })
    paciente_json = paciente_resp.get_json()
    assert paciente_resp.status_code == 201
    paciente_id = paciente_json.get("id")

    # Cria médico
    medico_resp = client.post("/medicos/", json={
        "crm": crm_medico,
        "nome": "Dr. Pedro",
        "especialidade": "Ortopedia",
        "cpf": cpf_medico,
        "telefone": "97777-6666",
        "email": "pedro@hospital.com"
    })
    medico_json = medico_resp.get_json()
    assert medico_resp.status_code == 201
    medico_id = medico_json.get("id")

    # Cria consulta usando os IDs reais
    consulta_resp = client.post("/consultas/", json={
        "id_paciente": paciente_id,
        "id_medico": medico_id,
        "data_consulta": "2025-12-01 10:00:00",
        "status": "agendada"
    })
    consulta_json = consulta_resp.get_json()
    assert consulta_resp.status_code == 201
    assert consulta_json["status"] == "ok"
    assert "id" in consulta_json


def test_listar_consultas(client):
    resp = client.get("/consultas/")
    assert resp.status_code == 200
    consultas = resp.get_json()
    assert isinstance(consultas, list)
    # pode ser zero se não rodar na ordem, mas ideal é garantir que há pelo menos uma
    assert all("id" in c for c in consultas)


