# Almacenamiento

## Objetivo

El sistema de almacenamiento conserva cada analisis en dos formatos:

- `TXT` para lectura humana
- `JSON` para integracion con otros sistemas o futuras interfaces

## Ubicacion

Los resultados se guardan en:

- `src/resultados/txt/`
- `src/resultados/json/`

## Comportamiento del guardado

La funcion `guardar_resultado()`:

1. crea las carpetas si no existen
2. genera un nombre unico con timestamp
3. escribe un archivo `.txt`
4. escribe un archivo `.json`
5. devuelve las rutas creadas

Ejemplo de nombre:

```text
analisis_2026-04-27_000048.txt
analisis_2026-04-27_000048.json
```

## Formato TXT

El TXT contiene:

- cabecera con fecha y hora
- texto analizado
- resumen del resultado basico
- resumen del resultado intermedio
- justificacion del resultado avanzado

## Formato JSON

El JSON contiene una estructura preparada para consumo programatico:

```json
{
  "timestamp": "2026-04-27 00:00:48",
  "texto": "El producto llego rapido, pero la calidad no es la esperada.",
  "basico": {},
  "intermedio": {},
  "avanzado": {}
}
```

## Lectura del historial

El modulo `leer.py` permite:

- listar analisis guardados
- leer un archivo JSON por nombre
- leer un archivo TXT por nombre
- buscar analisis por fecha

## Consideraciones

- los archivos no se sobrescriben porque el nombre incluye timestamp
- los resultados generados estan ignorados en Git mediante `.gitignore`
- esta capa es independiente del proveedor de IA y de la interfaz
