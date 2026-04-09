import os

from dotenv import load_dotenv

# LOAD ENV
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
GATEWAY_URL = os.getenv("GATEWAY_URL")

if not all([SECRET_KEY, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD]):
    raise RuntimeError("Variáveis de ambiente obrigatórias não configuradas.")

