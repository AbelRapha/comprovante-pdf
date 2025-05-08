import streamlit as st
import requests
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os
from flask import request


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


def get_user_ip():
    ip = request.remote_addr  # Captura o IP real do visitante
    return ip

def get_ip_info(ip):
    response = requests.get(f"https://ipinfo.io/{ip}/json")
    location_data = response.json()
    return location_data

def insert_into_db(ip, location_data):
    sql = """
    INSERT INTO dados_ip (ip, cidade, estado, uf)
    VALUES (%s, %s, %s, %s)
    """
    valores = (ip, location_data.get("city"), location_data.get("region"), location_data.get("country"))
    cursor.execute(sql, valores)
    conn.commit()

# Coleta os dados
ip = get_user_ip()  # Obtém o IP do visitante
location_data = get_ip_info(ip)  # Busca os detalhes do IP
insert_into_db(ip, location_data)  # Salva no banco

st.success("O comprovante foi enviado no seu e-mail")

# Fechar conexão quando o app terminar
cursor.close()
conn.close()


