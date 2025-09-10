# import os
# import tempfile
# import pytest
# import sqlite3
# from flask import Flask
# from CuraSys.backend.database import get_dbd
# from CuraSys.backend.init_db import init_db
# from CuraSys.backend.src.blueprints.routes.pacientes import paciente_db
# from CuraSys.backend.src.blueprints.routes.medicos import medico_db
# from CuraSys.backend.src.blueprints.routes.consultas import consulta_db
# from CuraSys.backend.src.blueprints.routes.exames import exames_db
# from CuraSys.backend.src.blueprints.routes.usuarios import usuario_db
#
# @pytest.fixture(scope="session")
# def app():
#     # cria um arquivo sqlite temporário
#     db_fd, db_path = tempfile.mkstemp()
#     os.environ["TEST_DB_PATH"] = db_path
#
#     app = Flask(__name__)
#     app.register_blueprint(paciente_db, url_prefix="/pacientes")
#     app.register_blueprint(medico_db, url_prefix="/medicos")
#     app.register_blueprint(consulta_db, url_prefix="/consultas")
#     app.register_blueprint(exames_db, url_prefix="/exames")
#     app.register_blueprint(usuario_db, url_prefix="/usuarios")
#
#     with app.app_context():
#         init_db(db_path)
#
#     yield app
#
#     os.close(db_fd)
#     os.unlink(db_path)
#
#
# @pytest.fixture()
# def client(app):
#     return app.test_client()
