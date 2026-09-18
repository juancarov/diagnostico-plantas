# Diagnóstico de Plantas

Dada una medición (humedad, luz, temperatura) y una especie, determina
el estado de la planta. Backend en capas (dominio / aplicación /
infraestructura / presentación) + front estático que consume la API.

## Alcance

Entra: API, lógica de diagnóstico, tabla de especies, front, pruebas
del dominio. No entra: hardware/ESP32 real, usuarios, histórico,
gamificación, móvil, nube.

## Estructura

```
diagnostico-plantas/
├── servidor/
│   ├── dominio/            # especie.py, entidades.py, puertos.py, excepciones.py, evaluador.py, servicio_diagnostico.py
│   ├── aplicacion/         # diagnosticar_planta.py, listar_especies.py
│   ├── infraestructura/    # csv_repositorio_especies.py, especies.csv, aplicacion_flask.py
│   ├── presentacion/       # dtos.py, controladores.py
│   ├── pruebas/
│   ├── ejecutar.py
│   └── requirements.txt
├── interfaz/                # index.html, estilo.css, logica.js
├── utilidades/               # preparar_especies_csv.py, traducir_nombres_comunes.py, probar_con_lecturas_sensor.py
└── datos_originales/         # floradb_houseplants_care.csv, plantas_interior_iot_ai.xlsx, lecturas_sensor_iot_salud.csv
```

## Correr el servidor

```bash
cd servidor
pip install -r requirements.txt
python ejecutar.py
```

- `POST /api/v1/diagnosticos` — `{ "especie", "humedad", "luz", "temperatura" }`
- `GET /api/v1/especies` — catálogo con nombre común y rangos

## Correr la interfaz

```bash
cd interfaz
python -m http.server 8080
```

Abre `http://127.0.0.1:8080/index.html`. Si el servidor corre en otro
puerto, ajusta `API_BASE` en `logica.js`.

## Correr las pruebas

```bash
cd servidor
python -m unittest discover -s pruebas -t . -p "prueba_*.py" -v
```

(el flag `-p` hace falta porque los archivos se llaman `prueba_*.py`,
no `test_*.py`)

## Datos

`especies.csv` (69 especies) sale de **FloraDB Houseplants Care**
(Hugging Face, CC-BY-NC-4.0, nombres verificados contra GBIF):
https://huggingface.co/datasets/Ichlibitiche/floradb-houseplants-care-sample.
Luz y temperatura vienen ya como rangos numéricos de la fuente; la
humedad no (solo trae un valor ideal), así que se le arma una banda de
±10 puntos — la única cifra que este proyecto agrega por su cuenta.
Ojo: los rangos de luz/temperatura de la fuente son por categoría
("Bright Indirect" → un rango fijo), no medidos planta por planta.

`plantas_interior_iot_ai.xlsx` es el primer dataset que se probó y se
descartó (niveles sin unidad definida); queda como evidencia, sin uso
en el código.

`lecturas_sensor_iot_salud.csv` no sirve para la tabla de especies (no
trae nombres de especie, y solo la humedad se relaciona con el estrés
en ese dataset) — se usa para probar la API con datos reales en
`utilidades/probar_con_lecturas_sensor.py`.


