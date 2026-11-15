
"""Método abierto de la Secante para BelugaCalc."""

import math
from core.biseccion import preparar_funcion


def formato_matematico(expresion):
    texto = str(expresion)

    for potencia, simbolo in (
        ("**4", "⁴"),
        ("**3", "³"),
        ("**2", "²")
    ):
        texto = texto.replace(potencia, simbolo)

    return texto.replace("*", "")


def resolver_secante(
    expresion, x0, x1, tolerancia, max_iteraciones
):
    """
    Resuelve f(x) = 0 mediante el método de la Secante.

    Retorna:
    funcion_simbolica, filas, raiz, residuo, resumen
    """

    # 1. Validar datos
    try:
        anterior = float(x0)
        actual = float(x1)
        tolerancia = float(tolerancia)
        max_iteraciones = int(max_iteraciones)

    except (ValueError, TypeError, OverflowError) as exc:
        raise ValueError(
            "X0, X1, tolerancia e iteraciones deben ser numéricos."
        ) from exc

    if not all(map(
        math.isfinite, (anterior, actual, tolerancia)
    )):
        raise ValueError("Los valores deben ser finitos.")

    if anterior == actual:
        raise ValueError("X0 y X1 deben ser diferentes.")

    if tolerancia <= 0:
        raise ValueError("La tolerancia debe ser mayor que cero.")

    if max_iteraciones < 1:
        raise ValueError(
            "El máximo de iteraciones debe ser al menos 1."
        )

    # 2. Preparar la función
    simbolica, f = preparar_funcion(expresion)

    filas = []
    convergio = False
    motivo = "Se alcanzó el máximo de iteraciones."

    # 3. Verificar los valores iniciales
    if abs(f(anterior)) < tolerancia:
        actual = anterior
        convergio = True
        motivo = "X0 ya satisface la tolerancia del residuo."

    elif abs(f(actual)) < tolerancia:
        convergio = True
        motivo = "X1 ya satisface la tolerancia del residuo."

    else:
        # 4. Aplicar el método
        for i in range(1, max_iteraciones + 1):

            f_anterior = f(anterior)
            f_actual = f(actual)

            denominador = f_actual - f_anterior

            escala = max(
                abs(f_actual),
                abs(f_anterior),
                1e-300
            )

            # Evitar división entre cero
            if abs(denominador) <= 1e-14 * escala:
                raise ZeroDivisionError(
                    "f(X1) - f(X0) es cero o demasiado pequeño. "
                    "Prueba con otros valores iniciales."
                )

            # Fórmula de la Secante
            nuevo = actual - f_actual * (
                (actual - anterior) / denominador
            )

            if not math.isfinite(nuevo):
                raise ArithmeticError(
                    "La nueva aproximación no es finita."
                )

            f_nuevo = f(nuevo)

            # 5. Calcular error y residuo
            cambio = abs(nuevo - actual)
            residuo = abs(f_nuevo)

            # 6. Guardar iteración
            filas.append({
                "it": i,
                "x_anterior": anterior,
                "x_actual": actual,
                "fx_anterior": f_anterior,
                "fx_actual": f_actual,
                "x_nuevo": nuevo,
                "fx_nuevo": f_nuevo,
                "cambio": cambio,
                "residuo": residuo
            })

            # 7. Actualizar valores
            anterior = actual
            actual = nuevo

            # 8. Comprobar convergencia
            if residuo < tolerancia and cambio < tolerancia:
                convergio = True
                motivo = (
                    "Residuo y cambio menores que la tolerancia."
                )
                break

    # 9. Resultado final
    residuo_final = abs(f(actual))

    resumen = (
        f"Método: Secante\n"
        f"Función: {formato_matematico(simbolica)}\n"
        f"Raíz aproximada: {actual:.10f}\n"
        f"Residuo: {residuo_final:.10g}\n"
        f"Iteraciones: {len(filas)}\n"
        f"Convergencia: {'Sí' if convergio else 'No'}\n"
        f"Motivo: {motivo}"
    )

    return simbolica, filas, actual, residuo_final, resumen
