import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

# Carga y limpieza de datos para el cálculo orbital
df = pd.read_csv("data/procesado/nasa_neo_unido.csv")
columnas = ['name', 'a', 'e', 'i', 'om', 'w', 'rot_per', 'diameter']
df_limpio = df.dropna(subset=columnas).copy()

for col in columnas[1:]:
    df_limpio[col] = pd.to_numeric(df_limpio[col], errors='coerce')
df_limpio = df_limpio.dropna(subset=columnas)

# Selección de los 5 asteroides más grandes para la visualización
df_top5 = df_limpio.nlargest(5, 'diameter')

# Configuración del espacio de trazado 3D
fig = plt.figure(figsize=(15, 12)) 
ax = fig.add_subplot(111, projection='3d')

# Representación del Sol y la órbita de la Tierra como puntos de referencia
ax.scatter(0, 0, 0, color='gold', s=400, edgecolors='black', zorder=10, label="Sol")
theta_tierra = np.linspace(0, 2 * np.pi, 100)
ax.plot(np.cos(theta_tierra), np.sin(theta_tierra), 0, color='dodgerblue', linestyle='--', linewidth=2, label='Tierra (1 UA)', zorder=5)

# Preparación de colores basada en el periodo de rotación
theta = np.linspace(0, 2 * np.pi, 300)
norm = Normalize(vmin=df_top5['rot_per'].min(), vmax=df_top5['rot_per'].max())
cmap = plt.get_cmap('viridis')

max_distancia_calculada = 0 

# Cálculo y trazado de trayectorias orbitales mediante elementos keplerianos
for _, row in df_top5.iterrows():
    a, e = row['a'], row['e']
    i_rad, om, w = np.radians(row['i']), np.radians(row['om']), np.radians(row['w'])
    
    r = (a * (1 - e**2)) / (1 + e * np.cos(theta))
    x_plan, y_plan = r * np.cos(theta), r * np.sin(theta)
    
    # Transformación de coordenadas al plano eclíptico
    x_ecl, y_ecl, z_ecl = [], [], []
    for xp, yp in zip(x_plan, y_plan):
        x1, y1 = xp * np.cos(w) - yp * np.sin(w), xp * np.sin(w) + yp * np.cos(w)
        x2, y2, z2 = x1, y1 * np.cos(i_rad), y1 * np.sin(i_rad)
        x3, y3, z3 = x2 * np.cos(om) - y2 * np.sin(om), x2 * np.sin(om) + y2 * np.cos(om), z2
        x_ecl.append(x3); y_ecl.append(y3); z_ecl.append(z3)
        
    max_distancia_calculada = max(max_distancia_calculada, np.max(np.abs(x_ecl)), np.max(np.abs(y_ecl)))
    ax.plot(x_ecl, y_ecl, z_ecl, color=cmap(norm(row['rot_per'])), alpha=0.9, linewidth=2.5, label=f"{row['name']} (D: {row['diameter']:.1f} km)")

# Ajustes estéticos, etiquetas y límites de cámara
ax.set_title("Trayectorias de los 5 NEOs con mayor diámetro con representación rotacional", fontsize=15, fontweight='bold')
ax.set_xlabel("X (UA)"); ax.set_ylabel("Y (UA)"); ax.set_zlabel("Z (UA)")
ax.xaxis.pane.fill = ax.yaxis.pane.fill = ax.zaxis.pane.fill = False
limite_camara = min(max_distancia_calculada, 4.0)
ax.set_xlim(-limite_camara, limite_camara); ax.set_ylim(-limite_camara, limite_camara); ax.set_zlim(-limite_camara, limite_camara)
ax.legend(loc='upper left', bbox_to_anchor=(-0.1, 1), fontsize=10)

# Barra de color para el periodo de rotación
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, shrink=0.5, pad=0.05)
cbar.set_label('Periodo de rotación (horas)', fontsize=12)

# Guardado de múltiples vistas (superior, lateral e isométrica)
carpeta_salida = "resultados"
os.makedirs(carpeta_salida, exist_ok=True)
ruta_base = f"{carpeta_salida}/trayectoria"
plt.savefig(f"{ruta_base}_vista1.png", dpi=300, bbox_inches='tight', facecolor='white')
ax.view_init(elev=90, azim=-90); plt.savefig(f"{ruta_base}_vista2.png", dpi=300, bbox_inches='tight', facecolor='white')
ax.view_init(elev=0, azim=-90); plt.savefig(f"{ruta_base}_vista3.png", dpi=300, bbox_inches='tight', facecolor='white')

ax.view_init(elev=30, azim=-60)
plt.show()