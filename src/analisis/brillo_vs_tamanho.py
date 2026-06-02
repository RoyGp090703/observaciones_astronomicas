import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable 
from matplotlib.ticker import ScalarFormatter 

df = pd.read_csv("data/procesado/nasa_neo_unido.csv")

df_limpio = df.dropna(subset=['diameter', 'absoluteMagnitude']).copy()

df_limpio['diameter_m'] = df_limpio['diameter'] * 1000

h_min = df_limpio['absoluteMagnitude'].min()
h_max = df_limpio['absoluteMagnitude'].max()
df_limpio['H_brillo_norm'] = (h_max - df_limpio['absoluteMagnitude']) / (h_max - h_min)

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(11, 8))

limite_izq = df_limpio['H_brillo_norm'].min() - 0.05
limite_der = df_limpio['H_brillo_norm'].max() + 0.05

scatter = ax.scatter(
    x=df_limpio['H_brillo_norm'], 
    y=df_limpio['diameter_m'], 
    c=df_limpio['H_brillo_norm'], 
    cmap='plasma', 
    s=(df_limpio['diameter'] * 20) + 15, 
    alpha=0.7,
    edgecolors='white',
    linewidths=0.5,
    vmin=limite_izq, 
    vmax=limite_der  
)

ax.set_title("Relación entre el brillo de un asteroide y su tamaño", fontsize=15, fontweight='bold')
ax.set_ylabel("Diámetro (m)", fontsize=12) 

ax.set_xlim(limite_izq, limite_der) 
ax.set_yscale('log')

formateador = ScalarFormatter()
formateador.set_scientific(False)
ax.yaxis.set_major_formatter(formateador)

ax.tick_params(axis='x', labelbottom=False)

extremos = pd.concat([
    df_limpio.nlargest(2, 'diameter_m'),
    df_limpio.nsmallest(2, 'diameter_m')
])

for _, row in extremos.iterrows():
    if row['H_brillo_norm'] > 0.5:
        desplazamiento = (-15, 0) 
        alineacion = 'right' 
    else:
        desplazamiento = (15, 0) 
        alineacion = 'left' 
        
    ax.annotate(
        row['name'], 
        xy=(row['H_brillo_norm'], row['diameter_m']), 
        xytext=desplazamiento, 
        textcoords='offset points', 
        fontsize=10,
        fontweight='bold',
        color='#333333',
        va='center', 
        ha=alineacion, 
        arrowprops=dict(arrowstyle="-", color='gray', lw=1) 
    )

divider = make_axes_locatable(ax)
cax = divider.append_axes("bottom", size="4%", pad=0.05) 

cbar = plt.colorbar(scatter, cax=cax, orientation='horizontal')

cbar.set_label('') 
altura_y = -1.8 

cbar.ax.text(0.0, altura_y, 'Menos brillante', transform=cbar.ax.transAxes, 
             va='top', ha='left', fontsize=12, color='#4a0082')

cbar.ax.text(0.5, altura_y, 'Escala de brillo (H)', transform=cbar.ax.transAxes, 
             va='top', ha='center', fontsize=12, color="#000000")

cbar.ax.text(1.0, altura_y, 'Más brillante', transform=cbar.ax.transAxes, 
             va='top', ha='right', fontsize=12, color='#d4a000')

plt.tight_layout()

carpeta_salida = "resultados"
os.makedirs(carpeta_salida, exist_ok=True)
ruta_imagen = f"{carpeta_salida}/brillo_vs_tamanho.png"
plt.savefig(ruta_imagen, dpi=300, bbox_inches='tight', facecolor='white')

plt.show()