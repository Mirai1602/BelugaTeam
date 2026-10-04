from fractions import Fraction

# Clase de inversa.py, donde vamos a usar la ventana de operaciones nueva
# de Matrices inversas
class MatrizInversa:
    """Lógica independiente para calcular y verificar matrices inversas."""

    @staticmethod
    def a_fraction(valor):
        """Convierte números y textos a Fraction sin perder exactitud."""
        if isinstance(valor, Fraction):
            return valor
        if isinstance(valor, int):
            return Fraction(valor, 1)
        if isinstance(valor, float):
            return Fraction(str(valor))

        texto = str(valor).strip().replace(",", ".")
        if "/" in texto:
            partes = texto.split("/")
            if len(partes) != 2:
                raise ValueError(f"Valor fraccionario inválido: {valor}")
            return Fraction(int(partes[0].strip()), int(partes[1].strip()))
        return Fraction(texto)

    @staticmethod
    def formato_valor(valor):
        valor = MatrizInversa.a_fraction(valor)
        if valor.denominator == 1:
            return str(valor.numerator)
        return f"{valor.numerator}/{valor.denominator}"

    @staticmethod
    def formato_matriz(matriz):
        return "\n".join(
            "[ " + "  ".join(f"{MatrizInversa.formato_valor(v):>8}" for v in fila) + " ]"
            for fila in matriz
        )

    @staticmethod
    def validar_matriz(matriz):
        """Realiza las validaciones previas y devuelve (filas, columnas)."""
        if not matriz or not isinstance(matriz, list):
            raise ValueError("La matriz no puede estar vacía.")

        filas = len(matriz)
        if any(not isinstance(fila, list) or len(fila) == 0 for fila in matriz):
            raise ValueError("Todas las filas deben contener elementos.")

        columnas = len(matriz[0])
        if any(len(fila) != columnas for fila in matriz):
            raise ValueError("Todas las filas deben tener la misma cantidad de columnas.")

        if filas != columnas:
            raise ValueError(
                f"La matriz no es cuadrada ({filas}×{columnas}). "
                "No se puede calcular su inversa."
            )

        return filas, columnas

    # Muestra de ventana de labels (menu)
    @staticmethod
    def inversa(matriz, operacion="Matriz inversa"):
        """Calcula A^-1 y devuelve resultado, pasos, validaciones y verificación."""
        filas, columnas = MatrizInversa.validar_matriz(matriz)
        A = [[MatrizInversa.a_fraction(v) for v in fila] for fila in matriz]
        identidad = MatrizInversa._identidad(filas)
        validaciones = [
            f"Dimensiones detectadas: {filas}×{columnas}.",
            "Validación: la matriz es cuadrada."
        ]

        if operacion == "Matriz inversa de una matriz inversa":
            # Primera inversión: B = A^-1.
            primera_resultado, primera_pasos, primera_metodo = MatrizInversa._calcular_por_tamano(A)

            # Segunda inversión: B^-1 = (A^-1)^-1 = A.
            segunda_resultado, segunda_pasos, segunda_metodo = MatrizInversa._calcular_por_tamano(
                primera_resultado
            )

            verificacion_primera = MatrizInversa._verificar_inversa(A, primera_resultado)
            verificacion_segunda = MatrizInversa._verificar_inversa(primera_resultado, segunda_resultado)

            validaciones.extend([
                "La primera inversa existe; la matriz A es no singular.",
                "Se aplica nuevamente la inversión sobre A⁻¹.",
                "Propiedad utilizada: (A⁻¹)⁻¹ = A.",
                "La segunda inversión devuelve la matriz original A."
            ])

            pasos = (
                "=== PRIMERA INVERSIÓN: A⁻¹ ===\n"
                + primera_pasos
                + "\n\n=== VERIFICACIÓN DE A⁻¹ ===\n"
                + verificacion_primera
                + "\n\n=== SEGUNDA INVERSIÓN: (A⁻¹)⁻¹ ===\n"
                + segunda_pasos
                + "\n\n=== VERIFICACIÓN DE (A⁻¹)⁻¹ ===\n"
                + verificacion_segunda
            )

            return {
                "resultado": segunda_resultado,
                "pasos": pasos,
                "validaciones": "\n".join(validaciones),
                "metodo": f"{primera_metodo} + {segunda_metodo}",
            }

        resultado, pasos, metodo = MatrizInversa._calcular_por_tamano(A)
        verificacion = MatrizInversa._verificar_inversa(A, resultado)
        validaciones.append("La matriz tiene inversa: se pudo obtener [I | A⁻¹].")
        validaciones.append("Verificación: A·A⁻¹ = I y A⁻¹·A = I.")

        pasos += "\n\n=== VERIFICACIÓN ===\n" + verificacion

        return {
            "resultado": resultado,
            "pasos": pasos,
            "validaciones": "\n".join(validaciones),
            "metodo": metodo,
        }

    @staticmethod
    def _calcular_por_tamano(A):
        """Selecciona el método adecuado según el tamaño de la matriz."""
        n = len(A)
        if n == 2:
            return MatrizInversa._inversa_2x2(A)

        aumentada, pasos, metodo = MatrizInversa._calcular_inversa(A)
        resultado = MatrizInversa._extraer_inversa(aumentada)
        return resultado, pasos, metodo

    # Calculo de determinante + comprobacion de 2x2
    @staticmethod
    def _inversa_2x2(A):
        a, b = A[0]
        c, d = A[1]
        determinante = a * d - b * c

        pasos = [
            "Matriz A:",
            MatrizInversa.formato_matriz(A),
            "Método: fórmula para una matriz 2×2.",
            f"det(A) = ({MatrizInversa.formato_valor(a)})({MatrizInversa.formato_valor(d)}) - "
            f"({MatrizInversa.formato_valor(b)})({MatrizInversa.formato_valor(c)})",
            f"det(A) = {MatrizInversa.formato_valor(determinante)}",
        ]

        if determinante == 0:
            raise ValueError("La matriz 2×2 es singular porque su determinante es 0. No tiene inversa.")

        resultado = [
            [d / determinante, -b / determinante],
            [-c / determinante, a / determinante],
        ]
        pasos.extend([
            "Como det(A) ≠ 0, la inversa existe.",
            "A⁻¹ = 1/det(A) · [ d  -b ; -c  a ]",
            "Resultado A⁻¹:",
            MatrizInversa.formato_matriz(resultado),
        ])
        return resultado, "\n".join(pasos), "Fórmula de inversa 2×2"

    # Operacion de calculo a ejercicio indicado de inversa
    # (osea luego de darle a ejecutar)
    @staticmethod
    def _calcular_inversa(A):
        n = len(A)
        identidad = MatrizInversa._identidad(n)
        aumentada = [A[i][:] + identidad[i][:] for i in range(n)]
        pasos = [
            f"Método: Gauss-Jordan para matriz {n}×{n}.",
            "Paso 1: construir la matriz aumentada [A | I].",
            MatrizInversa._formato_aumentada(aumentada, n),
        ]

        for col in range(n):
            pivote = next((fila for fila in range(col, n) if aumentada[fila][col] != 0), None)
            if pivote is None:
                raise ValueError("La matriz es singular y no tiene inversa: no existe un pivote válido en la columna correspondiente.")

            if pivote != col:
                aumentada[col], aumentada[pivote] = aumentada[pivote], aumentada[col]
                pasos.append(f"Intercambio de filas: F{col + 1} ↔ F{pivote + 1}")
                pasos.append(MatrizInversa._formato_aumentada(aumentada, n))

            valor_pivote = aumentada[col][col]
            if valor_pivote != 1:
                aumentada[col] = [v / valor_pivote for v in aumentada[col]]
                pasos.append(
                    f"Normalización del pivote: F{col + 1} ← F{col + 1} / {MatrizInversa.formato_valor(valor_pivote)}"
                )
                pasos.append(MatrizInversa._formato_aumentada(aumentada, n))

            for fila in range(n):
                if fila == col:
                    continue
                factor = aumentada[fila][col]
                if factor == 0:
                    continue

                aumentada[fila] = [
                    aumentada[fila][j] - factor * aumentada[col][j]
                    for j in range(2 * n)
                ]
                pasos.append(
                    f"Eliminación: F{fila + 1} ← F{fila + 1} - ({MatrizInversa.formato_valor(factor)})F{col + 1}"
                )
                pasos.append(MatrizInversa._formato_aumentada(aumentada, n))

        izquierda = [fila[:n] for fila in aumentada]
        if izquierda != identidad:
            raise ValueError("No fue posible obtener la identidad. La matriz no tiene inversa.")

        pasos.append("Resultado del algoritmo: [I | A⁻¹].")
        pasos.append("A⁻¹:")
        pasos.append(MatrizInversa.formato_matriz(MatrizInversa._extraer_inversa(aumentada)))
        return aumentada, "\n".join(pasos), "Gauss-Jordan sobre [A | I]"

    @staticmethod
    def _identidad(n):
        return [
            [Fraction(1 if i == j else 0, 1) for j in range(n)]
            for i in range(n)
        ]

    @staticmethod
    def _multiplicar(A, B):
        """Multiplicación exacta de matrices usando Fraction."""
        filas_a = len(A)
        columnas_a = len(A[0])
        filas_b = len(B)
        columnas_b = len(B[0])

        if columnas_a != filas_b:
            raise ValueError("No se pueden multiplicar las matrices: las dimensiones internas no coinciden.")

        return [
            [
                sum(A[i][k] * B[k][j] for k in range(columnas_a))
                for j in range(columnas_b)
            ]
            for i in range(filas_a)
        ]

    @staticmethod
    def _es_identidad(matriz):
        n = len(matriz)
        identidad = MatrizInversa._identidad(n)
        return matriz == identidad

    @staticmethod
    def _verificar_inversa(A, inversa):
        producto_1 = MatrizInversa._multiplicar(A, inversa)
        producto_2 = MatrizInversa._multiplicar(inversa, A)
        identidad = MatrizInversa._identidad(len(A))

        ok_1 = MatrizInversa._es_identidad(producto_1)
        ok_2 = MatrizInversa._es_identidad(producto_2)

        return (
            "Comprobación A · A⁻¹:\n"
            + MatrizInversa.formato_matriz(producto_1)
            + f"\nResultado: {'✓ Es la identidad.' if ok_1 else '✗ No es la identidad.'}\n\n"
            "Comprobación A⁻¹ · A:\n"
            + MatrizInversa.formato_matriz(producto_2)
            + f"\nResultado: {'✓ Es la identidad.' if ok_2 else '✗ No es la identidad.'}\n\n"
            f"Conclusión: {'La inversa fue verificada correctamente.' if ok_1 and ok_2 else 'La verificación falló.'}"
        )

    # Construccion de n fila
    @staticmethod
    def _extraer_inversa(aumentada):
        n = len(aumentada)
        return [fila[n:] for fila in aumentada]

    @staticmethod
    def _formato_aumentada(matriz, separacion):
        lineas = []
        for fila in matriz:
            izquierda = "  ".join(f"{MatrizInversa.formato_valor(v):>8}" for v in fila[:separacion])
            derecha = "  ".join(f"{MatrizInversa.formato_valor(v):>8}" for v in fila[separacion:])
            lineas.append(f"[ {izquierda}  | {derecha} ]")
        return "\n".join(lineas)
