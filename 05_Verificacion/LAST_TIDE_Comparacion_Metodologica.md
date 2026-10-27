# Informe de ejecución y contraste — 26/10/2026

## Fuente real procesada

`GSAF5 (1).xlsx` localizado entre los archivos del proyecto. **7.125 × 23**. La ejecución no depende de cifras copiadas de una presentación.

## Resultados comprobados directamente

- 7.125 filas originales y 23 columnas.
- `Type == Invalid`: **552** → conjunto sin Invalid **6.573**.
- `Fatal Y/N`, tras `strip` y conversión a mayúsculas: **N = 4.986, Y = 1.496, UNKNOWN = 643**. Con desenlace conocido **6.482**.
- Países EE. UU. + Australia + Sudáfrica: **66,91 %** de los registros con país conocido, y los diez primeros **78,26 %**.
- Florida, entre estados conocidos: **18,08 %**.
- Diez localizaciones más frecuentes **6,12 %**. **La normalización implementada da 4.593 lugares distintos**, no los 4.569 indicados en Claude, por reglas de unificación diferentes.

## Diferencias que impiden validar la presentación de Claude con estas reglas

- H1: las reglas de grupo aquí son de palabras clave; generan **surf y tablas 1.721 / 24,15 %**, y **natación y baño 1.676 / 23,52 %**. Claude declaraba 1.162 / 16,31 % y 1.076 / 15,10 %. Estos dos últimos valores sí corresponden a formas normalizadas de `Activity_clean`, **no al grupo amplio**. No se deben mezclar ambas definiciones.
- H3: los porcentajes por actividad y V de Cramér **dependen de la agrupación utilizada**. Con nuestras reglas, V = **0,331**, no 0,385. No trasladar un V calculado con una categorización al gráfico elaborado con otra.
- H4: la clasificación restrictiva implementada encuentra **1.910 especies identificadas** (sin Invalid), no 2.058. La diferencia está en qué descripciones libres se aceptan como identificación específica. No cabe forzar la salida para igualar cifras previas.
- Las afirmaciones de 130 reasignaciones y los porcentajes por época requieren comparar reglas concretas y salidas con el notebook original de esas hipótesis. No se han reproducido aquí.

## Decisión adoptada

Mantener los originales, exportar `auditoria_limpieza.csv`, documentar las reglas y **no presentar las divergencias como errores del fichero ni como conclusiones científicas**. Son diferencias metodológicas que deben acordarse entre los cinco integrantes.

## Limitaciones y videojuego

El GSAF reúne incidentes documentados, no la población expuesta. No mide el riesgo de actividades, regiones o especies. Las pistas y encuentros en el videojuego son un mecanismo narrativo inventado.
