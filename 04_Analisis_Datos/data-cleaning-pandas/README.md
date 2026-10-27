# LAST TIDE — Limpieza y análisis del Global Shark Attack File

Proyecto de *data wrangling* del bootcamp de **Data Analytics de Ironhack**.
Partimos del **Global Shark Attack File (GSAF)**, un registro histórico de
incidentes documentados con tiburones, lo limpiamos con pandas y usamos los
hallazgos como material para **LAST TIDE**, un concepto de videojuego de
supervivencia marina.

> **Advertencia que atraviesa todo el proyecto.** El GSAF describe incidentes
> *documentados*. No mide exposición ni riesgo individual: no sabemos cuánta
> gente practica cada actividad ni cuántas veces entra en el agua. Todo lo que
> hay aquí es **descriptivo**; ninguna conclusión es causal.

---

## Hipótesis

| | Pregunta | Base usada | Tipo de apoyo |
|---|---|---|---|
| **H1** | ¿Qué actividades aparecen en los registros? | 7.125 | Descriptivo |
| **H2** | ¿Dónde se concentran? | 7.125 | Descriptivo |
| **H3** | ¿Qué cambia entre desenlaces mortales y no mortales? | 6.482 | Descriptivo + χ² exploratorio |
| **H4** | ¿Qué especies se identifican? | 6.573 | Descriptivo |

## Las tres bases (no se mezclan)

El error más fácil de cometer en este dataset es comparar cifras calculadas
sobre universos distintos. Cada hipótesis declara la suya:

```
7.125   filas originales · 23 columnas
  − 552 registros marcados como Type == "Invalid"
= 6.573 subconjunto sin Invalid                    → base de H4

7.125   filas originales
  − 643 registros con Fatal (Y/N) no concluyente (UNKNOWN)
= 6.482 casos con desenlace clasificado            → base de H3
        de los cuales: N = 4.986 no mortales · Y = 1.496 mortales
```

---

## Técnicas de limpieza aplicadas

El enunciado pide al menos cinco. Estas son las nuestras:

1. **Normalización de nombres de columna.** El GSAF trae espacios finales en el
   propio nombre de varias columnas (`'Species '`, `'Fatal (Y/N)'`, `'Sex '`).
   Sin arreglarlo, `df['Species']` lanza `KeyError` y parece que la columna no
   existe.
2. **Manipulación de cadenas y normalización de categorías** en `Activity`:
   minúsculas, espacios colapsados y corrección de erratas reales del archivo
   (`swimmingq → swimming`, `spearfishiong → spearfishing`). La auditoría de
   reglas de agrupación acabó con **130 actividades reasignadas**.
3. **Tratamiento de valores desconocidos** en `Fatal (Y/N)`: solo se aceptan
   `Y` y `N`; los valores reales `F`, `M`, `Nq`, `2017`, `"Y x 2"` y los vacíos
   pasan a `UNKNOWN` (643 registros). **El valor original se conserva.**
4. **Expresiones regulares** sobre `Species`: entradas como `"possibly"` o
   `"bull or tiger"` se marcan como **no identificadas**. No se adivina la
   especie.
5. **Normalización geográfica** de `Country`, `State` y `Location`, y
   unificación de variantes de país.
6. **Filtrado y revisión de valores especiales**: duplicados exactos, filas
   completamente vacías y el subconjunto `Invalid`.

---

## Resultados

### H1 · Actividad (sobre 7.125)

| Actividad | Registros | % |
|---|---:|---:|
| Surf y tablas | 1.162 | 16,31 % |
| Natación y baño | 1.076 | 15,10 % |
| Pesca | — | 7,2 % |
| Pesca submarina | — | 5,7 % |

Las cuatro concentran el **44,3 %** de los registros.
Frecuencia registrada **≠** probabilidad de ataque.

### H2 · Ubicación

