import streamlit as st
import requests
import pandas as pd
from conexion import get_baserow_data, TABLE_IDS , headers, URL_BASE

# --- INTERFAZ ---
st.set_page_config(page_title="Horarios Telemática", layout="wide")
st.title("📅 Control de Horarios - Telemática")

menu = ["Inicio", "Ver Horarios", "Gestión Estudiantes", "Profesores","Usuarios"]
choice = st.sidebar.selectbox("Menú", menu)

if choice == "Inicio":
    st.subheader("Panel de Control")
    st.info("Bienvenido al sistema. Usa el menú lateral para navegar.")

elif choice == "Ver Horarios":
    st.subheader("🗓️ Horario de Clases")
    datos = get_baserow_data(TABLE_IDS["Horarios"])
    if datos:
        df = pd.DataFrame(datos)
        # Mostrar tabla limpia
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No hay registros en la tabla de Horarios.")

elif choice == "Gestión Estudiantes":
    st.subheader("🎓 Lista de Estudiantes")
    estudiantes = get_baserow_data(TABLE_IDS["estudiante"])
    if estudiantes:
        st.dataframe(pd.DataFrame(estudiantes), use_container_width=True)

elif choice == "Profesores":
    st.subheader("👨‍🏫 Plantel Docente")
    profes = get_baserow_data(TABLE_IDS["profesores"])
    if profes:
        st.table(pd.DataFrame(profes))
elif choice == "Usuarios":
    st.subheader("👥 Gestión de Usuarios del Sistema")

    # --- FORMULARIO PARA AGREGAR USUARIO ---
    with st.expander("➕ Registrar Nuevo Usuario"):
        with st.form("nuevo_usuario"):
            nuevo_nombre = st.text_input("Nombre Completo")
            nuevo_user = st.text_input("Nombre de Usuario")
            nueva_clave = st.text_input("Contraseña", type="password")
            nuevo_rol = st.selectbox("Rol", ["Administrador", "Profesor", "Estudiante"])
            
            boton_enviar = st.form_submit_button("Guardar Usuario")

            if boton_enviar:
                if nuevo_nombre and nuevo_user and nueva_clave:
                    # Datos en el formato que Baserow espera
                    payload = {
                        "Nombre": nuevo_nombre,
                        "Username": nuevo_user,
                        "Password": nueva_clave,
                        "Rol": nuevo_rol
                    }
                    
                    # URL para enviar (POST)
                    url_post = f"{URL_BASE}/{TABLE_IDS['usuario']}/?user_field_names=true"
                    res = requests.post(url_post, headers=headers, json=payload)
                    
                    if res.status_code == 200 or res.status_code == 201:
                        st.success("✅ Usuario creado exitosamente")
                        st.rerun()
                    else:
                        st.error(f"Error al guardar: {res.text}")
                else:
                    st.warning("Por favor rellena todos los campos")

    