"""Implementación del método Regula Falsi (Regla Falsa)."""
import math

from core.biseccion import preparar_funcion, verificar_continuidad


def resolver_regula_falsi(expresion, a, b, tolerancia, max_iteraciones):
    """Resuelve f(x)=0 por Regula Falsi usando el criterio Ea porcentual de la guía.

    Fórmula: xr = b - f(b) * (a - b) / (f(a) - f(b))
    Actualización: si f(a)*f(xr)<0, b=xr; si no, a=xr.
    Retorna función simbólica, filas, raíz, error, resumen e intervalos inicial/final.
    """
    try:
        a, b = float(a), float(b)
        tolerancia = float(tolerancia)
        max_iteraciones = int(max_iteraciones)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("A, B, la tolerancia y el máximo de iteraciones deben ser numéricos.") from exc

    if not all(math.isfinite(v) for v in (a, b, tolerancia)):
        raise ValueError("A, B y la tolerancia deben ser valores finitos.")
    if a >= b:
        raise ValueError("El límite A debe ser menor que el límite B.")
    if tolerancia <= 0:
        raise ValueError("La tolerancia Ea debe ser mayor que cero.")
    if max_iteraciones < 1:
        raise ValueError("El máximo de iteraciones debe ser al menos 1.")

    simbolica, f = preparar_funcion(expresion)
    verificar_continuidad(simbolica, a, b)
    fa, fb = f(a), f(b)

    if fa == 0:
        return simbolica, [], a, 0.0, f"La raíz exacta coincide con A = {a:g}.", (a, b), (a, b)
    if fb == 0:
        return simbolica, [], b, 0.0, f"La raíz exacta coincide con B = {b:g}.", (a, b), (a, b)
    if fa * fb >= 0:
        raise ValueError(
            "El intervalo no encierra una raíz: f(A) y f(B) deben tener signos opuestos. "
            f"f(A) = {fa:.8g}; f(B) = {fb:.8g}. Inspecciona la gráfica y elige otros extremos."
        )

    intervalo_inicial = (a, b)
    filas = []
    xr_anterior = None
    error = None
    raiz = None

    for it in range(1, max_iteraciones + 1):
        denominador = fa - fb
        if abs(denominador) <= 1e-15 * max(1.0, abs(fa), abs(fb)):
            raise ZeroDivisionError(
                "f(A) - f(B) es cero o demasiado pequeño; no se puede calcular la interpolación. "
                "Prueba otro intervalo."
            )

        # Intersección de la recta secante entre (A,f(A)) y (B,f(B)) con el eje X.
        xr = b - (fb * (a - b)) / denominador
        if not math.isfinite(xr):
            raise ArithmeticError("La interpolación produjo una aproximación no finita.")
        fxr = f(xr)

        if xr_anterior is None:
            error = None
            criterio = "Primera iteración: no existe una aproximación anterior para calcular Ea."
        elif xr == 0:
            error = abs(xr - xr_anterior)
            criterio = "xr = 0: se utiliza el cambio absoluto para evitar división entre cero."
        else:
            error = abs((xr - xr_anterior) / xr) * 100.0
            criterio = "Ea = |(xr actual - xr anterior) / xr actual| × 100%."

        fila = {
            "it": it, "a": a, "b": b, "fa": fa, "fb": fb,
            "xr": xr, "fxr": fxr, "error": error,
            "residuo": abs(fxr), "criterio": criterio,
        }
        filas.append(fila)
        raiz = xr

        if fxr == 0:
            error = 0.0
            fila["error"] = error
            fila["actualizacion"] = "Se encontró una raíz exacta: f(xr) = 0."
            fila["criterio"] = "Raíz exacta; no se requieren más iteraciones."
            break

        producto = fa * fxr
        if producto < 0:
            b, fb = xr, fxr
            fila["actualizacion"] = "B = xr; la raíz permanece en [A, xr]."
        elif producto > 0:
            a, fa = xr, fxr
            fila["actualizacion"] = "A = xr; la raíz permanece en [xr, B]."
        else:
            raise ArithmeticError("No se pudo conservar el cambio de signo del intervalo.")

        if error is not None and error < tolerancia:
            break
        xr_anterior = xr
    else:
        raise ValueError(
            f"No se alcanzó Ea < {tolerancia:g}% en {max_iteraciones} iteraciones. "
            "Aumenta el máximo de iteraciones o utiliza una tolerancia menos estricta."
        )

    intervalo_final = (a, b)
    error_texto = "no calculado" if error is None else f"{error:.6g}%"
    resumen = (
        f"Se realizaron {len(filas)} iteraciones. Raíz aproximada: {raiz:.10g}. "
        f"Error aproximado final: {error_texto}. Residuo |f(xr)|: {abs(f(raiz)):.6g}."
    )
    return simbolica, filas, raiz, error, resumen, intervalo_inicial, intervalo_final
