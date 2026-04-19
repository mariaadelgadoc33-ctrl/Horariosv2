import streamlit as st
import requests# Función para alumnos/profes
from conexion import validar_usuario_baserow, validar_estudiante_baserow

st.set_page_config(page_title="Sistema Telemática", layout="wide")

# 1. Definir la Clave Maestra del Administrador
CLAVE_MAESTRA_ADMIN = "Admin1234" # Tú puedes cambiarla aquí

# 2. Inicializar estados de sesión
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.rol = None

# --- INTERFAZ DE LOGIN ---
if not st.session_state.autenticado:
    st.title("🛡️ Sistema de Control de Horarios")
    
    # PASO A: Elegir el Rol
    rol_elegido = st.radio("Seleccione su perfil para ingresar:", 
                          ["Administrador", "Estudiante", "Profesor"], 
                          horizontal=True)

    st.divider()

    # PASO B: Formulario según el Rol
    if rol_elegido == "Administrador":
        st.subheader("Acceso Restringido - Administrador")
        clave_admin = st.text_input("Ingrese la Clave Maestra de Seguridad", type="password")
        if st.button("Validar Acceso Admin"):
            if clave_admin == CLAVE_MAESTRA_ADMIN:
                st.session_state.autenticado = True
                st.session_state.rol = "Administrador"
                st.rerun()
            else:
                st.error("Clave Maestra Incorrecta")

    else:
        # Estudiantes y Profesores piden lo mismo
        st.subheader(f"Ingreso para {rol_elegido}")
        cedula = st.text_input("Cedula")
        #clave = st.text_input("Contraseña", type="password")
        
        if st.button(f"Entrar como {rol_elegido}"):
            # Validamos contra la base de datos de Baserow
            es_valido = validar_estudiante_baserow(cedula)
            if es_valido:
                st.session_state.autenticado = True
                st.session_state.rol = rol_elegido
                st.rerun()
            else:
                st.error("Cedula incorrectos para este rol")

# --- INTERFAZ PROTEGIDA (POST-LOGIN) ---
else:
    # Definir páginas
    inicio = st.Page("views/inicio.py", title="Inicio", icon="🏠")
    horarios = st.Page("views/horarios.py", title="Horarios", icon="📅")
    estudiantes = st.Page("views/estudiantes.py", title="Estudiantes", icon="🎓")
    profesores = st.Page("views/profesores.py", title="Profesores", icon="👨‍🏫")
    usuarios = st.Page("views/usuarios.py", title="Usuarios", icon="👥")

    # 3. FILTRO DE PERMISOS: Solo el Admin ve todo
    if st.session_state.rol == "Administrador":
        menu = [inicio, horarios, estudiantes, profesores, usuarios]
    else:
        # Estudiantes y Profesores solo visualizan
        menu = [inicio, horarios]

    st.sidebar.button("Cerrar Sesión", on_click=lambda: st.session_state.clear())
    
    pg = st.navigation(menu)
    pg.run()





































