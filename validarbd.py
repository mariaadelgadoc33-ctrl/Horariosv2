import requests

# Datos confirmados
TOKEN = "6pgKWAUjOrtjtOMFG4MbZJUoz6J11xxa"
DATABASE_ID = "819535" 

# La URL debe tener barras "/" claras entre cada palabra
URL = "https://api.baserow.io/" + DATABASE_ID + "/"

headers = {"Authorization": f"Token {TOKEN}"}

print(f"--- CONSULTANDO BASE DE DATOS: {DATABASE_ID} ---")
print(f"--- url: {URL} ---")

try:
    # Usamos un timeout de 10 segundos para que no se quede colgado
    #response = requests.get(URL, headers=headers, timeout=10)
    #response = requests.get("https://api.baserow.io/361684/", headers={"Authorization": "Token YOUR_DATABASE_TOKEN" })
    response = requests.get("https://api.baserow.io/api/database/tables/all-tables/",
    headers= headers)
    if response.status_code == 200:
        tablas = response.json()
        print("✅ ¡CONEXIÓN EXITOSA! Aquí están tus IDs reales:\n")
        for t in tablas:
            print(f"TABLA: {t['name']} --> ID: {t['id']}")
    elif response.status_code == 401:
        print("❌ ERROR: El TOKEN no es válido. Genéralo de nuevo en Baserow.")
    elif response.status_code == 404:
        print(f"❌ ERROR: El DATABASE_ID {DATABASE_ID} no existe.")
    else:
        print(f"❌ ERROR {response.status_code}: {response.text}")

except Exception as e:
    print(f"❌ FALLO TÉCNICO: {e}")
