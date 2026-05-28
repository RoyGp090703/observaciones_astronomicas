import sys
from pathlib import Path
import pandas as pd
from apify_client import ApifyClient

# Forzamos la codificación UTF-8 en la consola para evitar errores de caracteres
sys.stdout.reconfigure(encoding='utf-8')

# Calculamos la ruta absoluta del directorio del proyecto dinámicamente.
# Path(__file__).resolve().parent apunta a 'src/extraccion'
# Subimos dos niveles (.parent.parent) para llegar a la raíz del proyecto.
DIRECTORIO_ACTUAL = Path(__file__).resolve().parent
RAIZ_PROYECTO = DIRECTORIO_ACTUAL.parent.parent
DIRECTORIO_DESTINO = RAIZ_PROYECTO / "data" / "raw"

# Creamos la ruta de destino si no existe (parents=True crea las carpetas intermedias)
DIRECTORIO_DESTINO.mkdir(parents=True, exist_ok=True)

# Mover el token a un archivo .env para mayor seguridad antes del paso a producción
TOKEN_APIFY = "apify_api_WbDJAhXtKm8vHoVNEIKv8vSL0LjnNx1FRMqd"
cliente_apify = ApifyClient(TOKEN_APIFY)

# Parámetros para el Actor de Apify (Wrapper de NASA NeoWs)
parametros_extraccion = {
    "apiKey": "DEMO_KEY",
    "feedMode": "browse", # 'browse' extrae el catálogo general
    "maxResults": 50      # Límite de prueba para conservar créditos
}

print("Lanzando API...")

try:
    # Llamada síncrona al Actor
    ejecucion = cliente_apify.actor("compute-edge/nasa-neo-scraper").call(run_input=parametros_extraccion)
    id_dataset = ejecucion["defaultDatasetId"]
    
    print(f"Dataset generado exitosamente. Descargando ID: {id_dataset}...")
    
    # Conversión del dataset iterador a una lista de diccionarios
    datos_asteroides = list(cliente_apify.dataset(id_dataset).iterate_items())

except Exception as e:
    print(f"Error crítico durante la conexión o ejecución del scraper: {e}")
    datos_asteroides = []

if datos_asteroides:
    # Convertimos el JSON estructurado en un DataFrame tabular
    df_neo = pd.DataFrame(datos_asteroides)
    
    # Definimos la ruta completa del archivo de salida
    ruta_archivo = DIRECTORIO_DESTINO / "nasa_neo.csv"
    
    # Guardamos el DataFrame preservando la codificación y sin índice numérico
    df_neo.to_csv(ruta_archivo, index=False, encoding='utf-8')
    
    print(f"\n Extracción y carga completadas exitosamente.")
    print(f"Ubicación: {ruta_archivo}")
    print(f"Total de registros insertados: {len(df_neo)}")
else:
    print("\nAdvertencia: La ejecución finalizó pero no se recuperaron datos. Revisa los límites de la DEMO_KEY.")