import time
import requests
import pandas as pd
from pathlib import Path

# Configuración de rutas y límites
BASE_PATH = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_PATH / "data" / "crudo"
DATA_DIR.mkdir(parents=True, exist_ok=True)

API_KEY = "k9FkbUhAZgRdiZ2C8jHeTOkxpZqmUDND71prUdjX"
BASE_URL = "https://api.nasa.gov/neo/rest/v1/neo/browse"
MAX_RECORDS = 2000

def fetch_neo_data():
    """Extrae datos de la API de NASA NeoWs manejando paginación."""
    url = f"{BASE_URL}?api_key={API_KEY}"
    extracted_data = []

    print(f"Iniciando extracción de hasta {MAX_RECORDS} registros...")

    while url and len(extracted_data) < MAX_RECORDS:
        response = requests.get(url)
        response.raise_for_status()  # Detecta errores HTTP automáticamente
        payload = response.json()
        
        for neo in payload.get("near_earth_objects", []):
            if len(extracted_data) >= MAX_RECORDS:
                break
            
            # Normalización de datos anidados para aplanamiento estructural
            approach_data = neo.get("close_approach_data", [{}])[0]
            diameter = neo.get("estimated_diameter", {}).get("kilometers", {})
            velocity = approach_data.get("relative_velocity", {})
            distance = approach_data.get("miss_distance", {})
            
            extracted_data.append({
                "id": neo.get("id"),
                "name": neo.get("name"),
                "nasaJplUrl": neo.get("nasa_jpl_url"),
                "absoluteMagnitude": neo.get("absolute_magnitude_h"),
                "estimatedDiameterMinKm": diameter.get("estimated_diameter_min"),
                "estimatedDiameterMaxKm": diameter.get("estimated_diameter_max"),
                "isPotentiallyHazardous": neo.get("is_potentially_hazardous_asteroid"),
                "isSentryObject": neo.get("is_sentry_object"),
                "closeApproachDate": approach_data.get("close_approach_date"),
                "closeApproachVelocityKmh": velocity.get("kilometers_per_hour"),
                "missDistanceKm": distance.get("kilometers"),
                "orbitingBody": approach_data.get("orbiting_body")
            })
        
        # Navegación hacia la siguiente página del set de datos
        url = payload.get("links", {}).get("next")
        time.sleep(1) # Respeto al rate-limiting del servidor

    return extracted_data

if __name__ == "__main__":
    neo_dataset = fetch_neo_data()
    
    # Persistencia en formato tabular optimizado
    output_file = DATA_DIR / "nasa_neo1.csv"
    pd.DataFrame(neo_dataset).to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"Proceso completado. Dataset guardado en: {output_file}")