- **66,9 %** en tres países: EE. UU., Australia y Sudáfrica *(sobre registros con país conocido)*.
- **78,3 %** en los diez primeros países.
- **18,1 %** Florida *(sobre registros con estado conocido)*.
- **6,1 %** los diez lugares más frecuentes, entre **4.569 lugares distintos**.

El país concentra; el lugar dispersa. Posible sesgo de notificación: se
registra más donde hay más cobertura documental.

### H3 · Desenlace (sobre 6.482)

Reparto de actividades **dentro** de cada desenlace. Cada columna suma 100 %.

| Actividad | No mortales (N = 4.986) | Mortales (Y = 1.496) |
|---|---:|---:|
| Surf y tablas | 28,8 % | 7,6 % |
| Natación y baño | 23,3 % | 37,0 % |
| Naufragio / caída al agua | 1,8 % | 16,2 % |

- χ² exploratorio sobre actividad: **V de Cramér = 0,385** (asociación moderada).
  Se informa del tamaño del efecto y no del p-valor: con miles de filas el
  p-valor sale significativo casi siempre.
- **Efecto de la época:** desde el año 2000 la diferencia de natación y baño
  cae de **+13,6 a +5,6 puntos**; la del surf se mantiene. Parte de la
  diferencia es histórica.

Es **composición de registros**, no probabilidad de morir. Que el surf pese
más entre los no mortales no significa que surfear sea más seguro: hay muchos
más surfistas que náufragos.

### H4 · Especies (sobre 6.573)

Solo **2.058** registros (**31,3 %**) tienen especie identificada; cerca del
**69 %** no la tiene. Entre las identificadas:

| Especie | % |
|---|---:|
| Blanco | 34 % |
| Tigre | 15 % |
| Toro | 13 % |

La especie **no falta al azar**: no se identifica por igual en los casos
mortales que en los no mortales. Por eso este reparto mide **cobertura
documental**, no peligrosidad relativa.

---

## Mayor obstáculo

Texto libre, categorías inconsistentes y **tres bases conviviendo**. Lo que
hicimos:

- Auditoría de las reglas de agrupación: **130 actividades reasignadas**.
- Prueba de sensibilidad sin `Invalid`: los `UNKNOWN` pasan de **643 a 116** y
  el reparto apenas cambia.
- Comparación por épocas, que muestra qué parte de las diferencias de desenlace
  es histórica.

**Conclusión metodológica:** las conclusiones dependen de cómo se limpia,
filtra y analiza la base. Ninguna hipótesis queda «demostrada»: hay apoyo
observacional, sin causalidad.

---

## Estructura del repositorio

```
data-cleaning-pandas/
├── README.md
├── requirements.txt
├── data/                     # el GSAF no se versiona (ver .gitignore)
├── notebooks/
│   └── shark_attacks.ipynb   # notebook principal
└── src/
    ├── cleaning.py           # limpieza; run_pipeline() es la función principal
    └── analysis.py           # EDA e hipótesis
```

## Cómo ejecutarlo

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# descarga GSAF5.xls y déjalo en data/
jupyter notebook notebooks/shark_attacks.ipynb
```

```python
from src.cleaning import run_pipeline, subset_with_outcome, subset_without_invalid
from src.analysis import activity_by_outcome, cramers_v

df = run_pipeline("data/GSAF5.xls")
tabla = activity_by_outcome(df)
```

---

## Presentación

Diapositivas: `<PEGAR AQUÍ EL ENLACE DE GOOGLE SLIDES>`

## Equipo

Adriana Rojas Rodríguez · Edvaldo · Jordi Callejo · Alejandro · Jose Galindo

## Fuente de los datos

Global Shark Attack File, Shark Research Institute. Registro de incidentes
documentados; la cobertura varía por época y por país.

## Limitaciones

- No hay denominador de exposición: no se puede calcular riesgo.
- Cobertura desigual por país y por época (sesgo de notificación).
- La especie falta en cerca del 69 % de los registros, y no al azar.
- Todas las asociaciones son exploratorias. Ninguna es causal.
