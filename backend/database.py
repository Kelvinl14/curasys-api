import sqlite3
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
# Caminhos fixos
MAIN_DB_PATH = BASE_DIR / "hospital.db"

def get_dbd():
    db_path = str(MAIN_DB_PATH)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
