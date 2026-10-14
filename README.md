# json2csv

Conversor de archivos JSON a CSV con estrategia de filtro.

`json2csv` lee un documento JSON y lo aplana a filas CSV usando un
delimitador configurable (coma por defecto). Acepta entrada por
argumento o por entrada estándar, y escribe el resultado a un archivo o a
salida estándar.

TP11 — Gestión de Calidad, Ingeniería de Software II (FCYT — UADER).

## Estado

La conversión de JSON a CSV está implementada con estrategia de filtros
(pipe-and-filter) en `src/json2csv/conversor.py` y cableada en la CLI.
El repositorio cuenta con ambiente virtual, calidad estática (ruff, black,
pycodestyle, pydocstyle, mypy, pyright), pruebas con Pytest e Hypothesis,
auditoría con bandit y pipeline de CI/CD completo con documentación
automática vía pdoc.

## Requisitos

- Python 3.12 o superior.

## Instalación

El proyecto se desarrolla siempre dentro de un entorno virtual:

```bash
python -m venv .venv
. .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

```bash
python json2csv.py {-i input.txt} {-o output.txt} {-d delimitador}
```

- Sin `-i`, el JSON se lee de la entrada estándar.
- Sin `-o`, el CSV se escribe en la salida estándar.
- Sin `-d`, el delimitador es la coma.

## Estructura del proyecto

```
.
├── .github/workflows/ci.yml       # pipeline de CI/CD de este repo
├── src/json2csv/                  # código del paquete
├── tests/                         # pruebas unitarias y de propiedades
├── pyproject.toml                 # configuración de herramientas
├── requirements.txt               # dependencias
├── .python-version                # versión de Python
├── VERSION                        # versión del proyecto
└── BUILD                          # número de build
```

## Calidad y CI

Cada push y cada pull request hacia `main` o `develop` ejecutan cinco jobs:

| Job | Qué verifica |
| :--- | :--- |
| `lint` | `ruff`, `black`, `pycodestyle` (PEP 8), `pydocstyle` (PEP 257), `mypy` y `pyright` |
| `security` | Auditoría con `bandit` |
| `tests` | `pytest` con cobertura mínima del 85 % |
| `update-build` | Incrementa `BUILD` de forma automática |
| `docs` | Genera la documentación con `pdoc` |

## Documentación

La documentación de los módulos se genera con `pdoc`:

```bash
PYTHONPATH=src pdoc json2csv -o docs/_build/html
```

## Licencia

MIT. Ver [LICENSE](LICENSE).
