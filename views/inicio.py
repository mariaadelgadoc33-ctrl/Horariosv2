import streamlit as st
import pandas as pd

# Importamos la función Y el diccionario
from conexion import get_baserow_data, TABLE_IDS , headers, URL_BASE

st.set_page_config(page_title="Horarios Telemática", layout="wide")
st.title("📅 Control de Horarios - Telemática")




