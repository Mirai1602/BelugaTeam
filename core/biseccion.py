"""Método de bisección con validación de continuidad, signos y error aproximado."""
import ast
import math
import sympy as sp

X = sp.Symbol("x")

_FUNCTIONS = {
    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
    "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
    "sqrt": sp.sqrt, "log": sp.log, "ln": sp.log,
    "exp": sp.exp, "abs": sp.Abs,
}
_CONSTANTS = {"pi": sp.pi, "e": sp.E}


def _ast_a_sympy(nodo):
    """Interpreta únicamente operaciones y funciones matemáticas permitidas."""
    if isinstance(nodo, ast.Expression):
        return _ast_a_sympy(nodo.body)
    if isinstance(nodo, ast.Constant) and isinstance(nodo.value, (int, float)):
        return sp.sympify(nodo.value)
    if isinstance(nodo, ast.Name):
        if nodo.id == "x":
            return X
        if nodo.id in _CONSTANTS:
            return _CONSTANTS[nodo.id]
        raise ValueError(f"Nombre no permitido en la función: {nodo.id}")
    if isinstance(nodo, ast.BinOp):
        izquierda = _ast_a_sympy(nodo.left)
        derecha = _ast_a_sympy(nodo.right)
        operaciones = {
            ast.Add: lambda: izquierda + derecha,
            ast.Sub: lambda: izquierda - derecha,
            ast.Mult: lambda: izquierda * derecha,
            ast.Div: lambda: izquierda / derecha,
            ast.Pow: lambda: izquierda ** derecha,
            ast.Mod: lambda: sp.Mod(izquierda, derecha),
        }
        for tipo, operacion in operaciones.items():
            if isinstance(nodo.op, tipo):
                return operacion()
        raise ValueError("Operador matemático no permitido.")
    if isinstance(nodo, ast.UnaryOp):
        valor = _ast_a_sympy(nodo.operand)
        if isinstance(nodo.op, ast.UAdd):
            return valor
        if isinstance(nodo.op, ast.USub):
            return -valor
        raise ValueError("Operador unario no permitido.")
    if isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name):
        nombre = nodo.func.id
        if nombre not in _FUNCTIONS or nodo.keywords or len(nodo.args) != 1:
            raise ValueError(f"Función no permitida o argumentos incorrectos: {nombre}")
        return _FUNCTIONS[nombre](_ast_a_sympy(nodo.args[0]))
    raise ValueError("La expresión contiene sintaxis no permitida.")


def preparar_funcion(expresion):
    """Valida y prepara una función matemática de una variable x."""
    if not isinstance(expresion, str) or not expresion.strip():
        raise ValueError("Debes ingresar una función matemática.")
    texto = expresion.strip().replace("^", "**")
    try:
        arbol = ast.parse(texto, mode="eval")
        simbolica = _ast_a_sympy(arbol)
    except (SyntaxError, TypeError, ZeroDivisionError, ValueError) as exc:
        if isinstance(exc, ValueError):
            raise
        raise ValueError(
            "La función no es válida. Ejemplo: x^3 - 2*x - 5. "
            "Puedes usar sin, cos, tan, sqrt, log y exp."
        ) from exc

    if simbolica.free_symbols - {X}:
        raise ValueError("La función solo puede contener la variable x.")

    numerica = sp.lambdify(X, simbolica, modules=["math"])

    def f(valor):
        try:
            resultado = float(numerica(float(valor)))
        except (ValueError, TypeError, ZeroDivisionError, OverflowError) as exc:
            raise ValueError(
                f"No se puede evaluar la función en x = {valor:.10g}. "
                "Revisa el dominio de la función."
            ) from exc
        if not math.isfinite(resultado):
            raise ValueError(
                f"La función no produce un valor real finito en x = {valor:.10g}."
            )
        return resultado

    return simbolica, f


