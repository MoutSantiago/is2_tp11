"""Núcleo de conversión de JSON a CSV con estrategia de filtros.

La conversión se modela como una tubería (pipe-and-filter): cada filtro
recibe la salida del anterior y la transforma, de modo que el flujo
completo es ``texto JSON -> registros -> encabezados -> filas -> CSV``.
"""

import csv
import io
import json
from collections.abc import Iterable, Iterator
from typing import Any

Registro = dict[str, Any]


def filtro_decodificador(texto: str) -> list[Registro]:
    """Decodifica el texto JSON en una lista de registros.

    Args:
        texto: Contenido JSON. Puede ser un objeto o una lista de
            objetos.

    Returns:
        Lista de registros (diccionarios) normalizada.

    Raises:
        ValueError: Si el JSON es inválido o no contiene objetos.
    """
    try:
        datos = json.loads(texto)
    except json.JSONDecodeError as error:
        raise ValueError(f"JSON inválido: {error}") from error
    if isinstance(datos, dict):
        datos = [datos]
    if not isinstance(datos, list) or not all(
        isinstance(item, dict) for item in datos
    ):
        raise ValueError("El JSON debe ser un objeto o una lista de objetos.")
    return datos


def filtro_encabezados(registros: Iterable[Registro]) -> list[str]:
    """Extrae los encabezados preservando el orden de aparición.

    Args:
        registros: Registros de los que se toman las claves.

    Returns:
        Lista de encabezados sin duplicados.
    """
    encabezados: list[str] = []
    for registro in registros:
        for clave in registro:
            if clave not in encabezados:
                encabezados.append(clave)
    return encabezados


def filtro_formateador(
    registros: Iterable[Registro], encabezados: list[str]
) -> Iterator[list[Any]]:
    """Alinea cada registro con los encabezados produciendo filas.

    Args:
        registros: Registros a formatear.
        encabezados: Columnas del CSV de salida.

    Yields:
        Una fila por registro, con valores vacíos en claves ausentes.
    """
    for registro in registros:
        yield [registro.get(encabezado, "") for encabezado in encabezados]


def filtro_serializador(
    encabezados: list[str],
    filas: Iterable[list[Any]],
    delimitador: str,
) -> str:
    """Serializa encabezados y filas como texto CSV.

    Args:
        encabezados: Columnas del CSV.
        filas: Filas de datos ya alineadas.
        delimitador: Carácter separador de campos.

    Returns:
        El documento CSV completo.
    """
    bufer = io.StringIO()
    escritor = csv.writer(bufer, delimiter=delimitador)
    escritor.writerow(encabezados)
    escritor.writerows(filas)
    return bufer.getvalue()


def convertir(texto: str, delimitador: str = ",") -> str:
    """Convierte texto JSON a CSV encadenando los filtros.

    Args:
        texto: Contenido JSON de entrada.
        delimitador: Delimitador del CSV de salida.

    Returns:
        El documento CSV resultante.

    Raises:
        ValueError: Si la entrada no es JSON de objetos válido.
    """
    registros = filtro_decodificador(texto)
    encabezados = filtro_encabezados(registros)
    filas = filtro_formateador(registros, encabezados)
    return filtro_serializador(encabezados, filas, delimitador)
