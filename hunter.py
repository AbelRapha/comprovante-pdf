import streamlit as st
import requests
import mysql.connector
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

HOST = os.getenv("HOST")
USER = os.getenv("USER_DATABASE")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")


# Conectar ao banco de dados MySQL
conn = mysql.connector.connect(
    host=str(HOST),
    user=USER,
    password=str(PASSWORD),
    database=DATABASE
)
cursor = conn.cursor()

# Função para capturar IP do usuário a partir dos headers do Streamlit
def get_user_ip():
    headers = st.context.headers # Obtém os headers
    x_forwarded_for = headers.get("X-Forwarded-For", "")

    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]  # Pega o primeiro IP da lista (IP real do cliente)
        return ip
    return "IP não encontrado"

# Função para buscar detalhes do IP
def get_ip_info(ip):
    response = requests.get(f"https://ipinfo.io/{ip}/json")
    return response.json()

# Função para salvar no banco
def insert_into_db(ip, location_data):
    sql = """
    INSERT INTO dados_ip (ip, cidade, estado, uf)
    VALUES (%s, %s, %s, %s)
    """
    valores = (ip, location_data.get("city"), location_data.get("region"), location_data.get("country"))
    cursor.execute(sql, valores)
    conn.commit()


# # Coleta os dados
user_ip = get_user_ip()  # Obtém o IP diretamente dos headers
if user_ip != "IP não encontrado":
    location_data = get_ip_info(user_ip)  # Busca detalhes da localização
    insert_into_db(user_ip, location_data)  # Salva no banco
    st.success("Comprovante enviado")
else:
    st.warning("Erro ao enviar comprovante")

# Fechar conexão quando o app terminar
cursor.close()
conn.close()

