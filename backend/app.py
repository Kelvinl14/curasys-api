from flask import Flask
from flask_cors import CORS
from .src.blueprints.routes.pacientes import paciente_db
from .src.blueprints.routes.consultas import consulta_db
from .src.blueprints.routes.usuarios import usuario_db
from .src.blueprints.routes.medicos import medico_db
from .src.blueprints.routes.exames import exames_db
from .src.blueprints.routes.auth import auth_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # registro dos blueprints
    app.register_blueprint(paciente_db, url_prefix="/pacientes")
    app.register_blueprint(consulta_db, url_prefix="/consultas")
    app.register_blueprint(usuario_db, url_prefix="/usuarios")
    app.register_blueprint(medico_db, url_prefix="/medicos")
    app.register_blueprint(exames_db, url_prefix="/exames")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)