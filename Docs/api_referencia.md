# API Referencia

## Modulo `sentimiento.cliente`

### `get_client()`

Devuelve una instancia reutilizable del cliente de OpenAI.

Errores esperados:

- `RuntimeError` si falta `OPENAI_API_KEY`

## Modulo `sentimiento.niveles`

### `analizar_sentimiento_basico(texto: str) -> dict`

Realiza un analisis basico y devuelve una categoria simple de sentimiento.

### `analizar_sentimiento_intermedio(texto: str) -> dict`

Realiza un analisis intermedio y devuelve sentimiento, polaridad, emociones e intensidad.

Si la respuesta no es JSON valido, devuelve un diccionario con clave `error`.

### `analizar_sentimiento_avanzado(texto: str) -> dict`

Realiza un analisis avanzado con justificacion, fragmentos, tonalidad y recomendacion.

Si la respuesta no es JSON valido, devuelve un diccionario con clave `error`.

## Modulo `sentimiento.analizador`

### `analizar_texto(texto: str) -> dict`

Orquesta el analisis completo y devuelve:

- `texto`
- `basico`
- `intermedio`
- `avanzado`

## Modulo `sentimiento.multitexto`

### `analizar_sentimiento_multitexto(textos: list[str]) -> dict`

Analiza una lista de textos usando el analisis intermedio y calcula estadisticas agregadas.

Incluye:

- resultados individuales
- total de textos
- conteo de positivos, negativos y neutrales
- polaridad promedio

## Modulo `almacenamiento.guardar`

### `guardar_resultado(texto_entrada: str, resultados: dict) -> dict[str, str]`

Guarda el resultado en TXT y JSON y devuelve las rutas generadas.

Errores esperados:

- `TypeError` si el texto no es cadena
- `TypeError` si `resultados` no es diccionario

## Modulo `almacenamiento.leer`

### `listar_analisis() -> list[str]`

Lista los nombres de archivos JSON guardados.

### `leer_json(nombre: str) -> dict`

Lee y parsea un analisis JSON por nombre de archivo.

### `leer_txt(nombre: str) -> str`

Lee un analisis TXT por nombre de archivo.

### `buscar_por_fecha(fecha: str) -> list[str]`

Filtra analisis cuyo nombre contiene la fecha indicada.
