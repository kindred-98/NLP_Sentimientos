# NLP_Sentimientos

Proyecto base para refactorizar un analizador de sentimientos con IA a una estructura profesional, modular y testeable.

## Estado actual

Esta fase deja preparado el esqueleto del proyecto para desarrollar:

- modularizacion del analizador
- persistencia de resultados en TXT y JSON
- tests unitarios
- pipeline CI/CD
- interfaz grafica con Tkinter

## Estructura del proyecto

```text
NLP_Sentimientos/
├── Docs/
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
├── main.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Siguientes fases

1. Refactorizar el codigo heredado en modulos.
2. Implementar almacenamiento de resultados.
3. Añadir tests y automatizacion.
4. Construir la interfaz final.
