import requests
import streamlit as st


# --- CONFIGURACIÓN ---
TOKEN = "6pgKWAUjOrtjtOMFG4MbZJUoz6J11xxa"
URL_BASE = "https://api.baserow.io"

# IDs ACTUALIZADOS SEGÚN TU CONSULTA
TABLE_IDS = {
    "estudiante": "819535",
    "Horarios": "819596",
    "materia": "819630",
    "bloque": "936697",
    "profesores": "936712",
    "usuario": "936720"
}

headers = {"Authorization": f"Token {TOKEN}"}
URL_BASE = "https://api.baserow.io/api/database/rows/table"

def get_baserow_data(table_id):
    # Construcción precisa de la URL de filas
    url = f"{URL_BASE}/{table_id}/?user_field_names=true"
    #url = f"https://baserow.io/{table_id}/?user_field_names=true" /api/database/rows/table/
    print(f"\n--- URL GENERADA: {url} ---")
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('results', [])
        else:
            st.error(f"Error {response.status_code} en tabla {table_id}")
            return []
    except Exception as e:
        st.error(f"Fallo de conexión: {e}")
        return []



def validar_usuario_baserow(cedula, rol):
    """
    Busca en la tabla de usuarios de Baserow un registro que coincida
    con el correo, la contraseña y el rol proporcionado.
    """
    # Usamos el ID de la tabla de usuarios que ya tienes (936720)
    id_tabla_usuario = "936720"
    url = f"{URL_BASE}/{id_tabla_usuario}/?user_field_names=true"
    
    try:
        response = requests.get(url,headers=headers)
        
        if response.status_code == 200:
            usuarios = response.json().get('results', [])
            
            for u in usuarios:
                # Obtenemos los valores de Baserow (ajusta los nombres si son distintos)
                cedula = str(u.get('cedula', '')).strip()
                #b_pass = str(u.get('Password', '')).strip()
                b_rol = str(u.get('Rol', '')).strip()
                
                # Comprobación exacta
                if cedula == cedula.strip() and b_rol == rol:
                    return True # Credenciales correctas
                    
            return False # No se encontró coincidencia
        else:
            return False
            
    except Exception as e:
        print(f"Error en validación: {e}")
        return False




def validar_estudiante_baserow(cedula,):
    """
    Busca en la tabla de usuarios de Baserow un registro que coincida
    con el correo, la contraseña y el rol proporcionado.
    """
    # Usamos el ID de la tabla de usuarios que ya tienes (936720)
    id_tabla_estudiante = "819535"
    url = f"{URL_BASE}/{id_tabla_estudiante}/?user_field_names=true"
    
    try:
        response = requests.get(url,headers=headers)
        
        if response.status_code == 200:
            usuarios = response.json().get('results', [])
            
            for u in usuarios:
                # Obtenemos los valores de Baserow (ajusta los nombres si son distintos)
                cedula = str(u.get('cedula', '')).strip()
                #b_pass = str(u.get('Password', '')).strip()
                
                
                # Comprobación exacta
                if cedula == cedula.strip():
                    return True # Credenciales correctas
                    
            return False # No se encontró coincidencia
        else:
            return False
            
    except Exception as e:
        print(f"Error en validación: {e}")
        return False
    

def validar_profesores_baserow(cedula,):
    """
    Busca en la tabla de usuarios de Baserow un registro que coincida
    con el correo, la contraseña y el rol proporcionado.
    """
    # Usamos el ID de la tabla de usuarios que ya tienes (936720)
    id_tabla_profesores = "9367122"
    url = f"{URL_BASE}/{id_tabla_profesores}/?user_field_names=true"
    
    try:
        response = requests.get(url,headers=headers)
        
        if response.status_code == 200:
            usuarios = response.json().get('results', [])
            
            for u in usuarios:
                # Obtenemos los valores de Baserow (ajusta los nombres si son distintos)
                cedula = str(u.get('cedula', '')).strip()
                #b_pass = str(u.get('Password', '')).strip()
                
                
                # Comprobación exacta
                if cedula == cedula.strip():
                    return True # Credenciales correctas
                    
            return False # No se encontró coincidencia
        else:
            return False
            
    except Exception as e:
        print(f"Error en validación: {e}")
        return False
    

    





















