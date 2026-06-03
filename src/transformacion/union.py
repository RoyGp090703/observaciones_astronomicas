import pandas as pd
from pathlib import Path

# Configuración de rutas para directorios de datos
raiz = Path(__file__).resolve().parent.parent.parent
dir_crudo = raiz / "data" / "crudo"
dir_procesado = raiz / "data" / "procesado"
dir_procesado.mkdir(parents=True, exist_ok=True)

print("Cruzando datasets...")

# Carga de archivos fuente desde el directorio crudo
df_neo = pd.read_csv(dir_crudo / "nasa_neo1.csv")
df_jpl = pd.read_csv(dir_crudo / "nasa_neo2.csv")

# Limpieza de nombres para asegurar consistencia en la unión
df_neo['name'] = df_neo['name'].astype(str).str.strip()
df_jpl['full_name'] = df_jpl['full_name'].astype(str).str.strip()

# Fusión (merge) de datasets basada en el nombre del asteroide
df_final = pd.merge(df_neo, df_jpl, left_on="name", right_on="full_name", how="inner")
df_final = df_final.drop(columns=["full_name"]) 

# Persistencia del dataset unificado en directorio procesado
ruta_salida = dir_procesado / "nasa_neo_unido.csv"
df_final.to_csv(ruta_salida, index=False, encoding='utf-8')

print(f" Archivo guardado en: {ruta_salida}")