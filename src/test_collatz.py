"""Pruebas unitarias y funcionales para el módulo collatz."""

import subprocess
import sys

from collatz import collatz


# ============================================================
# TESTS UNITARIOS - CAJA BLANCA
# ============================================================
#
# T1 -> R2, R7, R8
# Verifica el caso base: el número ya es 1.
def test_T1() -> None:
    """Verificar el caso base: el número ya es 1."""
    assert collatz(1) == 0


# T2 -> R2, R4, R5, R7, R8
# Verifica el camino correspondiente a un número par.
def test_T2() -> None:
    """Verificar el camino correspondiente a un número par."""
    assert collatz(2) == 1


# T3 -> R2, R4, R6, R7, R8
# Verifica el camino correspondiente a un número impar.
def test_T3() -> None:
    """Verificar el camino correspondiente a un número impar."""
    assert collatz(3) == 7


# T4 -> R2, R4, R5, R7, R8
# Verifica más de una iteración utilizando un número par.
def test_T4() -> None:
    """Verificar más de una iteración con un número par."""
    assert collatz(4) == 2


# T5 -> R2, R4, R6, R7, R8
# Verifica un número impar cuya secuencia requiere varias iteraciones.
def test_T5() -> None:
    """Verificar un número impar de varias iteraciones."""
    assert collatz(5) == 5


# T6 -> R2, R4, R5, R6, R7, R8
# Verifica una secuencia que combina operaciones para números
# pares e impares.
def test_T6() -> None:
    """Verificar una secuencia con operaciones pares e impares."""
    assert collatz(10) == 6


# T7 -> R2, R4, R5, R6, R7, R8, R9, R10
# Corresponde al número 20 utilizado en el código original
# para comprobar los resultados.
def test_T7() -> None:
    """Verificar el número 20 utilizado en el código original."""
    assert collatz(20) == 7


# T14 -> R2, R3, R4, R5, R6, R7, R8
# Verifica el límite superior permitido: 1999.
def test_T14() -> None:
    """Verificar el límite superior permitido: 1999."""
    assert collatz(1999) == 50


# ============================================================
# TESTS FUNCIONALES - CAJA NEGRA
# ============================================================
#
# Estos casos deberían probar el comportamiento del programa
# completo: entrada, validación y salida.
#
# Como el código del PDF solo muestra la función collatz()
# y no implementa todavía la entrada por teclado ni las
# validaciones, estos tests quedan preparados para cuando
# exista la función/programa completo.


def ejecutar_programa(entrada: str) -> subprocess.CompletedProcess[str]:
    """Ejecutar el programa con la entrada indicada."""
    return subprocess.run(
        [sys.executable, "collatz.py"],
        check=False,
        input=entrada,
        text=True,
        capture_output=True,
    )


# T8 - Aceptar el máximo permitido: 1999
def test_T8() -> None:
    """Aceptar el máximo permitido: 1999."""
    resultado = ejecutar_programa("1999\n")
    assert resultado.returncode == 0
    assert "Número inicial: 1999" in resultado.stdout
    assert "Cantidad de iteraciones: 50" in resultado.stdout


# T9 - Rechazar cero
def test_T9() -> None:
    """Rechazar cero."""
    resultado = ejecutar_programa("0\n")
    assert "debe ser positivo" in resultado.stdout


# T10 - Rechazar un número negativo
def test_T10() -> None:
    """Rechazar un número negativo."""
    resultado = ejecutar_programa("-5\n")
    assert "debe ser positivo" in resultado.stdout


# T11 - Rechazar un número mayor que 1999
def test_T11() -> None:
    """Rechazar un número mayor que 1999."""
    resultado = ejecutar_programa("2000\n")
    assert "no puede ser mayor que 1999" in resultado.stdout


# T12 - Rechazar texto
def test_T12() -> None:
    """Rechazar texto."""
    resultado = ejecutar_programa("abc\n")
    assert "debe ingresar un número entero" in resultado.stdout


# T13 - Aceptar 1998
def test_T13() -> None:
    """Aceptar 1998."""
    resultado = ejecutar_programa("1998\n")
    assert resultado.returncode == 0
    assert "Número inicial: 1998" in resultado.stdout
    assert "Cantidad de iteraciones:" in resultado.stdout


# T15 - Volver a comprobar el límite superior
def test_T15() -> None:
    """Volver a comprobar el límite superior."""
    resultado = ejecutar_programa("2000\n")
    assert "no puede ser mayor que 1999" in resultado.stdout


# T16 - Rechazar -1
def test_T16() -> None:
    """Rechazar -1."""
    resultado = ejecutar_programa("-1\n")
    assert "debe ser positivo" in resultado.stdout
