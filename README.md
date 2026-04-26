# NLP_Sentimientos

Proyecto Python para refactorizar un analizador de sentimientos con IA a una estructura modular, testeable y preparada para integracion continua.

## Descripcion

El proyecto parte de un script heredado y lo transforma en una aplicacion organizada por responsabilidades:

- `src/sentimiento`: analisis de sentimiento por niveles y por lotes
- `src/almacenamiento`: persistencia y lectura de resultados
- `tests`: pruebas unitarias del analizador y del almacenamiento
- `.github/workflows/ci.yml`: pipeline de validacion automatica

El material heredado y la documentacion tecnica se conservan en `docs/`.

## Instalacion

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Uso

El punto de entrada actual es `main.py`, que deja preparado el proyecto y la carga del analizador modular.

Para trabajar desde codigo, el flujo principal es:

```python
from sentimiento.analizador import analizar_texto
from almacenamiento.guardar import guardar_resultado

texto = "El producto llego rapido, pero la calidad no es la esperada."
resultado = analizar_texto(texto)
rutas = guardar_resultado(texto, resultado)
print(rutas)
```

Si ejecutas con imports desde raiz, recuerda exponer `src` en `PYTHONPATH`.

## Estructura del proyecto

```text
NLP_Sentimientos/
├── docs/
│   ├── CodigoHeredado/
│   ├── almacenamiento.md
│   ├── api_referencia.md
│   └── arquitectura.md
├── src/
│   ├── almacenamiento/
│   ├── resultados/
│   │   ├── json/
│   │   └── txt/
│   └── sentimiento/
├── tests/
│   ├── conftest.py
│   ├── test_almacenamiento.py
│   └── test_analizador.py
├── scripts/
│   └── check_folders.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── main.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Almacenamiento de resultados

Los resultados del analisis se guardan en:

- `src/resultados/txt/` para salida legible por personas
- `src/resultados/json/` para salida estructurada y reutilizable

Cada guardado genera un nombre con timestamp, por ejemplo:

```text
analisis_2026-04-27_000048.txt
analisis_2026-04-27_000048.json
```

## Tests

```bash
set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
set PYTHONPATH=src
pytest -q -p no:cacheprovider
```

## Pipeline CI

El workflow de GitHub Actions ejecuta:

- instalacion de dependencias
- lint con `ruff`
- tests unitarios
- cobertura con `pytest-cov`
- verificacion de carpetas requeridas
- analisis de seguridad con `bandit`

## Estado actual

Fases completadas hasta ahora:

1. Estructura base del proyecto
2. Modularizacion del codigo heredado
3. Persistencia en TXT y JSON
4. Tests unitarios
5. Pipeline de CI

Pendiente principal:

- interfaz grafica con Tkinter
