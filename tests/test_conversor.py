"""Pruebas del núcleo de conversión JSON a CSV."""

from pathlib import Path

import pytest
from _pytest.capture import CaptureFixture
from _pytest.monkeypatch import MonkeyPatch

from json2csv.cli import main
from json2csv.conversor import (
    convertir,
    filtro_decodificador,
    filtro_encabezados,
)


def test_convierte_lista_de_objetos() -> None:
    """Una lista de objetos produce encabezados más filas."""
    texto = '[{"a": 1, "b": 2}, {"a": 3, "b": 4}]'
    assert convertir(texto) == "a,b\r\n1,2\r\n3,4\r\n"


def test_convierte_objeto_unico() -> None:
    """Un objeto solo se trata como lista de un registro."""
    assert convertir('{"a": 1}') == "a\r\n1\r\n"


def test_delimitador_personalizado() -> None:
    """El delimitador informado reemplaza a la coma."""
    assert convertir('{"a": 1, "b": 2}', ";") == "a;b\r\n1;2\r\n"


def test_json_invalido_lanza_error() -> None:
    """Un texto que no es JSON produce ``ValueError``."""
    with pytest.raises(ValueError, match="JSON inválido"):
        convertir("no es json")


def test_json_no_objetos_lanza_error() -> None:
    """Un JSON que no contiene objetos produce ``ValueError``."""
    with pytest.raises(ValueError, match="objeto o una lista"):
        convertir("[1, 2, 3]")


def test_encabezados_preservan_orden() -> None:
    """Las claves nuevas aparecen como columnas al final."""
    registros = [{"a": 1}, {"b": 2, "a": 3}]
    assert filtro_encabezados(registros) == ["a", "b"]


def test_registro_con_claves_faltantes() -> None:
    """Una clave ausente se serializa como campo vacío."""
    texto = '[{"a": 1}, {"a": 2, "b": 3}]'
    assert convertir(texto) == "a,b\r\n1,\r\n2,3\r\n"


def test_decodificador_acepta_lista_vacia() -> None:
    """Una lista vacía decodifica a cero registros."""
    assert filtro_decodificador("[]") == []


def test_main_archivos(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    """Con ``-i`` y ``-o`` se lee y escribe en archivos."""
    entrada = tmp_path / "entrada.json"
    salida = tmp_path / "salida.csv"
    entrada.write_text('[{"a": 1}]')
    assert main(["-i", str(entrada), "-o", str(salida), "-d", ";"]) == 0
    assert salida.read_text() == "a\n1\n"


def test_main_estandar(
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
    tmp_path: Path,
) -> None:
    """Sin ``-i``/``-o`` se usan entrada y salida estándar."""
    import io

    monkeypatch.setattr("sys.stdin", io.StringIO('[{"a": 1}]'))
    assert main([]) == 0
    assert capsys.readouterr().out == "a\r\n1\r\n"


def test_main_entrada_vacia(capsys: CaptureFixture[str]) -> None:
    """Entrada estándar vacía termina con éxito sin salida."""
    assert main([]) == 0
    assert capsys.readouterr().out == ""


def test_main_error_json(
    monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]
) -> None:
    """Un JSON inválido devuelve código 1 y aviso por stderr."""
    import io

    monkeypatch.setattr("sys.stdin", io.StringIO("no json"))
    assert main([]) == 1
    assert "JSON inválido" in capsys.readouterr().err
