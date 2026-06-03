import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carga y limpieza de datos para el análisis orbital
df = pd.read_csv("data/procesado/nasa_neo_unido.csv")
columnas_req = ['diameter', 'missDistanceKm', 'closeApproachVelocityKmh']
df_limpio = df.dropna(subset=columnas_req).copy()

# Preparación de variables: normalización de distancia
df_orbita = df_limpio.copy()
df_orbita['missDistance_norm'] = df_orbita['missDistanceKm'] / 1e7

# Configuración del estilo y área de trazado
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 7))

# Generación del gráfico de dispersión
scatter = plt.scatter(
    x=df_orbita['missDistance_norm'], 
    y=df_orbita['closeApproachVelocityKmh'], 
    s=df_orbita['diameter'] * 50, 
    alpha=0.7,  
    c=df_orbita['diameter'], 
    cmap='viridis',
    edgecolors='black', 
    linewidths=0.5
)

# Etiquetas y títulos para claridad interpretativa
plt.title("Relación entre la distancia a la Tierra, velocidad y tamaño del asteroide", fontsize=15, fontweight='bold')
plt.xlabel(r"Distancia a la Tierra ($10^7$ km)", fontsize=12)
plt.ylabel("Velocidad de proximidad (km/h)", fontsize=12)

# Barra de color para representar el diámetro
cbar = plt.colorbar(scatter)
cbar.set_label('Diámetro (km)', fontsize=12)

# Guardado de la visualización en formato PNG
plt.tight_layout()
carpeta_salida = "resultados"
os.makedirs(carpeta_salida, exist_ok=True)
ruta_imagen = f"{carpeta_salida}/distancia_vs_velocidad.png"
plt.savefig(ruta_imagen, dpi=300, bbox_inches='tight', facecolor='white')

plt.show()