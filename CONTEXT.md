# Contexto para asistentes de IA

Este archivo documenta los prompts y las decisiones tomadas con ayuda de IA
para el proyecto, según el requisito de la consigna.

## Convenciones del proyecto

- Python 3.12, código en `src/`, pruebas en `tests/`.
- Línea máxima de 79 caracteres (PEP 8).
- Docstrings obligatorios en toda función, clase y módulo público
  (PEP 257, convención `pep257`).
- Tipado completo: `mypy --strict` y `pyright` deben pasar sin errores.
- La cobertura mínima es del 85 %.

## Prompt 1 — Auditoría de estructura del repositorio

> Revisá este repo contra los requisitos de estructura y configuración del
> enunciado (no el código ni la documentación de la TP). Armá una tabla
> con el estado de cada punto y marcá los que rompen el CI.

Resultado: se detectó que el workflow invocaba `requirements.txt` cuando el
archivo se llamaba `requeriments.txt`, que faltaban `pycodestyle` y
`hypothesis` en las dependencias, y que `pyproject.toml` estaba vacío.

## Prompt 2 — Saneado de configuración

> Hice un par de cambios, si podés arreglá lo demás. Montá el esqueleto de
> CookieCutter, completá `pyproject.toml`, cargá `VERSION`, `BUILD`,
> `CHANGELOG.md`, `README.md` y `CONTEXT.md`, arreglá el workflow de CI y
> agregá las dependencias faltantes.

Decisiones tomadas durante esa sesión:

- Se renombró `requeriments.txt` a `requirements.txt` para coincidir con lo
  que el workflow instala.
- Se agregaron `pycodestyle`, `hypothesis` y `cookiecutter` a las
  dependencias.
- Se excluyó `template/` de `ruff`, `black`, `pydocstyle` y `bandit`: sus
  archivos todavía contienen marcado Jinja y no son código Python válido.
- El job `docs` pasó a dispararse en cada PR, y `bandit` corre con `-lll`
  para que un hallazgo de severidad alta corte el pipeline.
- Se corrigió el paso de documentación: `pdoc` no acepta un directorio como
  spec, así que ahora es `PYTHONPATH=src pdoc <paquete> -o docs/_build/html`.

## Prompt 3 — Verificación local

> Ejecutá localmente los mismos comandos que el CI para confirmar que la
> configuración quedó consistente.

## Prompt 4 — Estructura del repositorio

> Verificá que el repositorio cumpla con los requisitos de estructura y
> configuración del enunciado, sin evaluar el código ni la documentación
> de la TP.

## Prompt 5 — El esqueleto en la raíz

> Pero queda horrible el directorio del cookiecutter dentro del repo.

Se movió el esqueleto a `template/`. Cookiecutter 2.7 no descubre plantillas
en subdirectores de forma automática: `find_template` solo mira los hijos
directos del repositorio. La salida es invocar el template con
`--directory`, de modo que el layout queda limpio pero el comando de
generación pasa a ser `cookiecutter . --directory template`.

Como efecto secundario se resolvió un problema previo: con el esqueleto en
la raíz, `ruff` trataba `{{cookiecutter.repo_name}}/pyproject.toml` como
configuración jerárquica y abortaba antes de poder excluirlo.

## Prompt 6 — Auditoría de los puntos a–u

> Verifica que todos los puntos relacionados con el repositorio (puntos del
> a al u) estén implementados, a excepción del de cookiecutter. Si falta
> alguno soluciónalo.

Resultado:

- Se comprobó la instalación desde cero con `python -m venv` y se detectó
  que `pydocstyle` se ejecuta en CI pero no figuraba en
  `requirements.txt`. Se añadió `pydocstyle==6.3.0`.
- Se eliminó la opción `env` de la configuración de `pytest`, que carecía
  de plugin instalado y provocaba una advertencia.
- Se actualizó el `README.md` para describir la estructura vigente del
  repositorio y quitar referencias obsoletas al esqueleto de CookieCutter.
