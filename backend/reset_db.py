import os
from pathlib import Path
from src.utils.logs import log

BASE_DIR = Path(__file__).resolve().parent

def reset_database():
    # Remove o banco se já existir
    path = "hospital.db"
    db_default = str(BASE_DIR / path)

    try:
        if os.path.exists(db_default):
            os.remove(db_default)
            log("warning", f"Banco de dados '{path}' removido.")

        import init_db  # isso vai rodar o script inteiro de criação
        init_db.init_db()
        log("info", "Banco de dados recriado com sucesso.")

    except PermissionError as e:
        log("error", f"Não foi possivel remover o banco de dados, '{path}': {e}")
    except FileNotFoundError:
        log("warning", f"O arquivo '{path}' não existe.")
    except Exception as e:
        # captura qualquer outro erro inesperado
        log("critical", f"Erro inesperado ao tentar excluir '{path}': {e}")



if __name__ == "__main__":
    reset_database()