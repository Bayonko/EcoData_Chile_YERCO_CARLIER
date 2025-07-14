import requests

API_BASE = "https://mindicador.cl/api"

def consultar_indicador(tipo="dolar"):
    url = f"{API_BASE}/{tipo}"
    try:
        respuesta = requests.get(url)
        datos = respuesta.json()
        return datos
    except Exception as e:
        print("Error al consultar la API:", e)
        return None