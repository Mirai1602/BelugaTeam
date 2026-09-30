from fractions import Fraction


class MatrizInversa:
    """Lógica independiente para calcular matrices inversas.

    Este módulo no modifica MatrizModel ni las operaciones existentes.
    """

    @staticmethod
    def a_fraction(valor):
        #"""Convierte números y textos a Fraction sin perder exactitud."""
        #Esto solo es extra, pero funciona bien 
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
    #Le da la estructura a la matriz 
    def formato_matriz(matriz):
        return "\n".join(
            "[ " + "  ".join(f"{MatrizInversa.formato_valor(v):>8}" for v in fila) + " ]"
            for fila in matriz
        )
    #Sector de validaciones, se asegura que la matriz sea cuadrada y no vacía
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

        # Validacion 1: Una inversa solamente existe para matrices cuadradas.
        if filas != columnas:
            raise ValueError(
                f"La matriz no es cuadrada ({filas}×{columnas}). "
                "No se puede calcular su inversa."
            )

        return filas, columnas

    @staticmethod
    def inversa(matriz, operacion="Matriz inversa"):
        """Calcula A^-1 y devuelve resultado, pasos y validaciones."""
        filas, columnas = MatrizInversa.validar_matriz(matriz)
        A = [[MatrizInversa.a_fraction(v) for v in fila] for fila in matriz]
        validaciones = [
            f"Dimensiones detectadas: {filas}×{columnas}.",
            "Validación: la matriz es cuadrada."
        ]

        if operacion == "Matriz inversa de una matriz inversa":
            # (A^-1)^-1 = A, pero primero comprobamos que A sea invertible.
            primera = MatrizInversa._calcular_inversa(A)
            resultado = MatrizInversa._extraer_inversa(primera[0])
            validaciones.append("La primera inversa existe; se aplica nuevamente la inversión.")
            validaciones.append("Propiedad utilizada: (A⁻¹)⁻¹ = A.")
            return {
                "resultado": resultado,
                "pasos": primera[1] + "\n\nSegunda inversión:\n" + MatrizInversa.formato_matriz(A),
                "validaciones": "\n".join(validaciones),
                "metodo": primera[2],
            }

        if filas == 2:
            resultado, pasos, metodo = MatrizInversa._inversa_2x2(A)
        else:
            aumentada, pasos, metodo = MatrizInversa._calcular_inversa(A)
            resultado = MatrizInversa._extraer_inversa(aumentada)

        validaciones.append("La matriz tiene inversa: determinante/rango no singular.")
        return {
            "resultado": resultado,
            "pasos": pasos,
            "validaciones": "\n".join(validaciones),
            "metodo": metodo,
        }

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
            "Resultado:",
            MatrizInversa.formato_matriz(resultado),
        ])
        return resultado, "\n".join(pasos), "Fórmula de inversa 2×2"

    @staticmethod
    def _calcular_inversa(A):
        n = len(A)
        identidad = [
            [Fraction(1 if i == j else 0, 1) for j in range(n)]
            for i in range(n)
        ]
        aumentada = [A[i][:] + identidad[i][:] for i in range(n)]
        pasos = [
            f"Método: Gauss-Jordan para matriz {n}×{n}.",
            "Matriz aumentada inicial [A | I]:",
            MatrizInversa._formato_aumentada(aumentada, n),
        ]

        for col in range(n):
            pivote = next((fila for fila in range(col, n) if aumentada[fila][col] != 0), None)
            if pivote is None:
                raise ValueError("La matriz es singular y no tiene inversa.")

            if pivote != col:
                aumentada[col], aumentada[pivote] = aumentada[pivote], aumentada[col]
                pasos.append(f"F{col + 1} ↔ F{pivote + 1}")
                pasos.append(MatrizInversa._formato_aumentada(aumentada, n))

            valor_pivote = aumentada[col][col]
            if valor_pivote != 1:
                aumentada[col] = [v / valor_pivote for v in aumentada[col]]
                pasos.append(
                    f"F{col + 1} ← F{col + 1} / {MatrizInversa.formato_valor(valor_pivote)}"
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
                    f"F{fila + 1} ← F{fila + 1} - ({MatrizInversa.formato_valor(factor)})F{col + 1}"
                )
                pasos.append(MatrizInversa._formato_aumentada(aumentada, n))

        izquierda = [fila[:n] for fila in aumentada]
        if izquierda != identidad:
            raise ValueError("No fue posible obtener la identidad. La matriz no tiene inversa.")

        pasos.append("Se obtuvo [I | A⁻¹].")
        return aumentada, "\n".join(pasos), "Gauss-Jordan sobre [A | I]"

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
