"""Pruebas de propiedades del parser de argumentos de json2csv."""

from hypothesis import given
from hypothesis import strategies as st

from json2csv.cli import parse_args

# Un delimitador o una ruta utilizable no empieza con "-": argparse
# lo interpretaría como un flag en lugar de como un valor.
SEGMENTOS_SEGUROS = st.text(
    alphabet=st.characters(
        blacklist_categories=("Cc", "Cs"),
        blacklist_characters="-",
    ),
    min_size=1,
    max_size=8,
)

DELIMITADORES = st.sampled_from([",", ";", "\t", "|", ":", " "])


@given(delimitador=DELIMITADORES)
def test_delimitador_se_preserva(delimitador: str) -> None:
    """Cualquier delimitador válido se refleja sin alterarse."""
    args = parse_args(["-d", delimitador])
    assert args.delimiter == delimitador


@given(delimitador=SEGMENTOS_SEGUROS)
def test_delimitador_libre_se_preserva(delimitador: str) -> None:
    """Un delimitador arbitrario que no parece un flag se preserva."""
    args = parse_args(["--delimiter", delimitador])
    assert args.delimiter == delimitador


@given(
    entrada=SEGMENTOS_SEGUROS,
    salida=SEGMENTOS_SEGUROS,
)
def test_rutas_se_preservan(entrada: str, salida: str) -> None:
    """Las rutas se devuelven tal como fueron informadas."""
    args = parse_args(["-i", entrada, "-o", salida])
    assert args.input == entrada
    assert args.output == salida
