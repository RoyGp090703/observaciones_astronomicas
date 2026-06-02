import json
import requests
import pandas as pd
from pathlib import Path

ruta_destino = Path(__file__).resolve().parent.parent.parent / "data" / "crudo"
ruta_destino.mkdir(parents=True, exist_ok=True)

print("Descargando...")

parametros = {
    "fields": "full_name,class,neo,pha,H,diameter,albedo,rot_per,GM,density,e,a,q,i,om,w,ma,n,per,moid,condition_code,n_obs_used",
    "sb-cdata": json.dumps({"AND": ["neo|EQ|Y", "diameter|GT|0"]}),
    "limit": 100000
}

respuesta = requests.get("https://ssd-api.jpl.nasa.gov/sbdb_query.api", params=parametros).json()

df_jpl = pd.DataFrame(respuesta["data"], columns=respuesta["fields"])

for col in df_jpl.columns:
    try: df_jpl[col] = pd.to_numeric(df_jpl[col])
    except ValueError: pass

archivo_final = ruta_destino / "nasa_neo2.csv"
df_jpl.to_csv(archivo_final, index=False, encoding='utf-8')

print(f" Archivo guardado en: {archivo_final}")