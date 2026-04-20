import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# ================= CONFIG =================
st.set_page_config(page_title="Formulario Clientes")

st.title("📋 Registro de Clientes")

# ================= CREDENCIALES =================
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope
)

client = gspread.authorize(creds)

# Abre tu hoja
SHEET_NAME = "Registro Clientes"
sheet = client.open(SHEET_NAME).sheet1

# ================= FORMULARIO =================
with st.form("formulario"):

    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    celular = st.text_input("Celular")
    direccion = st.text_input("Dirección")

    submit = st.form_submit_button("Guardar")

    if submit:
        if nombre and apellido:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            sheet.append_row([
                nombre,
                apellido,
                celular,
                direccion,
                fecha
            ])

            st.success("✅ Datos guardados correctamente")
        else:
            st.warning("⚠️ Completa los campos obligatorios")