def verificar_continuidad(simbolica, a, b):
    """Comprueba simbólicamente si la función es continua en [a,b]."""
    intervalo = sp.Interval(a, b)
    try:
        dominio = sp.calculus.util.continuous_domain(simbolica, X, sp.S.Reals)
        faltante = intervalo - dominio
    except (NotImplementedError, ValueError, TypeError) as exc:
        raise ValueError(
            "No se pudo comprobar automáticamente la continuidad en el intervalo. "
            "Inspecciona la gráfica y utiliza un intervalo donde la función sea continua."
        ) from exc
    if faltante != sp.S.EmptySet:
        raise ValueError(
            f"La función no es continua en todo el intervalo [{a:g}, {b:g}]. "
            "Revisa la gráfica y selecciona otro intervalo."
        )
    return True


def resolver_biseccion(expresion, a, b, tolerancia, max_iteraciones):
    """Resuelve por bisección siguiendo la notación y reglas de la presentación docente.

    Error aproximado porcentual: Ea = abs((c_actual-c_anterior)/c_actual)*100.
    """
    try:
        a, b = float(a), float(b)
        tolerancia = float(tolerancia)
        max_iteraciones = int(max_iteraciones)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("Los límites, la tolerancia y las iteraciones deben ser numéricos.") from exc

    if not all(math.isfinite(v) for v in (a, b, tolerancia)):
        raise ValueError("Los límites y la tolerancia deben ser valores finitos.")
    if a >= b:
        raise ValueError("El límite inferior A debe ser menor que el límite superior B.")
    if tolerancia <= 0:
        raise ValueError("La tolerancia Ea debe ser mayor que cero.")
    if max_iteraciones < 1:
        raise ValueError("El número máximo de iteraciones debe ser al menos 1.")

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
            f"f(A) = {fa:.8g}; f(B) = {fb:.8g}. Observa la gráfica y selecciona otro intervalo."
        )

    filas = []
    c_anterior = None
    raiz = None
    error = None
    intervalo_inicial = (a, b)

    for it in range(1, max_iteraciones + 1):
        c = (a + b) / 2.0
        fc = f(c)

        if c_anterior is None:
            error = None
            criterio = "Primera iteración: no hay aproximación anterior para calcular Ea."
        elif c == 0:
            error = abs(c - c_anterior)
            criterio = "c = 0: se usa diferencia absoluta para evitar división entre cero."
        else:
            error = abs((c - c_anterior) / c) * 100.0
            criterio = "Ea = |(c actual - c anterior) / c actual| x 100%."

        fila = {
            "it": it, "xi": a, "xf": b, "xm": c,
            "fxi": fa, "fxf": fb, "fxm": fc,
            "error": error, "residuo": abs(fc), "criterio": criterio,
        }
        filas.append(fila)
        raiz = c

        if fc == 0:
            error = 0.0
            fila["error"] = error
            fila["criterio"] = "Raíz exacta: f(c) = 0."
            fila["actualizacion"] = "No se requiere actualizar: se encontró la raíz."
            break

        # Regla del docente: f(A)*f(C)<0 => B=C; si no, A=C.
        if fa * fc < 0:
            b, fb = c, fc
            fila["actualizacion"] = "B = C (la raíz queda en [A, C])."
        elif fc * fb < 0:
            a, fa = c, fc
            fila["actualizacion"] = "A = C (la raíz queda en [C, B])."
        else:
            raise ArithmeticError("No se pudo conservar el cambio de signo del intervalo.")

        if error is not None and error < tolerancia:
            break
        c_anterior = c
    else:
        raise ValueError(
            f"No se alcanzó Ea < {tolerancia:g}% en {max_iteraciones} iteraciones. "
            "Aumenta n o utiliza una tolerancia menos estricta."
        )

    resumen = (
        f"Se realizaron {len(filas)} iteraciones. Raíz aproximada: {raiz:.10g}. "
        f"Error aproximado final: {'no calculado' if error is None else f'{error:.6g}%'} ."
    )
    return simbolica, filas, raiz, error, resumen, intervalo_inicial, (a, b)
