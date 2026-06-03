# Observaciones astronómicas
| Autor | Contacto |
| :--- | :--- |
| **Lina Nicole Reyes Nava** | linareyes@ciencias.unam.mx  |
| **Rodrigo García Peláez** | rodrigo090703@ciencias.unam.mx |

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
│   ├── crudo/                        # Archivos fuente sin procesar
│   └── procesado/                    # Datasets limpios para el análisis
├── resultados/                       # Salidas gráficas
└── src/                              # Código fuente del proyecto
    ├── analisis/                     # Scripts dedicados al estudio de datos
    │   ├── brillo_vs_tamanho.py      # Relación brillo - diámetro
    │   ├── distancia_vs_velocidad.py # Relación distancia - velocidad - diámetro
    │   └── trayectorias.py           # Modelado de trayectorias de los 5 asteroides de mayor diámetro
    ├── extraccion/                   # Módulos de carga de datos
    │   ├── carga1.py                 # Extracción de datos de NeoWs API
    │   └── carga2.py                 # Extracción de datos de Small-Body DB
    └── transformacion/               # Lógica de procesamiento
        └── unión.py                  # Script principal de unificación
```

## Fuentes de datos
| Fuente | URL | Descripción |
| :--- | :--- | :--- |
| **NeoWs (API)** | [apify.com](https://apify.com/compute-edge/nasa-neo-scraper) | Provee datos cinemáticos, incluyendo velocidad relativa y distancia a la Tierra y fechas de observación. También contiene clasificaciones de riesgo. |
| **Small-Body DB** | [ssd.jpl.nasa.gov](https://ssd.jpl.nasa.gov/tools/sbdb_query.html#!#results) | Repositorio con propiedades físicas del asteroide como diámetro y magnitud absoluta, excentricidad, etc. Además contiene datos de observaciones. |


