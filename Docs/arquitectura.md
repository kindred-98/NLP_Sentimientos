# Arquitectura

## Objetivo

La arquitectura del proyecto separa el analisis de sentimiento, la persistencia de resultados y la capa de pruebas para evitar el acoplamiento del script heredado original.

## Estructura general

```text
main.py
  |
  v
src/sentimiento/analizador.py
  |
  +--> src/sentimiento/niveles.py
  |      |
  |      +--> src/sentimiento/cliente.py
  |
  +--> src/sentimiento/multitexto.py

src/almacenamiento/guardar.py
src/almacenamiento/leer.py
```

## Responsabilidades

- `main.py`: punto de entrada actual del proyecto.
- `src/sentimiento/cliente.py`: crea y reutiliza el cliente de OpenAI.
- `src/sentimiento/niveles.py`: implementa el analisis basico, intermedio y avanzado.
- `src/sentimiento/analizador.py`: orquesta el analisis completo de un texto.
- `src/sentimiento/multitexto.py`: agrega analisis de varios textos y calcula estadisticas.
- `src/almacenamiento/guardar.py`: guarda resultados en TXT y JSON.
- `src/almacenamiento/leer.py`: consulta el historial persistido.
- `tests/`: valida comportamiento funcional y persistencia.

## Flujo de datos

1. Un texto entra por `main.py` o por futuras capas superiores como la GUI.
2. `analizador.py` delega el trabajo en los niveles de analisis.
3. `niveles.py` usa `cliente.py` para comunicarse con OpenAI.
4. El resultado compuesto puede enviarse a `guardar.py`.
5. El historial puede recuperarse con `leer.py`.

## Ventajas frente al codigo heredado

- separacion clara de responsabilidades
- cliente OpenAI centralizado
- analisis reutilizable desde varias interfaces
- persistencia desacoplada del analisis
- testing mas sencillo mediante mocks y funciones pequeñas
