import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/procesado/nasa_neo_unido.csv")

columnas_req = ['diameter', 'missDistanceKm', 'closeApproachVelocityKmh']
df_limpio = df.dropna(subset=columnas_req).copy()

df_orbita = df_limpio[df_limpio['missDistanceKm'] < 75000000]

sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 7))

scatter = plt.scatter(
    x=df_orbita['missDistanceKm'], 
    y=df_orbita['closeApproachVelocityKmh'], 
    s=df_orbita['diameter'] * 50, 
    alpha=0.5,
    c=df_orbita['diameter'], 
    cmap='viridis',
    edgecolors='white',
    linewidths=0.5
)

plt.title("Análisis Orbital: Distancia vs Velocidad vs Tamaño", fontsize=15, fontweight='bold')
plt.xlabel("Distancia de Proximidad a la Tierra (km)", fontsize=12)
plt.ylabel("Velocidad de Proximidad (km/h)", fontsize=12)

cbar = plt.colorbar(scatter)
cbar.set_label('Diámetro (km)', fontsize=11)

plt.tight_layout()

carpeta_salida = "resultados"
os.makedirs(carpeta_salida, exist_ok=True)
ruta_imagen = f"{carpeta_salida}/distancia_vs_velocidad_vs_tamanho.png"
plt.savefig(ruta_imagen, dpi=300, bbox_inches='tight', facecolor='white')

plt.show()