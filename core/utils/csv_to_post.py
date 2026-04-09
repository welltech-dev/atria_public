import os
import csv
import psycopg2
from dotenv import load_dotenv

# CONFIGURAÇÃO DO CAMINHO DO .ENV

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# sobe duas pastas até a raiz do projeto (~/a_1)
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../"))

ENV_PATH = os.path.join(ROOT_DIR, ".env")

if not os.path.exists(ENV_PATH):
    raise FileNotFoundError(f".env não encontrado em: {ENV_PATH}")

load_dotenv(ENV_PATH)

# VALIDAÇÃO DAS VARIÁVEIS

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT", 5432)

missing = [var for var in ["DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD"] if not os.getenv(var)]

if missing:
    raise EnvironmentError(f"Variáveis ausentes no .env: {missing}")

# CONEXÃO

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

# MIGRAÇÃO CSV → POSTGRESQL

CSV_PATH = os.path.join(ROOT_DIR, "users.csv")

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"Arquivo users.csv não encontrado em: {CSV_PATH}")

conn = get_connection()
cur = conn.cursor()

with open(CSV_PATH, newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        cur.execute("""
            INSERT INTO users (username, email, password)
            VALUES (%s, %s, %s)
            ON CONFLICT (email) DO NOTHING;
        """, (
            row["username"],
            row["email"],
            row["password"]
        ))

conn.commit()
cur.close()
conn.close()

print("Migração concluída com sucesso 🚀")
