import pytest
import sqlite3
from flask import Flask
from CuraSys.backend.src.blueprints.routes.exames import exames_db
from ...database import get_dbd


@pytest.fixture
def app(tmp_path):
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(exames_db, url_prefix="/exames")

    # cria banco temporário
    db_path = tmp_path / "test_e.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # Cria tabela de exames
    conn.execute("""
        CREATE TABLE IF NOT EXISTS exames (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER NOT NULL,
            tipo TEXT NOT NULL, 
            resultado TEXT,
            arquivo_exame TEXT,
            criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_paciente) REFERENCES pacientes(id)
        ) 
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

    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_criar_exame(client):
    resp = client.post("/exames/", json={
        "id_paciente": 1,
        "tipo": "Sangue",
        "resultado": "Normal",
        "arquivo_exame": "exame1.pdf"
    })
    assert resp.status_code == 201
    assert resp.get_json()["status"] == "ok"


def test_listar_exames(client):
    # cria 1 exame
    client.post("/exames/", json={
        "id_paciente": 2,
        "tipo": "Raio-X",
        "resultado": "Fratura",
        "arquivo_exame": "raiox.png"
    })

    resp = client.get("/exames/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert any(e["tipo"] == "Raio-X" for e in data)


def test_detalhar_exame(client):
    client.post("/exames/", json={
        "id_paciente": 3,
        "tipo": "Urina",
        "resultado": "Infecção",
        "arquivo_exame": "urina.jpg"
    })

    resp = client.get("/exames/")
    exame_id = resp.get_json()[-1]["id"]

    resp = client.get(f"/exames/{exame_id}")
    assert resp.status_code == 200
    assert resp.get_json()["tipo"] == "Urina"


def test_atualizar_exame(client):
    client.post("/exames/", json={
        "id_paciente": 4,
        "tipo": "Sangue",
        "resultado": "Anemia",
        "arquivo_exame": "sangue1.pdf"
    })

    resp = client.get("/exames/")
    exame_id = resp.get_json()[-1]["id"]

    resp = client.put(f"/exames/{exame_id}", json={
        "resultado": "Normalizado",
        "arquivo_exame": "sangue2.pdf"
    })
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "atualizado"

    resp = client.get(f"/exames/{exame_id}")
    data = resp.get_json()
    assert data["resultado"] == "Normalizado"
    assert data["arquivo_exame"] == "sangue2.pdf"


def test_deletar_exame(client):
    client.post("/exames/", json={
        "id_paciente": 5,
        "tipo": "Tomografia",
        "resultado": "Lesão",
        "arquivo_exame": "tomo.pdf"
    })

    resp = client.get("/exames/")
    exame_id = resp.get_json()[-1]["id"]

    resp = client.delete(f"/exames/{exame_id}")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "deletado"

    resp = client.get(f"/exames/{exame_id}")
    assert resp.status_code == 404

# import pytest
# import sqlite3
# from flask import Flask
# from werkzeug.security import check_password_hash
#
# # importa o blueprint
# from ...src.blueprints.routes.exames import exames_db
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
#     app.register_blueprint(exames_db, url_prefix="/exames")
#
#     # inicializa um banco só para testes
#     db_path = tmp_path / "test.db"
#     conn = sqlite3.connect(db_path)
#     conn.row_factory = sqlite3.Row
#
#     # Cria tabela de exames
#     conn.execute("""
#         CREATE TABLE IF NOT EXISTS exames (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             id_paciente INTEGER NOT NULL,
#             tipo TEXT NOT NULL,
#             resultado TEXT,
#             arquivo_exame TEXT,
#             criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY (id_paciente) REFERENCES pacientes(id)
#         )
#     """)
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
#
# def test_criar_exame(client):
#     resp = client.post("/exames/", json={
#         "id_paciente": 1,
#         "tipo": "Raio-X",
#         "resultado": "Fratura detectada",
#         "arquivo_exame": "raiox.pdf"
#     })
#     assert resp.status_code == 201
#     assert resp.get_json()["status"] == "ok"
#
#
# def test_listar_exames(client):
#     resp = client.get("/exames/")
#     assert resp.status_code == 200
#     exames = resp.get_json()
#     assert isinstance(exames, list)
#     assert len(exames) > 0
#
#
# def test_deletar_exame(client):
#     exame_id = client.get("/exames/").get_json()[0]["id"]
#     resp = client.delete(f"/exames/{exame_id}")
#     assert resp.status_code == 200
#     assert resp.get_json()["status"] == "deletado"
#
#     resp = client.get(f"/exames/{exame_id}")
#     assert resp.status_code == 404
