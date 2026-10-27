# Verificación de la actualización del mapa mundial
Fecha: 27/10/2026. Alcance: el prototipo y la documentación de su nueva navegación.

## Pruebas realizadas
- JavaScript del HTML analizado por Node sin errores de sintaxis.
- Cuatro identificadores únicos, tres objetivos por nivel y coordenadas dentro del dominio de la proyección.
- Pruebas de lógica: inicio con solo Florida disponible; rechazo de completar una parada bloqueada; desbloqueo secuencial; repetir una parada no duplica piezas; progreso alterado/no secuencial se normaliza; serialización y recuperación del progreso.
- Navegador real, HTTP local: Bahamas bloqueada antes de completar Florida.
- Recorrido de las cuatro paradas, los doce objetivos y las cuatro piezas usando los controles de la interfaz y el modo presentación. Comprobados los estados 1/4, 2/4, 3/4 y 4/4 y el final «LA RADIO RESPONDE».
- Interacción lejos del objetivo rechazada sin recogerlo.
- Mapa en mitad de una misión: pausa y continuación del objetivo ya recogido.
- Recarga: se conserva el estado 4/4 de paradas completadas.
- Nueva travesía: cancelar conserva 4/4; confirmar vuelve a 0/4 y Florida disponible.
- Movimiento por teclado observado por cambio de distancia al objetivo; controles móviles INVESTIGAR y SONAR comprobados.
- Diseño observado a 1366 px y comprobado a 390 px: sin desbordamiento horizontal, cuatro marcadores y controles móviles presentes.
- Diálogos sobre el mapa, con foco en su botón. Controles del fondo inertes al abrir mapa o diálogo.
- Sin errores o advertencias de aplicación en la consola durante las pruebas registradas.
- Sin dependencias externas en ejecución: estilos, datos, geometría cartográfica y código integrados en el HTML.

## Límites de la verificación
La campaña completa se recorrió con el atajo explícito de presentación; no se afirma una travesía manual completa ni una prueba de equilibrio de dificultad. No se forzó la destrucción del casco en la prueba de interfaz. La política del navegador de pruebas bloquea el protocolo file://: la apertura por doble clic no pudo comprobarse allí y no se sorteó esa restricción. La prueba funcional se realizó con el mismo HTML servido por HTTP local. El guardado en navegadores con almacenamiento bloqueado tiene una alternativa en memoria, cuya captura de excepción se revisó en el código.

No se ha recalculado el análisis GSAF ni se ha validado nuevamente el contenido de los documentos originales. La actualización no convierte frecuencias documentadas en riesgos individuales.

## Integridad del paquete
Se comparan los bytes de todos los archivos originales con los del ZIP recibido. Se reemplazan el HTML de juego, los dos avisos de lectura de la raíz y, en esta actualización, el guion de exposición. Las incorporaciones son el acceso al juego, la guía actual, captura del mapa, este informe y pruebas de lógica. El manifiesto adjunto enumera las huellas de los archivos preservados.

## Actualización del guion por diapositiva
Se han revisado visualmente las nueve diapositivas del PDF de presentación y preparado un bloque oral específico para cada una. Se conserva el reparto: Edvaldo 1; Jose 2-3; Alejandro 4-5; Jordi 6-8; Adriana 9. Los tiempos suman 180 segundos orientativos y requieren ensayo. El texto oral tiene 366 palabras, sin contar las indicaciones de cambio que no se leen. PDF de tres páginas renderizado y revisado sin cortes ni superposiciones. Presentación y juego no se han modificado en esta revisión del guion.
