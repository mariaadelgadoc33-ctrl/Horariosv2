import streamlit as st
import requests# Función para alumnos/profes
from conexion import validar_usuario_baserow, validar_estudiante_baserow, validar_profesores_baserow




# Primero definimos la configuración de la página para evitar errores en Streamlit
st.set_page_config(page_title="Sistema Telemática", layout="wide")

st.markdown("""
    <style>
        /* 1. Fondo Principal (Azul Hielo) */
        .stApp {
            background: linear-gradient(135deg, #87CEEB 0%, #4FC3F7 100%);
        }
       

        /* 2. Barra Lateral (Azul Glaciar) */
        [data-testid="stSidebar"] {
            background-color: #d1e9ff !important;
            border-right: 2px solid #a3d1ff;
        }

        /* 3. Textos Generales (Azul Medianoche para legibilidad máxima) */
        html, body, p, label, .stMarkdown {
            color: #002d57 !important;
            font-family: 'Inter', 'Roboto', 'Helvetica Neue',  sans-serif;
        }

        /* 4. Títulos (Azul Real) */
        h1, h2, h3 {
            color: #004a99 !important;
            font-weight: 600 !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
        }

        /* 5. Botones (Azul Eléctrico) */
        .stButton>button {
            background-color: #0056b3 !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .stButton>button:hover {
            background-color: #003d80 !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        }

        /* 6. Inputs y Cajas de Texto (Bordes Azul Cielo) */
        .stTextInput>div>div>input, .stSelectbox>div>div>div {
            background-color: #ffffff !important;
            border: 1px solid #80bdff !important;
            color: #002d57 !important;
        }

        /* 7. Tablas y Data Editors (Encabezados Celeste) */
        [data-testid="stHeader"] {
            background-color: rgba(0,0,0,0) !important;
        }
        
        thead tr th {
            background-color: #007bff !important;
            color: white !important;
        }

        /* 8. Estilo para tarjetas o contenedores informativos */
        .stAlert {
            background-color: #e3f2fd !important;
            border: 1px solid #bbdefb !important;
            color: #004a99 !important;
        }
    </style>
    """, unsafe_allow_html=True)

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
                st.error("Clactive Maestra Incorrecta")

    else:
    # Estudiantes y Profesores piden lo mismo
         st.subheader(f"Ingreso para {rol_elegido}")
         cedula = st.text_input("Cedula")
    #clave = st.text_input("Contraseña", type="password")

    # PRIMERO: Creamos el botón. 
         if st.button(f"Entrar como {rol_elegido }", key=f"btn_{rol_elegido}"):
        
        # LUEGO: Verificamos si el campo está vacío (nota la sangría)
           if not cedula: 
            # Si está vacío, mostramos una advertencia
            st.warning("⚠️ Por favor, ingrese su Cedula para continuar.")
            
        # ACCIÓN: Si NO está vacío, procedemos con la validación normal
           else:
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
    # 1. Definir páginas (Tienen 4 espacios de sangría)
    inicio = st.Page("views/inicio.py", title="Inicio", icon="🏠")
    horarios = st.Page("views/horarios.py", title="Horarios", icon="📅")
    estudiantes = st.Page("views/estudiantes.py", title="Estudiantes", icon="🎓")
    profesores = st.Page("views/profesores.py", title="Profesores", icon="👨‍🏫")
    usuarios = st.Page("views/usuarios.py", title="Usuarios", icon="👥")

    # 2. FILTRO DE PERMISOS (También tienen 4 espacios de sangría)
    if st.session_state.rol == "Administrador":
        menu = [inicio, horarios, estudiantes, profesores, usuarios]
    else:
        # Estudiantes y Profesores solo visualizan
        menu = [inicio, horarios]

    # 3. NAVEGACIÓN (Sigue teniendo 4 espacios de sangría)
    st.sidebar.button("Cerrar Sesión", on_click=lambda: st.session_state.clear())
    
    pg = st.navigation(menu)
    pg.run()

