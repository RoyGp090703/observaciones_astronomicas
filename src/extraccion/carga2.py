import sys
import json
import requests
import pandas as pd
from pathlib import Path

# Forzamos la codificación UTF-8 en la consola para evitar errores de impresión en Windows
sys.stdout.reconfigure(encoding='utf-8')

# Resolución dinámica de rutas
# Asumiendo que el script está en: proyecto/src/extraccion/script.py
DIRECTORIO_ACTUAL = Path(__file__).resolve().parent
RAIZ_PROYECTO = DIRECTORIO_ACTUAL.parent.parent
DIRECTORIO_DESTINO = RAIZ_PROYECTO / "data" / "raw"

# Creamos el directorio destino si no existe
DIRECTORIO_DESTINO.mkdir(parents=True, exist_ok=True)

URL_API = "https://ssd-api.jpl.nasa.gov/sbdb_query.api"

# Motor lógico de búsqueda: Solo objetos con diámetro y albedo mayor a 0
reglas_filtro = {
    "AND": [
        "diameter|GT|0",
        "albedo|GT|0"
    ]
}

# Cadena exhaustiva con prácticamente todos los campos útiles de la API:
# Identificación y Banderas: full_name, class, neo, pha
# Propiedades Físicas: H, diameter, albedo, rot_per (periodo rotación), GM, density
# Elementos Orbitales: e (excentricidad), a (semieje mayor), q (perihelio), i (inclinación), om, w, ma, n, per (periodo)
# Distancias y Calidad: moid (distancia de intersección con la Tierra), condition_code, n_obs_used
CAMPOS_EXHAUSTIVOS = "full_name,class,neo,pha,H,diameter,albedo,rot_per,GM,density,e,a,q,i,om,w,ma,n,per,moid,condition_code,n_obs_used"

parametros_consulta = {
    "fields": CAMPOS_EXHAUSTIVOS,
    "sb-cdata": json.dumps(reglas_filtro),
    "limit": 1500  # Límite de registros para el dataset
}

print("Lanzando consulta...")
respuesta = requests.get(URL_API, params=parametros_consulta)

if respuesta.status_code == 200:
    datos_crudos = respuesta.json()
    
    # Extraemos las cabeceras (columnas) y las filas de datos
    columnas = datos_crudos.get("fields", [])
    filas = datos_crudos.get("data", [])
    
    # Construcción del DataFrame
    df_jpl = pd.DataFrame(filas, columns=columnas)
    
    # Convertimos automáticamente cualquier columna que parezca número de string a float/int.
    # Usamos un enfoque vectorizado para no tener que listar manualmente las 20 columnas numéricas.
    df_jpl = df_jpl.apply(pd.to_numeric, errors='ignore')
    
    # Definimos la ruta final del archivo CSV
    ruta_archivo = DIRECTORIO_DESTINO / "nasa_neo2.csv"
    
    # Guardado directo preservando codificación y sin índice numérico
    df_jpl.to_csv(ruta_archivo, index=False, encoding='utf-8')
    
    print(f"\n Extracción y carga completadas exitosamente.")
    print(f"Ubicación: {ruta_archivo}")
    print(f"Total de registros insertados: {len(df_jpl)}")

else:
    print(f"\n Falló la conexión con la API.")
    print(f"Código HTTP: {respuesta.status_code}")
    print(f"Detalle del error: {respuesta.text}")