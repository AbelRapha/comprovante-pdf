import streamlit as st
import requests
import pandas as pd
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



def get_ip_info():
    response = requests.get("https://api64.ipify.org?format=json")
    ip = response.json()["ip"]
    
    response = requests.get(f"https://ipinfo.io/{ip}/json")
    location_data = response.json()

    return ip, location_data


def insert_into_db(ip, location_data):
    sql = """
    INSERT INTO dados_ip (ip, cidade, estado, uf)
    VALUES (%s, %s, %s, %s)
    """
    valores = (ip, location_data.get("city"), location_data.get("region"), location_data.get("country"))

    cursor.execute(sql, valores)
    conn.commit()


# Coleta os dados
ip, location_data = get_ip_info()
insert_into_db(ip, location_data)
st.success("O comprovante foi enviado no seu e-mail")

# Fechar conexão quando o app terminar
cursor.close()
conn.close()


