# Observaciones astronómicas

| Autor | Contacto |
| :--- | :--- |
| **Lina Nicole Reyes Nava** | linareyes@ciencias.unam.mx  |
| **Rodrigo García Peláez** | rodrigo090703@ciencias.unam.mx |

---

## Descripción
Este proyecto integra información proveniente de dos bases de datos oficiales de la NASA sobre Objetos Cercanos a la Tierra (**NEOs**, por sus siglas en inglés). El motor de procesamiento correlaciona los registros de ambas fuentes para generar un dataset unificado, consolidando únicamente los registros coincidentes para un análisis más preciso.

Una vez consolidado el conjunto de datos, se lleva a cabo un análisis multidimensional enfocado en responder a las siguientes preguntas de investigación:

1. ¿Existe una relación entre la magnitud absoluta (brillo) y el diámetro estimado de los asteroides?

2. ¿Cómo interactúan las variables de tamaño, velocidad y distancia mínima de aproximación en los NEOs?

3. ¿Cuáles son las trayectorias de los cinco asteroides con mayor diámetro registrado?

El proyecto procesa los resultados y utiliza diferentes técnicas de graficación para una clara interpretación de los resultados.

## Estructura del repositorio

```text
├── data/
│   ├── crudo/               # Archivos fuente sin procesar
│   └── procesado/           # Datasets listos para el análisis
├── resultados/              # Salidas gráficas del análisis
└── src/                     # Código fuente del proyecto
    ├── analisis/            # Scripts para el procesamiento y graficación
    │   ├── brillo_vs_tamanho.py
    │   ├── distancia_vs_velocidad.py
    │   └── trayectorias.py
    ├── extraccion/          # Scripts de carga de datos vía API
    │   ├── carga1.py
    │   └── carga2.py
    └── transformacion/      # Scripts para la unión de los datasets crudos
        └── unión.py
```
dsdsdsd