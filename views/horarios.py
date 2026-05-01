import streamlit as st
import pandas as pd
import requests
# Importamos la función Y el diccionario
from conexion import get_baserow_data, TABLE_IDS , headers, URL_BASE







st.title("🗓️ Gestión de Horarios ")

# 1. CARGA DE DATOS
datos_bloques = get_baserow_data(TABLE_IDS["Bloque"])
datos_clases = get_baserow_data(TABLE_IDS["Horarios"])

if datos_bloques:
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    
    # 2. LISTA DE HORAS (De la tabla bloque)
    horas_lista = [str(b.get("Hora", "")).strip() for b in datos_bloques if b.get("Hora")]
    horas_lista = list(dict.fromkeys(horas_lista)) # Eliminar duplicados
    
    # 3. CREAR CUADRÍCULA
    df_horario = pd.DataFrame(index=horas_lista, columns=dias).fillna("")
    
    # 4. MAPEO DE MATERIAS Y SUS IDS
    mapeo_clases_ids = {} 
    if datos_clases:
        for c in datos_clases:
            d = str(c.get("Dia", "")).strip()
            h = str(c.get("Bloque", "")).strip()
            m = str(c.get("materia", "")).strip()
            
            if d in dias and h in df_horario.index:
                df_horario.at[h, d] = m
                mapeo_clases_ids[(h, d)] = c.get("id")

    # --- VISTA PARA ADMINISTRADOR ---
    if st.session_state.rol == "Administrador":
        st.subheader("🔧 Panel de Edición")
        df_editado = st.data_editor(df_horario, use_container_width=True, num_rows="dynamic")

        if st.button("💾 Guardar y Actualizar Horario"):
            with st.spinner("Sincronizando con Baserow..."):
                exito = True
                
                for i in range(len(df_editado)):
                    h_edit = str(df_editado.index[i]).strip()
                    if not h_edit: continue

                    for j, d in enumerate(dias):
                        # Extraer valor de la celda de forma segura
                        val_raw = df_editado.iat[i, j]
                        valor_materia = str(val_raw).strip() if pd.notnull(val_raw) else ""
                        
                        id_reg = mapeo_clases_ids.get((h_edit, d))

                        # AL SER TEXTO: El payload es simple, sin corchetes
                        payload = {
                            "Dia": d,
                            "Bloque": h_edit, 
                            "materia": valor_materia
                        }

                        if id_reg:
                            # Si cambió algo, actualizamos
                            url = f"{URL_BASE}/{TABLE_IDS['Horarios']}/{id_reg}/?user_field_names=true"
                            requests.patch(url, headers=headers, json=payload)
                        elif valor_materia != "":
                            # Si es nuevo, creamos
                            url = f"{URL_BASE}/{TABLE_IDS['Horarios']}/?user_field_names=true"
                            requests.post(url, headers=headers, json=payload)
                
                st.success("✅ ¡Horario actualizado en tiempo real!")
                st.rerun()



        

    # --- VISTA PARA ESTUDIANTES ---
    else:
        st.subheader("📅  Horario Escolar")
        st.markdown("""
            <style>
                .t-horario { width: 100%; border-collapse: collapse; background-color: white; }
                .t-horario th { background-color: #ADD8E6 !important; color: black !important; font-weight: 900; border: 2px solid black; padding: 12px; text-align: center; }
                .t-horario td { background-color: white !important; color: black !important; font-weight: 800; border: 1px solid black; padding: 10px; text-align: center; }
            </style>
        """, unsafe_allow_html=True)

        html = '<table class="t-horario"><thead><tr><th style="background:#F0F0F0">HORA</th>'
        for d in dias: html += f'<th>{d}</th>'
        html += "</tr></thead><tbody>"

        for hora, fila in df_horario.iterrows():
            html += f'<tr><td style="background:#F0F0F0; font-weight:900">{hora}</td>'
            for d in dias: html += f'<td>{fila[d]}</td>'
            html += "</tr>"
        html += "</tbody></table>"
        st.markdown(html, unsafe_allow_html=True)
else:
    st.info("No hay horas configuradas.")

   