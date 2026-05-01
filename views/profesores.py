import streamlit as st
import pandas as pd
import requests
# Importamos la función Y el diccionario
from conexion import get_baserow_data, TABLE_IDS , headers, URL_BASE


st.title("👨‍🏫 Gestión de Profesores")

# 1. CARGA DE DATOS
datos_profesores = get_baserow_data(TABLE_IDS["profesores"])

if datos_profesores is not None:
    df_original = pd.DataFrame(datos_profesores)
    
    # Nombres de columnas según tu Baserow (Ajusta si es necesario)
    columnas_ver = ["id", "Nombre y Apellido", "cedula", "Materia"] 
    
    columnas_reales = [c for c in columnas_ver if c in df_original.columns]
    df_profesores = df_original[columnas_reales].copy()

    # --- VISTA PARA ADMINISTRADOR ---
    if st.session_state.rol == "Administrador":
        st.subheader("🔧 Panel de Control de Docentes")
        st.info("💡 Edita las celdas directamente. Usa el (+) para agregar y 'Supr' para eliminar filas.")
        
        # Estilo coherente con el sistema
        st.markdown("""<style> div[data-testid="stDataEditor"] th { background-color: #87CEEB !important; color: black !important; font-weight: bold; } </style>""", unsafe_allow_html=True)

        df_editado = st.data_editor(
            df_profesores, 
            use_container_width=True, 
            num_rows="dynamic", 
            hide_index=True,
            key="editor_profesores"
        )

        if st.button("💾 Guardar Cambios"):
            with st.spinner("Actualizando profesores..."):
                exito = True
                
                # Identificar eliminaciones
                ids_finales = [str(x) for x in df_editado["id"].tolist() if pd.notnull(x)]
                ids_originales = [str(x) for x in df_profesores["id"].tolist()]

                for id_orig in ids_originales:
                    if id_orig not in ids_finales:
                        requests.delete(f"{URL_BASE}/{TABLE_IDS['profesores']}/{id_orig}/", headers=headers)

                # Agregar o Modificar
                for _, fila in df_editado.iterrows():
                    payload = {
                        "Nombre y Apellido": str(fila["Nombre y Apellido"]).strip() if pd.notnull(fila["Nombre y Apellido"]) else "",
                        "cedula": str(fila["cedula"]).strip() if pd.notnull(fila["cedula"]) else "",
                        "Materia": str(fila["Materia"]).strip() if pd.notnull(fila["Materia"]) else ""
                    }
                    
                    id_actual = fila.get("id")

                    if pd.notnull(id_actual) and str(id_actual) != "":
                        url = f"{URL_BASE}/{TABLE_IDS['profesores']}/{id_actual}/?user_field_names=true"
                        requests.patch(url, headers=headers, json=payload)
                    else:
                        if payload["Nombre y Apellido"] != "":
                            url = f"{URL_BASE}/{TABLE_IDS['profesores']}/?user_field_names=true"
                            requests.post(url, headers=headers, json=payload)

                st.success("✅ ¡Actualizado!")
                st.rerun()

    # --- VISTA PARA OTROS ROLES ---
    else:
        st.subheader("📋 Lista de Profesores")
        st.dataframe(df_profesores, use_container_width=True, hide_index=True)

else:
    st.warning("No hay profesores registrados.")
