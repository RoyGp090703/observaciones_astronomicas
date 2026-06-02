import time
import requests
import pandas as pd
from pathlib import Path

ruta_destino = Path(__file__).resolve().parent.parent.parent / "data" / "crudo"
ruta_destino.mkdir(parents=True, exist_ok=True) 

url = "https://api.nasa.gov/neo/rest/v1/neo/browse?api_key=k9FkbUhAZgRdiZ2C8jHeTOkxpZqmUDND71prUdjX"
datos = []

print("Descargando...")

while url and len(datos) < 2000:
    respuesta = requests.get(url).json()
    
    for ast in respuesta.get("near_earth_objects", []):
        if len(datos) >= 2000: break
        
        acercamiento = ast.get("close_approach_data", [{}])[0] if ast.get("close_approach_data") else {}
        diametro = ast.get("estimated_diameter", {}).get("kilometers", {})
        
        datos.append({
            "id": ast.get("id"),
            "name": ast.get("name"),
            "nasaJplUrl": ast.get("nasa_jpl_url"),
            "absoluteMagnitude": ast.get("absolute_magnitude_h"),
            "estimatedDiameterMinKm": diametro.get("estimated_diameter_min"),
            "estimatedDiameterMaxKm": diametro.get("estimated_diameter_max"),
            "isPotentiallyHazardous": ast.get("is_potentially_hazardous_asteroid"),
            "isSentryObject": ast.get("is_sentry_object"),
            "closeApproachDate": acercamiento.get("close_approach_date"),
            "closeApproachVelocityKmh": acercamiento.get("relative_velocity", {}).get("kilometers_per_hour"),
            "missDistanceKm": acercamiento.get("miss_distance", {}).get("kilometers"),
            "orbitingBody": acercamiento.get("orbiting_body")
        })
        
    url = respuesta.get("links", {}).get("next")
    time.sleep(1)

archivo_final = ruta_destino / "nasa_neo1.csv"
pd.DataFrame(datos).to_csv(archivo_final, index=False, encoding='utf-8')

print(f" Archivo guardado en: {archivo_final}")