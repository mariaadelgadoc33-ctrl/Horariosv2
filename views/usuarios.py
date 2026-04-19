import streamlit as st
import pandas as pd
import requests
# Importamos la función Y el diccionario
from conexion import get_baserow_data, TABLE_IDS , headers, URL_BASE

st.subheader("👥 Gestión de Usuarios del Sistema")

    # --- FORMULARIO PARA AGREGAR USUARIO ---
with st.expander("➕ Registrar Nuevo Usuario"):
        with st.form("nuevo_usuario"):
            
            cedula = st.text_input("Cedula")
            #nueva_clave = st.text_input("Contraseña", type="password")
            nuevo_rol = st.selectbox("Rol", ["Administrador", "Profesor", "Estudiante"])
            
            boton_enviar = st.form_submit_button("Guardar Usuario")

            if boton_enviar:
                if cedula:
                    # Datos en el formato que Baserow espera
                    payload = {
                        
                        "Cedula": cedula,
                        #"Password": nueva_clave,
                        "Rol": nuevo_rol
                    }
                    
                    # URL para enviar (POST)
                    url_post = f"{URL_BASE}/{TABLE_IDS['estudiante']}/?user_field_names=true"
                    res = requests.post(url_post, headers=headers, json=payload)
                    
                    if res.status_code == 200 or res.status_code == 201:
                        st.success("✅ Usuario creado exitosamente")
                        st.rerun()
                    else:
                        st.error(f"Error al guardar: {res.text}")
                else:
                    st.warning("Por favor rellena todos los campos")

    # --- TABLA DE USUARIOS EXISTENTES ---
st.write("---")
st.write("### Usuarios Registrados")
usuarios_lista = get_baserow_data(TABLE_IDS["estudiante"])
    
if usuarios_lista:
        df_usuarios = pd.DataFrame(usuarios_lista)
        # Mostramos solo columnas importantes para seguridad
        columnas_ver = [col for col in ['id', 'cedula', 'Rol'] if col in df_usuarios.columns]
        st.dataframe(df_usuarios[columnas_ver], use_container_width=True)
else:
        st.warning("No hay usuarios registrados aún.")