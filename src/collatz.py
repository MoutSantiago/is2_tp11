"""Módulo con la implementación del algoritmo de Collatz."""


def collatz(num: int) -> int:
    """Calcular la cantidad de iteraciones de la conjetura de Collatz."""
    iteraciones = 0

    while num != 1:
        if num % 2 == 0:
            num = num // 2
        else:
            num = 3 * num + 1

        iteraciones += 1

    return iteraciones


def main() -> None:
    """Solicitar un número al usuario e imprimir sus iteraciones."""
    entrada = input("Ingrese un número entero positivo (máximo 1999): ")

    try:
        num = int(entrada)
    except ValueError:
        print("Error: debe ingresar un número entero.")
        return

    if num <= 0:
        print("Error: el número debe ser positivo.")
        return

    if num > 1999:
        print("Error: el número no puede ser mayor que 1999.")
        return

    iteraciones = collatz(num)

    print("Número inicial:", num)
    print("Cantidad de iteraciones:", iteraciones)


if __name__ == "__main__":
    main()
