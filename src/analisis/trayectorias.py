import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

df = pd.read_csv("data/procesado/nasa_neo_unido.csv")

columnas = ['name', 'a', 'e', 'i', 'om', 'w', 'rot_per', 'diameter']
df_limpio = df.dropna(subset=columnas).copy()

for col in columnas[1:]:
    df_limpio[col] = pd.to_numeric(df_limpio[col], errors='coerce')

df_limpio = df_limpio.dropna(subset=columnas)

df_top5 = df_limpio.nlargest(5, 'diameter')

fig = plt.figure(figsize=(15, 12)) 
ax = fig.add_subplot(111, projection='3d')

ax.scatter(0, 0, 0, color='gold', s=400, edgecolors='black', zorder=10, label="Sol")

theta_tierra = np.linspace(0, 2 * np.pi, 100)
ax.plot(np.cos(theta_tierra), np.sin(theta_tierra), 0, color='dodgerblue', linestyle='--', linewidth=2, label='Tierra (1 UA)', zorder=5)

theta = np.linspace(0, 2 * np.pi, 300)

norm = Normalize(vmin=df_top5['rot_per'].min(), vmax=df_top5['rot_per'].max())
cmap = plt.get_cmap('viridis')

max_distancia_calculada = 0 

for _, row in df_top5.iterrows():
    a = row['a']
    e = row['e']
    i_rad = np.radians(row['i'])
    om = np.radians(row['om'])
    w = np.radians(row['w'])
    
    r = (a * (1 - e**2)) / (1 + e * np.cos(theta))
    
    x_plan = r * np.cos(theta)
    y_plan = r * np.sin(theta)
    
    x_ecl, y_ecl, z_ecl = [], [], []
    
    for xp, yp in zip(x_plan, y_plan):
        x1 = xp * np.cos(w) - yp * np.sin(w)
        y1 = xp * np.sin(w) + yp * np.cos(w)
        
        x2 = x1
        y2 = y1 * np.cos(i_rad)
        z2 = y1 * np.sin(i_rad)
        
        x3 = x2 * np.cos(om) - y2 * np.sin(om)
        y3 = x2 * np.sin(om) + y2 * np.cos(om)
        z3 = z2
        
        x_ecl.append(x3)
        y_ecl.append(y3)
        z_ecl.append(z3)
        
    max_distancia_calculada = max(max_distancia_calculada, np.max(np.abs(x_ecl)), np.max(np.abs(y_ecl)))
        
    color_linea = cmap(norm(row['rot_per']))
    etiqueta = f"{row['name']} (D: {row['diameter']:.1f} km)"
    ax.plot(x_ecl, y_ecl, z_ecl, color=color_linea, alpha=0.9, linewidth=2.5, label=etiqueta)

ax.set_title("Trayectorias de los 5 NEOs con mayor diámetro con representación rotacional", fontsize=15, fontweight='bold')
ax.set_xlabel("X (UA)", fontsize=12)
ax.set_ylabel("Y (UA)", fontsize=12)
ax.set_zlabel("Z (UA)", fontsize=12)

ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor('w')
ax.yaxis.pane.set_edgecolor('w')
ax.zaxis.pane.set_edgecolor('w')

limite_camara = min(max_distancia_calculada, 4.0)

ax.set_xlim(-limite_camara, limite_camara)
ax.set_ylim(-limite_camara, limite_camara)
ax.set_zlim(-limite_camara, limite_camara)

ax.legend(loc='upper left', bbox_to_anchor=(-0.1, 1), fontsize=10)

sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, shrink=0.5, pad=0.05)
cbar.set_label('Periodo de rotación (horas)', fontsize=12)

carpeta_salida = "resultados"
os.makedirs(carpeta_salida, exist_ok=True)

ruta_imagen1 = f"{carpeta_salida}/vista1_trayectorias.png"
plt.savefig(ruta_imagen1, dpi=300, bbox_inches='tight', facecolor='white')

ax.view_init(elev=90, azim=-90)
ruta_imagen2 = f"{carpeta_salida}/vista2_trayectorias.png"
plt.savefig(ruta_imagen2, dpi=300, bbox_inches='tight', facecolor='white')

ax.view_init(elev=0, azim=-90)
ruta_imagen3 = f"{carpeta_salida}/vista3_trayectorias.png"
plt.savefig(ruta_imagen3, dpi=300, bbox_inches='tight', facecolor='white')

ax.view_init(elev=30, azim=-60)
plt.show()