import streamlit as st
import pandas as pd

# Importamos la función Y el diccionario
from conexion import get_baserow_data, TABLE_IDS , headers, URL_BASE


st.subheader("🎓 Lista de Estudiantes")
estudiantes = get_baserow_data(TABLE_IDS["estudiante"])
if estudiantes:
        st.dataframe(pd.DataFrame(estudiantes), use_container_width=True)
else:
        st.warning("No hay registros en la tabla de Estudiantes.")


        
