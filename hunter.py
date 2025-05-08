import streamlit as st
import requests
import mysql.connector
from dotenv import load_dotenv
import os

# # Carregar variáveis do arquivo .env
# load_dotenv()

# HOST = os.getenv("HOST")
# USER = os.getenv("USER_DATABASE")
# PASSWORD = os.getenv("PASSWORD")
# DATABASE = os.getenv("DATABASE")


# # Conectar ao banco de dados MySQL
# conn = mysql.connector.connect(
#     host=str(HOST),
#     user=USER,
#     password=str(PASSWORD),
#     database=DATABASE
# )
# cursor = conn.cursor()

# # Função para capturar IP real do visitante via API
# def get_user_ip():
#     try:
#         response = requests.get("https://api64.ipify.org?format=json")
#         return response.json()["ip"]
#     except Exception as e:
#         return f"Erro ao obter IP: {e}"

# # Função para buscar detalhes do IP
# def get_ip_info(ip):
#     response = requests.get(f"https://ipinfo.io/{ip}/json")
#     return response.json()

# # Função para salvar no banco
# def insert_into_db(ip, location_data):
#     sql = """
#     INSERT INTO dados_ip (ip, cidade, estado, uf)
#     VALUES (%s, %s, %s, %s)
#     """
#     valores = (ip, location_data.get("city"), location_data.get("region"), location_data.get("country"))
#     cursor.execute(sql, valores)
#     conn.commit()

# # Coleta os dados
# if st.button("Enviar comprovante"):
#     user_ip = get_user_ip()  # Obtém o IP automaticamente
#     location_data = get_ip_info(user_ip)  # Busca detalhes da localização
#     insert_into_db(user_ip, location_data)  # Salva no banco
#     st.success("Comprovante enviado")


# # Fechar conexão quando o app terminar
# cursor.close()
# conn.close()

from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx


def get_remote_ip() -> str:
    """Get remote ip."""

    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None

        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except Exception as e:
        return None

    return session_info.request.remote_ip


import streamlit as st

st.title("Title")
st.markdown(f"The remote ip is {get_remote_ip()}")
