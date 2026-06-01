import streamlit as st
import pandas as pd

# Importamos la función Y el diccionario
from conexion import get_baserow_data, TABLE_IDS , headers, URL_BASE




# Inicializamos la variable en la memoria para saber qué sección está activa
if "modulo_activo" not in st.session_state:
    st.session_state.modulo_activo = "Menú Principal"

# --- LÓGICA DE RETORNO (La flecha intuitiva para devolverse) ---
if st.session_state.modulo_activo != "Menú Principal":
    if st.button("⬅️ Volver al Panel de Control Principal", type="secondary", key="btn_global_back"):
        st.session_state.modulo_activo = "Menú Principal"
        st.rerun()
    st.divider()

    # Importación y ejecución directa según la selección del menú desplegable centrado
    from conexion import get_baserow_data, TABLE_IDS, headers, URL_BASE
    
    try:
        if st.session_state.modulo_activo == "Horarios Escolares":
            import views.horarios as v_horarios
            # Si tu archivo tiene la función mostrar_modulo, la ejecuta aquí:
            if hasattr(v_horarios, 'mostrar_modulo'): v_horarios.mostrar_modulo()
        elif st.session_state.modulo_activo == "Control de Estudiantes":
            import views.estudiantes as v_estudiantes
            if hasattr(v_estudiantes, 'mostrar_modulo'): v_estudiantes.mostrar_modulo()
        elif st.session_state.modulo_activo == "Plantel de Profesores":
            import views.profesores as v_profesores
            if hasattr(v_profesores, 'mostrar_modulo'): v_profesores.mostrar_modulo()
        elif st.session_state.modulo_activo == "Gestión de Usuarios":
            import views.usuarios as v_usuarios
            if hasattr(v_usuarios, 'mostrar_modulo'): v_usuarios.mostrar_modulo()
    except Exception as e:
        st.error(f"Error al cargar el módulo seleccionado: {e}")

# --- VISTA DEL PANEL DE CONTROL CENTRADO ---
else:
    # Inyección de estilos CSS para los cuadros redondeados, enmarcados en negro y centrados
    st.markdown("""
        <style>
            .cuadro-modulo {
                background-color: #ffffff;
                border: 2px solid #000000; /* Enmarcado con negro */
                border-radius: 15px;       /* Redondeado en las esquinas */
                padding: 20px;
                margin-bottom: 15px;
                text-align: center;        /* Módulos en el medio centrados */
                box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            }
            .titulo-modulo {
                font-size: 20px;
                font-weight: bold;
                color: #004a99;
                margin-bottom: 5px;
            }
            .indicador-flecha {
                font-size: 16px;
                font-weight: bold;
                color: #002d57;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<br><h1 style='text-align: center;'>🎛️ Panel de Control Principal</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 18px;'>Bienvenido al sistema. Rol activo: <b>{st.session_state.rol}</b></p><br>", unsafe_allow_html=True)

    # Forzar el centrado del selector mediante el sistema de columnas de Streamlit
    izq_space, col_central, der_space = st.columns([1, 2, 1])

    with col_central:
        st.markdown("<h3 style='text-align: center; margin-bottom: 25px;'>¿Qué módulo desea gestionar hoy?</h3>", unsafe_allow_html=True)
        
        # Renderizado de cuadros de información según el Rol del usuario
        if st.session_state.rol == "Administrador":
            # Cuadro 1: Horarios
            st.markdown("""
                <div class="cuadro-modulo">
                    <div class="titulo-modulo">📅 Horarios Escolares</div>
                    <div class="indicador-flecha">👈 Selecciona "Horarios" en el menú lateral izquierdo</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Cuadro 2: Estudiantes
            st.markdown("""
                <div class="cuadro-modulo">
                    <div class="titulo-modulo">🎓 Control de Estudiantes</div>
                    <div class="indicador-flecha">👈 Selecciona "Estudiantes" en el menú lateral izquierdo</div>
                </div>
            """, unsafe_allow_html=True)
                
            # Cuadro 3: Profesores
            st.markdown("""
                <div class="cuadro-modulo">
                    <div class="titulo-modulo">👨‍🏫 Plantel de Profesores</div>
                    <div class="indicador-flecha">👈 Selecciona "Profesores" en el menú lateral izquierdo</div>
                </div>
            """, unsafe_allow_html=True)
                
            # Cuadro 4: Usuarios
            st.markdown("""
                <div class="cuadro-modulo">
                    <div class="titulo-modulo">👥 Gestión de Usuarios</div>
                    <div class="indicador-flecha">👈 Selecciona "Usuarios" en el menú lateral izquierdo</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Estudiantes y Profesores solo ven el cuadro de Horarios
            st.markdown("""
                <div class="cuadro-modulo">
                    <div class="titulo-modulo">📅 Horarios Escolares</div>
                    <div class="indicador-flecha">👈 Selecciona "Horarios" en el menú lateral izquierdo</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Cerrar Sesión de Forma Segura", use_container_width=True, key="btn_logout_dashboard"):
            st.session_state.clear()
            st.rerun()
