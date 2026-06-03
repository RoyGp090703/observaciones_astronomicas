import time
import requests
import pandas as pd
from pathlib import Path

# Configuración de ruta y creación de directorio
ruta_destino = Path(__file__).resolve().parent.parent.parent / "data" / "crudo"
ruta_destino.mkdir(parents=True, exist_ok=True)

print("Descargando...")

CLAVE_API = "k9FkbUhAZgRdiZ2C8jHeTOkxpZqmUDND71prUdjX"
url = f"https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={CLAVE_API}"
REGISTROS_MAXIMOS = 2000
datos = []

# Extracción mediante paginación de la API
while url and len(datos) < REGISTROS_MAXIMOS:
    respuesta = requests.get(url).json()
    
    for neo in respuesta.get("near_earth_objects", []):
        if len(datos) >= REGISTROS_MAXIMOS:
            break
            
        # Extracción segura de datos anidados
        cercanos_crudo = neo.get("close_approach_data", [])
        cercanos_data = cercanos_crudo[0] if cercanos_crudo else {}
        
        diametro = neo.get("estimated_diameter", {}).get("kilometers", {})
        velocidad = cercanos_data.get("relative_velocity", {})
        distancia = cercanos_data.get("miss_distance", {})
        
        # Mapeo de campos al dataset
        datos.append({
            "id": neo.get("id"),
            "name": neo.get("name"),
            "nasaJplUrl": neo.get("nasa_jpl_url"),
            "absoluteMagnitude": neo.get("absolute_magnitude_h"),
            "estimatedDiameterMinKm": diametro.get("estimated_diameter_min"),
            "estimatedDiameterMaxKm": diametro.get("estimated_diameter_max"),
            "isPotentiallyHazardous": neo.get("is_potentially_hazardous_asteroid"),
            "isSentryObject": neo.get("is_sentry_object"),
            "closeApproachDate": cercanos_data.get("close_approach_date"),
            "closeApproachVelocityKmh": velocidad.get("kilometers_per_hour"),
            "missDistanceKm": distancia.get("kilometers"),
            "orbitingBody": cercanos_data.get("orbiting_body")
        })
    
    # Navegación a la siguiente página y pausa de seguridad
    url = respuesta.get("links", {}).get("next")
    time.sleep(1)

# Persistencia de datos en formato CSV
df_neo = pd.DataFrame(datos)
archivo_final = ruta_destino / "nasa_neo1.csv"
df_neo.to_csv(archivo_final, index=False, encoding='utf-8')

print(f" Archivo guardado en: {archivo_final}")