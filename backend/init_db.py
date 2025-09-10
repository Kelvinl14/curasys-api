import sqlite3
from pathlib import Path
from src.utils.logs import log

BASE_DIR = Path(__file__).resolve().parent

def init_db(db_path: str | None = None):
    """
    Inicializa o banco de dados.
    Se db_path não for informado, usa hospital.db no diretório BASE_DIR.
    """
    db_default = str(BASE_DIR / "hospital.db")
    db_file = db_path or db_default

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Cria a tabela pacientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data_nascimento DATE NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            telefone TEXT,
            email TEXT,
            criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')

    # Cria a tabela medicos
    cursor.execute(
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
    # Cria a tabela cosultas
    ## -obs: status: ex(agendada, realizada e cancelada)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER NOT NULL,
            id_medico INTEGER NOT NULL,
            data_consulta DATETIME NOT NULL,
            status TEXT DEFAULT 'agendada', -- agendada, realizada, cancelada
            criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_paciente) REFERENCES pacientes(id),
            FOREIGN KEY (id_medico) REFERENCES medicos(id)
        )
    """)

    # Cria tabela de exames
    cursor.execute("""
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

    # Cria uma tabela simples para login na plataforma
    ## -obs: role: ex(recepcao, medico, admin e cliente)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'recepcao', -- recepcao, medico, admin, cliente
            criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    log("info",'Banco inicializado com sucesso!')

if __name__ == "__main__":
    init_db()
