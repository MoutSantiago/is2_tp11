# Changelog

Todas las mudanças relevantes del proyecto se registran en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y
el versionado se apoya en [Semantic Versioning](https://semver.org/lang/es/).

## [No publicado]

### Agregado

- Conversión JSON → CSV con estrategia de filtros (pipe-and-filter) en
  `src/json2csv/conversor.py`, integrada a la CLI con `-i`, `-o` y `-d`,
  entrada/salida estándar por defecto y manejo de errores (código 1 y
  mensaje por stderr ante JSON inválido).
- Pruebas de conversión y de la CLI con entrada/salida estándar y archivos.

### Corregido

- Se agregó `pydocstyle` a `requirements.txt` para que el chequeo de
  docstrings del workflow funcione con dependencias instaladas desde cero.
- Se eliminó una opción de entorno de `pytest` sin plugin asociado que
  producía una advertencia de configuración.
- Se actualizó el `README.md` con la estructura y el estado actuales del
  repositorio.

## [0.1.0] - 2026-10-09

### Agregado

- Esqueleto de proyecto generado con CookieCutter (`template/`).
- Configuración centralizada de herramientas en `pyproject.toml`:
  `ruff`, `black`, `pycodestyle`, `pydocstyle`, `mypy`, `pyright`, `pytest`
  y `coverage` (umbral de 85 %).
- `requirements.txt` con las dependencias de desarrollo y validación.
- Workflow de CI/CD (`.github/workflows/ci.yml`) con los jobs `lint`,
  `security`, `tests`, `update-build` y `docs`.
- Archivos de control `VERSION`, `BUILD`, `CHANGELOG.md` y `CONTEXT.md`.

[No publicado]: https://github.com/santiago-mout/is2_tp11/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/santiago-mout/is2_tp11/releases/tag/v0.1.0
