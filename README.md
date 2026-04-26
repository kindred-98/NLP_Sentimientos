# NLP_Sentimientos

![CI](https://github.com/kindred-98/NLP_Sentimientos/workflows/CI%20Pipeline%20-%20Analisis%20de%20Sentimiento/badge.svg)

Proyecto Python para refactorizar un analizador de sentimientos con IA a una estructura modular, testeable y preparada para integracion continua.

## Descripcion

El proyecto parte de un script heredado y lo transforma en una aplicacion organizada por responsabilidades:

- `src/sentimiento`: analisis de sentimiento por niveles y por lotes
- `src/almacenamiento`: persistencia y lectura de resultados
- `tests/`: pruebas unitarias del analizador y del almacenamiento
- `.github/workflows/ci.yml`: pipeline de validacion automatica

El material heredado y la documentacion tecnica se conservan en `docs/`.

## Requisitos

- Python 3.12+
- Clave de API de OpenAI (`OPENAI_API_KEY`)

## Instalacion

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Crear un archivo `.env` en la raiz del proyecto:

```
OPENAI_API_KEY=tu-clave-api-aqui
```

## Uso

### CLI

Analizar un texto directamente desde terminal:

```bash
python main.py "El producto llego rapido, pero la calidad no es la esperada."
```

Modo interactivo:

```bash
python main.py
```

Guardar resultado tras el analisis:

```bash
python main.py -g "Me encanta este producto"
```

Listar el historial de analisis:

```bash
python main.py -l
```

Mas opciones:

```bash
python main.py --help
```

### Como modulo

```python
from sentimiento.analizador import analizar_texto
from almacenamiento.guardar import guardar_resultado

texto = "El producto llego rapido, pero la calidad no es la esperada."
resultado = analizar_texto(texto)
rutas = guardar_resultado(texto, resultado)
print(rutas)
```

## Estructura del proyecto

```
NLP_Sentimientos/
├── docs/
│   ├── CodigoHeredado/
│   ├── almacenamiento.md
│   ├── api_referencia.md
│   └── arquitectura.md
├── src/
│   ├── almacenamiento/
│   │   ├── guardar.py
│   │   └── leer.py
│   ├── resultados/
│   │   ├── json/
│   │   └── txt/
│   └── sentimiento/
│       ├── analizador.py
│       ├── cliente.py
│       ├── multitexto.py
│       └── niveles.py
├── tests/
│   ├── conftest.py
│   ├── test_almacenamiento.py
│   ├── test_analizador.py
│   └── test_cliente.py
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

Los resultados se guardan en:

- `src/resultados/txt/` para salida legible por personas
- `src/resultados/json/` para salida estructurada y reutilizable

Cada guardado genera un nombre con timestamp, por ejemplo:

```
analisis_2026-04-27_000048.txt
analisis_2026-04-27_000048.json
```

Las rutas pueden personalizarse via variables de entorno:

```bash
export NLP_RESULTADOS_TXT=/ruta/custom/txt
export NLP_RESULTADOS_JSON=/ruta/custom/json
```

## Tests

```bash
PYTHONPATH=src pytest -q -p no:cacheprovider
```

O usando el script del README:

```bash
set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
set PYTHONPATH=src
pytest -q -p no:cacheprovider
```

## Pipeline CI

El workflow de GitHub Actions ejecuta:

- instalacion de dependencias
- verificacion de formato con `ruff format`
- lint con `ruff`
- tests unitarios
- cobertura con `pytest-cov`
- generacion de badge de coverage
- verificacion de carpetas requeridas
- analisis de seguridad con `bandit`

## Contribucion

1. Haz un fork del repositorio
2. Crea una rama para tu funcionalidad (`git checkout -b feature/mi-feature`)
3. Commit con mensaje semantico (`git commit -m "feat(scope): descripcion"`)
4. Push a la rama (`git push origin feature/mi-feature`)
5. Abre un Pull Request

## Commits semanticos

El proyecto sigue la convencion [Conventional Commits](https://www.conventionalcommits.org/):

- `chore(project)`: estructura inicial, configuracion
- `refactor(sentiment)`: modularizacion del codigo heredado
- `feat(storage)`: implementacion de persistencia
- `test(sentiment)`: anadido de tests
- `ci(pipeline)`: configuracion de CI
- `docs(project)`: documentacion tecnica
- `feat(gui)`: interfaz grafica con Tkinter
- `fix(bug)`: correccion de errores
- `perf(core)`: mejora de rendimiento

## Estado del proyecto

Fases completadas:

1. Estructura base del proyecto
2. Modularizacion del codigo heredado
3. Persistencia en TXT y JSON
4. Tests unitarios
5. Pipeline de CI
6. Documentacion tecnica

Pendiente:

- Interfaz grafica con Tkinter

## Licencia

MIT