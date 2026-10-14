"""Pruebas de la línea de comandos de json2csv."""

import pytest

from json2csv.cli import main, parse_args


def test_delimitador_por_defecto() -> None:
    """Sin ``-d`` el delimitador es la coma."""
    assert parse_args([]).delimiter == ","


@pytest.mark.parametrize("delimitador", [",", ";", "\t", "|"])
def test_delimitador_explicito(delimitador: str) -> None:
    """``-d`` define el delimitador de salida."""
    args = parse_args(["-d", delimitador])
    assert args.delimiter == delimitador


def test_entrada_por_defecto_es_estandar() -> None:
    """Sin ``-i`` ni ``-o`` no se fijan rutas."""
    args = parse_args([])
    assert args.input is None
    assert args.output is None


def test_rutas_explicitas() -> None:
    """``-i`` y ``-o`` se reflejan en los argumentos."""
    args = parse_args(["-i", "entrada.json", "-o", "salida.csv"])
    assert args.input == "entrada.json"
    assert args.output == "salida.csv"


def test_main_devuelve_cero() -> None:
    """``main`` retorna un código de salida exitoso."""
    assert main([]) == 0
