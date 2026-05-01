import streamlit as st
import pandas as pd
import requests
# Importamos la función Y el diccionario
from conexion import get_baserow_data, TABLE_IDS , headers, URL_BASE

        



st.title("🎓 Gestión de Estudiantes")

# 1. CARGA DE DATOS
datos_estudiantes = get_baserow_data(TABLE_IDS["estudiante"])

if datos_estudiantes is not None:
    # Convertir a DataFrame y seleccionar columnas reales de Baserow
    df_original = pd.DataFrame(datos_estudiantes)
    
    # IMPORTANTE: Verifica que estos nombres coincidan con tus columnas en Baserow
    columnas_ver = ["id", "Nombre y Apellido", "Cedula", ] 
    
    # Filtrar solo las columnas que existen para evitar errores
    columnas_reales = [c for c in columnas_ver if c in df_original.columns]
    df_estudiantes = df_original[columnas_reales].copy()

    # --- VISTA PARA ADMINISTRADOR ---
    if st.session_state.rol == "Administrador":
        st.subheader("🔧 Panel de Control de Alumnos")
        st.info("💡 Edita las celdas directamente. Para agregar, usa el (+) al final. Para eliminar, selecciona la fila y presiona 'Supr'.")
        
        # Estilo celeste para encabezados
        st.markdown("""<style> div[data-testid="stDataEditor"] th { background-color: #87CEEB !important; color: black !important; font-weight: bold; } </style>""", unsafe_allow_html=True)

        # Editor dinámico
        df_editado = st.data_editor(
            df_estudiantes, 
            use_container_width=True, 
            num_rows="dynamic", 
            hide_index=True,
            key="editor_estudiantes"
        )

        if st.button("💾 Guardar Cambios en Base de Datos"):
            with st.spinner("Sincronizando con Baserow..."):
                exito = True
                
                # Obtener IDs actuales para saber qué borrar
                ids_finales = [str(x) for x in df_editado["id"].tolist() if pd.notnull(x)]
                ids_originales = [str(x) for x in df_estudiantes["id"].tolist()]

                # 1. ELIMINAR (Registros que estaban antes pero ya no están en el editor)
                for id_orig in ids_originales:
                    if id_orig not in ids_finales:
                        requests.delete(f"{URL_BASE}/{TABLE_IDS['estudiante']}/{id_orig}/", headers=headers)

                # 2. AGREGAR O MODIFICAR
                for _, fila in df_editado.iterrows():
                    # Limpieza de datos para evitar el error de JSON/NaN
                    payload = {
                        "Nombre y Apellido": str(fila["Nombre y Apellido"]).strip() if pd.notnull(fila["Nombre y Apellido"]) else "",
                        "Cedula": str(fila["Cedula"]).strip() if pd.notnull(fila["Cedula"]) else "",
                        
                    }
                    
                    id_actual = fila.get("id")

                    if pd.notnull(id_actual) and str(id_actual) != "":
                        # Actualizar (PATCH)
                        url = f"{URL_BASE}/{TABLE_IDS['estudiante']}/{id_actual}/?user_field_names=true"
                        requests.patch(url, headers=headers, json=payload)
                    else:
                        # Crear Nuevo (POST) - Solo si tiene nombre
                        if payload["Nombre y Apellido"] != "":
                            url = f"{URL_BASE}/{TABLE_IDS['estudiante']}/?user_field_names=true"
                            requests.post(url, headers=headers, json=payload)

                st.success("✅ ¡Lista de estudiantes actualizada correctamente!")
                st.rerun()

    