"""Proyección de defectos con el modelo exponencial de Musa.

Desarrolla el ejercicio propuesto en ``Taller_Defectos.ipynb``.

Modelo:

    lambda(t) = lambda0 * exp(-(lambda0 / mu0) * t)
    mu(t)     = mu0 * (1 - exp(-(lambda0 / mu0) * t))

Ajuste aproximado por regresión lineal sobre el log de la tasa:

    ln(d) = b + m * t      ->   lambda0 = exp(b),   mu0 = -lambda0 / m

donde ``d`` son los defectos instantáneos por intervalo (día / sesión).

Densidad de defectos (taller):   mu0 = S / delta   ->   S = mu0 * delta
Defectos liberados:              mu_r = mu0 - sum(mu_i)
"""

import io
import math
import sys
from collections.abc import Sequence


def _configurar_stdout() -> None:
    """Forzar la codificación UTF-8 de la salida estándar si es posible."""
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")


def mu(t: float, l0: float, mu0: float) -> float:
    """Calcular los defectos acumulados hasta el instante ``t``.

    Args:
        t: Instante (día o sesión).
        l0: Tasa inicial de defectos ``lambda0``.
        mu0: Total de defectos esperados.

    Returns:
        La cantidad de defectos acumulados ``mu(t)``.
    """
    return mu0 * (1.0 - math.exp(-(l0 / mu0) * t))


def lam(t: float, l0: float, mu0: float) -> float:
    """Calcular la tasa instantánea de defectos en el instante ``t``.

    Args:
        t: Instante (día o sesión).
        l0: Tasa inicial de defectos ``lambda0``.
        mu0: Total de defectos esperados.

    Returns:
        La tasa instantánea ``lambda(t)``.
    """
    return l0 * math.exp(-(l0 / mu0) * t)


def loglin_fit(
    t: Sequence[float], d: Sequence[float]
) -> tuple[float, float, float, float]:
    """Ajustar el modelo por regresión lineal sobre el log de la tasa.

    Args:
        t: Instantes (días o sesiones).
        d: Defectos instantáneos por intervalo.

    Returns:
        La tupla ``(lambda0, mu0, m, b)`` con ``lambda0`` y ``mu0``
        estimados y la pendiente ``m`` y ordenada ``b`` del ajuste.
    """
    pts = [(ti, di) for ti, di in zip(t, d) if di > 0]
    xs = [ti for ti, _ in pts]
    ys = [math.log(di) for _, di in pts]
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    den = sum((x - mx) ** 2 for x in xs)
    m = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den
    b = my - m * mx
    l0 = math.exp(b)
    mu0 = -l0 / m if m != 0 else float("inf")
    return l0, mu0, m, b


def report(
    t: Sequence[float], d: Sequence[int], titulo: str
) -> tuple[int, float | None, float | None]:
    """Imprimir el informe del ajuste para un conjunto de datos.

    Args:
        t: Instantes (días o sesiones).
        d: Defectos instantáneos por intervalo.
        titulo: Encabezado del informe.

    Returns:
        La tupla ``(i, lambda0, mu0)``; los dos últimos son ``None`` si
        no hay decaimiento estimable (pendiente no negativa).
    """
    print("=" * 70)
    print(titulo)
    print("=" * 70)
    print(f"  t (dia/sesion) = {t}")
    print(f"  d (defectos)   = {d}")
    i = sum(d)
    print(f"  defectos identificados  i = sum(d) = {i}")
    l0, mu0, m, b = loglin_fit(t, d)
    print(f"  regresion:  m = {m:.4f}   b = {b:.4f}")
    if m >= 0:
        print(
            f"  lambda0 = {l0:.4f}   "
            "mu0 = NO ESTIMABLE (m>=0, sin decaimiento)"
        )
        return i, None, None
    print(f"  lambda0 = {l0:.4f}   mu0 = {mu0:.4f}")
    return i, l0, mu0


_configurar_stdout()

# ======================================================================
# PARTE 1 - datos genericos (dias 0..6)
# ======================================================================
print()
t1 = [0, 1, 2, 3, 4, 5, 6]
d1 = [9, 18, 5, 7, 23, 2, 8]
i1, l01, mu01 = report(t1, d1, "PARTE 1 - Proyeccion generica (dias)")

if mu01 is not None and l01 is not None:
    print(f"  mu0 = {mu01:.2f} defectos totales esperados")
    print(
        f"  mu_r = mu0 - i = {mu01:.2f} - {i1} = "
        f"{mu01 - i1:.2f} defectos liberados"
    )
    print("  proyeccion de defectos acumulados:")
    for instante in (7, 10, 14, 21, 30):
        acumulados = mu(instante, l01, mu01)
        instantaneos = lam(instante, l01, mu01)
        print(
            f"     t={instante:>3}  mu(t)={acumulados:7.2f}   "
            f"lambda(t)={instantaneos:6.2f}"
        )

# ======================================================================
# PARTE 2 - Collatz: dataset de resultados de prueba (TP11)
#
#  Sesion 1 (inspeccion de codigo).............. 6 defectos
#  Sesion 2 (inspeccion de casos de test)....... 2 defectos
#  Sesion 3 (unitaria 1 - 8 fallos)............. 8 defectos
#  Sesion 4 (unitaria 2 - fallo T14)............ 1 defecto
#  Sesion 5 (unitaria 3 - validacion)........... 0 defectos
#  Sesion 6 (funcional 1)....................... 0 defectos
# ======================================================================
t2 = [1, 2, 3, 4]
d2 = [6, 2, 8, 1]
i2, _, mu02 = report(t2, d2, "PARTE 2 - Collatz (sesiones con defectos)")

S0 = 42  # cat collatz.py | wc -l  (equiv.)
print()
print(f"  tamano medido del codigo:  S0 = wc -l collatz.py = {S0} LOC")

if mu02 is not None:
    mu_r = mu02 - i2
    delta = i2 / S0
    # S = mu0 / delta  (con delta = defectos/LOC observada) == mu0*S0/i
    S_final = mu02 * S0 / i2
    print(
        f"  mu0 = {mu02:.2f} defectos totales;  "
        f"mu_r = mu0 - i = {mu_r:.2f} liberados"
    )
    print(
        f"  densidad observada delta = i/S0 = {i2}/{S0} = "
        f"{delta:.4f} def/LOC"
    )
    print(f"  S_final = mu0/delta = mu0*S0/i = {S_final:.1f} LOC")
    # linea de base del informe: D = 5/18 = 0.2778 def/LOC
    D = 5 / 18
    print(
        f"  (linea de base informe: D = 5/18 = {D:.4f} def/LOC  ->  "
        f"S = mu0/D = {mu02 / D:.1f} LOC)"
    )
