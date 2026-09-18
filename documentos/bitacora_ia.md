# Bitácora de uso de IA

## Qué se le pidió

Se usó un asistente de IA para armar la estructura inicial del
backend en capas (dominio/aplicación/infraestructura/presentación),
resolver dudas puntuales de SOLID mientras se escribía el código, y
para agilizar tareas mecánicas: generar los diagramas, traducir
nombres, y armar el plan de commits para el repositorio.

## Qué se revisó y se cambió

**Los datos de las especies pasaron por tres intentos.** El primero
fue un dataset con niveles de luz/temperatura del 1 al 4, sin ninguna
unidad definida — había que inventar la conversión a números, así que
se descartó. El segundo fue un CSV de lecturas de sensor con una
etiqueta de estrés; al revisarlo nos dimos cuenta de que no traía
nombres de especie y que solo la humedad se relacionaba con la
etiqueta (temperatura y luz eran prácticamente ruido), así que tampoco
sirvió como tabla de referencia — se quedó como datos de prueba para
la API. El tercero, el que se usa hoy, es el dataset FloraDB
(Hugging Face, verificado contra GBIF), que sí trae luz y temperatura
como rangos numéricos con unidad declarada; solo la humedad hubo que
estimarla con un margen propio, documentado como tal.

**Los diagramas se hicieron mal la primera vez.** La primera versión
del diagrama de paquetes tenía una flecha de "implementa" que cruzaba
por encima de una etiqueta de otro componente — al revisarlo se
corrigió la ruta para que no se cruzara con nada, y se rehicieron los
dos diagramas en draw.io para poder seguir editándolos a mano.

**El código se limpió de comentarios que sonaban a manual de clase.**
La primera versión tenía casi cada función anotada con "esto es SRP",
"esto es RA5", etc. Se decidió sacar esas etiquetas y dejar solo
comentarios cortos, del tipo que uno realmente escribiría.

**La carpeta de documentos se separó del código.** Se decidió que el
documento de arquitectura y esta bitácora no fueran parte del mismo
entregable que el código en sí, sino que se subieran aparte al
repositorio.

## Qué se aceptó tal cual

La separación en las 4 capas, los dos puertos del dominio
(`ProveedorDeEspecie` y `CatalogoDeEspecies`), y la regla de
agregación del estado global (contar parámetros fuera de rango) se
usaron como se propusieron, porque tenían sentido para el tamaño de
este proyecto.

## Qué falta revisar

El margen de ±10 puntos porcentuales para la humedad es una decisión
nuestra, no de ninguna fuente — falta confirmar si se justifica así o
si conviene buscar un respaldo mejor antes de la sustentación.
