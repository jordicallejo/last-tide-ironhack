# LAST TIDE · Mapa mundial y niveles
Actualización: 27 de octubre de 2026.

## Abrir
1. Extraer todo el ZIP en una carpeta normal.
2. Abrir `00_ABRIR_JUEGO.html` y pulsar el enlace, o abrir directamente `03_Videojuego/LAST_TIDE_Juego.html` en un navegador moderno.
3. Seleccionar Florida e iniciar la parada.

El juego contiene su mapa, estilos y código dentro del mismo HTML. No solicita fuentes, mapas ni servicios externos durante la partida. En la verificación se ha probado mediante un servidor HTTP local; la política del navegador de pruebas no permite abrir URLs file://, de modo que no se afirma una prueba directa por doble clic. Si el navegador local restringe archivos, puede servirse la carpeta con `python -m http.server 8000` y abrir http://localhost:8000/03_Videojuego/LAST_TIDE_Juego.html desde la raíz del proyecto.

## La petición de Adriana
El selector es un mapa mundial con cuatro paradas en regiones analizadas:

| Orden | Parada | Referencia regional aproximada | Pieza |
|---|---|---|---|
| 1 | Florida, EE. UU. | Costa de Volusia | Batería de navegación |
| 2 | Bahamas | Nassau como referencia cartográfica | Filtro de combustible |
| 3 | Sudáfrica | KwaZulu-Natal, referencia Durban | Antena de largo alcance |
| 4 | Australia | Nueva Gales del Sur, referencia Sydney | Módulo de radio |

Cada parada contiene tres objetivos con texto, temática y pieza propios. La siguiente se abre solo al recoger los tres objetivos y confirmar la pieza con E. Los marcadores del mapa y las tarjetas permiten seleccionar la parada. Las bloqueadas se pueden consultar, pero no iniciar. Las completadas se pueden revisitar sin duplicar piezas.

## Controles
- WASD o flechas: mover la embarcación.
- E: investigar un objetivo cercano. Tras recoger los tres, E instala la pieza.
- Espacio: sonar visual.
- M o botón MAPA MUNDIAL: pausar y volver al mapa. CONTINUAR PARADA retoma el estado en memoria.
- R: confirmar que se quiere reintentar la parada.
- Pantallas pequeñas: flechas táctiles, INVESTIGAR y SONAR.

El casco puede dañarse por proximidad a una silueta. Es una regla de ficción independiente de la especie y de las tasas históricas. Al agotar el casco se ofrece reintentar la parada. El mapa y los diálogos pausan el daño y el movimiento.

## Demostración rápida
Activar «Modo presentación» en el mapa antes de iniciar una parada. En la misión aparece «DEMO · ACERCAR AL OBJETIVO»; acerca el barco, pero NO recoge el objetivo ni desbloquea niveles. Después pulsar E, leer y continuar. Repetir tres veces y pulsar E una vez más para instalar la pieza. Así puede recorrerse toda la campaña sin invertir tiempo en desplazamientos. Las teclas 1/2/3 solo acercan a los objetivos con ese modo activado.

## Guardado
Se guardan las paradas completadas en localStorage del navegador. No se guarda una misión a medias al cerrar o recargar: el estado parcial se conserva solo mientras la pestaña siga abierta. Si el navegador impide guardar, se indica en pantalla y puede jugarse en memoria. Una partida de localhost, otro navegador o un archivo en otra ruta puede tener un almacenamiento diferente. NUEVA TRAVESÍA pide confirmar y permite cancelar.

## Rigor de los lugares
- Florida: 18,08 % de registros con estado conocido según `outputs/h2_geografia.csv` incluido.
- EE. UU., Australia y Sudáfrica: 66,91 % de registros con país conocido según esa misma salida.
- Bahamas se añade por su interés en los contextos de H2/H4 del grupo. El 74,6 % comunicado utiliza un subconjunto de países y actividades; no se interpreta como porcentaje de todos los incidentes de Bahamas.
- Volusia, Nassau, Durban y Sydney sirven para situar referencias regionales. No son coordenadas de incidentes individuales ni cuatro máximos geográficos demostrados.
- La ubicación y el orden de los niveles son decisiones narrativas, no una clasificación de riesgo. Las rutas son esquemáticas, no rutas navegables reales.
- Cada tarjeta explica qué hipótesis inspira su parada. H3 aporta desenlace e incertidumbre; no asigna daño por especie ni convierte porcentajes en probabilidades de muerte.

## Alcance del prototipo
Se ha implementado navegación cenital, objetivos, sonar visual, casco, diálogos, mapa, piezas, bloqueos y progreso. Las cinco actividades inspiran el texto y los objetivos; no se ha implementado un simulador independiente de surf, natación, pesca ni buceo. El concepto narrativo de primera persona, oxígeno, hambre, inventario limitado y álbum completo sigue siendo una propuesta, no funcionalidad de esta demo.

La presentación PDF/PPTX y sus imágenes se conservan sin cambios. El guion de exposición está actualizado y separado por las nueve diapositivas. El PDF del guion de demostración corresponde a la demo previa; para enseñar el juego actual usar esta guía. El análisis de datos del ZIP tampoco se ha alterado ni se ha recalculado como parte de este cambio del juego.

## Cartografía
Natural Earth, tierra a escala 1:110m, dominio público. Proyección equirectangular integrada como SVG en el HTML.
Fuente: https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_110m_land.geojson
Las rutas y etiquetas han sido creadas para la demo. No se solicitan teselas ni claves de mapas.
