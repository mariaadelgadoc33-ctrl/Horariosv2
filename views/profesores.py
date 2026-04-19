import streamlit as st
import pandas as pd
# Importamos la función Y el diccionario
from conexion import get_baserow_data, TABLE_IDS , headers, URL_BASE

st.title("🗓️ Profesores")

# Usamos el ID llamando al diccionario por su nombre
datos = get_baserow_data(TABLE_IDS["profesores"]) 

if datos:
        df = pd.DataFrame(datos)
        # Mostrar tabla limpia
        st.dataframe(df, use_container_width=True)
else:
        st.warning("No hay registros en la tabla de profesores.")