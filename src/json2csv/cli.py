"""Punto de entrada de línea de comandos de json2csv."""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from json2csv.conversor import convertir

DESCRIPCION = "Conversor de archivos JSON a CSV con estrategia de filtro."


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Construye el parser de argumentos de la CLI.

    Args:
        argv: Argumentos a procesar. Si es ``None`` se usan los de
            ``sys.argv``.

    Returns:
        El espacio de nombres con los argumentos interpretados.
    """
    parser = argparse.ArgumentParser(
        prog="json2csv",
        description=DESCRIPCION,
    )
    parser.add_argument("-i", "--input", help="Archivo JSON de entrada.")
    parser.add_argument("-o", "--output", help="Archivo CSV de salida.")
    parser.add_argument(
        "-d",
        "--delimiter",
        default=",",
        help="Delimitador del CSV de salida.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Ejecuta la CLI.

    Args:
        argv: Argumentos a procesar. Si es ``None`` se usan los de
            ``sys.argv``.

    Returns:
        El código de salida del proceso: 0 en caso de éxito y 1 si la
        entrada no es un JSON convertible.
    """
    args = parse_args(argv)
    if args.input:
        texto = Path(args.input).read_text(encoding="utf-8")
    else:
        try:
            texto = sys.stdin.read()
        except OSError:
            texto = ""
    if not texto.strip():
        return 0
    try:
        resultado = convertir(texto, args.delimiter)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    if args.output:
        with Path(args.output).open(
            "w", encoding="utf-8", newline=""
        ) as archivo:
            archivo.write(resultado)
    else:
        sys.stdout.write(resultado)
    return 0


if __name__ == "__main__":
    sys.exit(main())
