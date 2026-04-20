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
#SHEET_NAME = "Registro Clientes"
#sheet = client.open(SHEET_NAME).sheet1

from googleapiclient.discovery import build
import gspread.exceptions

SHEET_NAME = "Registro Clientes"
FOLDER_ID = "1XYWclBVOhuFxWS6d9pa8N3PbIz6aiJ45"

# Cliente Drive
drive_service = build('drive', 'v3', credentials=creds)

try:
    # 🔍 Buscar archivo dentro de la carpeta
    files = drive_service.files().list(
        q=f"name='{SHEET_NAME}' and '{FOLDER_ID}' in parents and trashed=false",
        fields="files(id, name)"
    ).execute().get('files', [])

    if files:
        # ✅ Si existe, abrirlo
        spreadsheet = client.open_by_key(files[0]['id'])
    else:
        # 🚀 Si no existe, crearlo
        spreadsheet = client.create(SHEET_NAME)

        # 🔥 Moverlo a la carpeta
        drive_service.files().update(
            fileId=spreadsheet.id,
            addParents=FOLDER_ID,
            removeParents='root',
            fields='id, parents'
        ).execute()

except Exception as e:
    st.error(f"Error: {e}")

# Seleccionar hoja
sheet = spreadsheet.sheet1

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
