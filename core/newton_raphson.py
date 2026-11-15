import math
import sympy as sp
from core.biseccion import preparar_funcion, X


def resolver_newton_raphson(expresion, x0, tolerancia, max_iteraciones):
    try:
        x0 = float(x0)
        tolerancia = float(tolerancia)
        max_iteraciones = int(max_iteraciones)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError('X0, tolerancia y máximo de iteraciones deben ser numéricos.') from exc
    if not math.isfinite(x0):
        raise ValueError('X0 debe ser un número finito.')
    if not math.isfinite(tolerancia) or tolerancia <= 0:
        raise ValueError('La tolerancia debe ser positiva y finita.')
    if max_iteraciones < 1:
        raise ValueError('El máximo de iteraciones debe ser al menos 1.')

    simbolica, f = preparar_funcion(expresion)
    derivada = sp.diff(simbolica, X)
    df_numerica = sp.lambdify(X, derivada, modules=['math'])

    def df(x):
        try:
            resultado = float(df_numerica(x))
        except (TypeError, ValueError, ZeroDivisionError, OverflowError) as exc:
            raise ValueError(f'No se puede evaluar la derivada en x = {x:.10g}.') from exc
        if not math.isfinite(resultado):
            raise ValueError('La derivada no es finita.')
        return resultado

    filas = []
    actual = x0
    convergio = False
    motivo = 'Se alcanzó el máximo de iteraciones.'
    for i in range(1, max_iteraciones + 1):
        fx = f(actual)
        if abs(fx) < tolerancia:
            convergio = True
            motivo = 'Residuo menor que la tolerancia.'
            break
        dfx = df(actual)
        if abs(dfx) < 1e-12:
            raise ZeroDivisionError('La derivada es cero o demasiado pequeña. Prueba otro X0.')
        nuevo = actual - fx / dfx
        if not math.isfinite(nuevo):
            raise ArithmeticError('La nueva aproximación no es finita.')
        fx_nuevo = f(nuevo)
        cambio = abs(nuevo - actual)
        residuo = abs(fx_nuevo)
        filas.append({'it': i, 'x_anterior': actual, 'fx': fx,
                      'dfx': dfx, 'x_nuevo': nuevo, 'fx_nuevo': fx_nuevo,
                      'cambio': cambio, 'residuo': residuo})
        actual = nuevo
        if residuo < tolerancia and cambio < tolerancia:
            convergio = True
            motivo = 'Residuo y cambio menores que la tolerancia.'
            break

    residuo_final = abs(f(actual))

    # Función para mostrar expresiones matemáticas bonitas
    def formato_matematico(expresion):
        texto = str(expresion)
        texto = texto.replace("**3", "³")
        texto = texto.replace("**2", "²")
        texto = texto.replace("**4", "⁴")
        texto = texto.replace("*", "")
        return texto

    # Formatear función y derivada
    funcion_formateada = formato_matematico(simbolica)
    derivada_formateada = formato_matematico(derivada)

    # Crear resumen
    resumen = (
        f'Método: Newton-Raphson\n'
        f'Función: {funcion_formateada}\n'
        f'Derivada: {derivada_formateada}\n'
        f'Raíz aproximada: {actual:.10f}\n'
        f'Residuo: {residuo_final:.10g}\n'
        f'Iteraciones: {len(filas)}\n'
        f'Convergencia: {"Sí" if convergio else "No"}\n'
        f'Motivo: {motivo}'
    )

    return simbolica, derivada, filas, actual, residuo_final, resumen
