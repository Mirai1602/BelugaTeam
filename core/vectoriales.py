from fractions import Fraction


class VectorModel:
    """Operaciones vectoriales usando únicamente Python estándar."""

    @staticmethod
    def a_fraction(valor):
        texto = str(valor).strip().replace(',', '.')
        return Fraction(texto) if texto else Fraction(0)

    @staticmethod
    def validar_misma_dimension(*vectores):
        if not vectores or any(len(v) == 0 for v in vectores):
            raise ValueError("Los vectores no pueden estar vacíos.")
        dimension = len(vectores[0])
        if any(len(v) != dimension for v in vectores):
            raise ValueError("Todos los vectores deben tener la misma dimensión.")

    @staticmethod
    def suma(a, b):
        VectorModel.validar_misma_dimension(a, b)
        return [x + y for x, y in zip(a, b)]

    @staticmethod
    def resta(a, b):
        VectorModel.validar_misma_dimension(a, b)
        return [x - y for x, y in zip(a, b)]

    @staticmethod
    def escalar(vector, factor):
        return [factor * x for x in vector]

    @staticmethod
    def combinacion_lineal(generadores, objetivo):
        """Resuelve C*c=b, donde las columnas de C son los generadores."""
        if not generadores:
            raise ValueError("Debe existir al menos un vector generador.")
        VectorModel.validar_misma_dimension(*generadores, objetivo)

        filas = len(objetivo)
        cantidad = len(generadores)
        aumentada = []

        for i in range(filas):
            fila = [generadores[j][i] for j in range(cantidad)]
            fila.append(objetivo[i])
            aumentada.append(fila)

        rref, pivotes = VectorModel._gauss_jordan(aumentada, cantidad)

        for fila in rref:
            if all(fila[j] == 0 for j in range(cantidad)) and fila[cantidad] != 0:
                return {
                    "es_combinacion": False,
                    "clasificacion": "No es combinación lineal: sistema incompatible.",
                    "coeficientes": None,
                    "pasos": "Se encontró una ecuación imposible del tipo 0 = b, con b distinto de cero."
                }

        if len(pivotes) < cantidad:
            return {
                "es_combinacion": True,
                "clasificacion": "Sí es combinación lineal, pero existen infinitas representaciones.",
                "coeficientes": "Existen variables libres; se requiere una representación particular.",
                "pasos": "El sistema es compatible indeterminado porque hay variables libres."
            }

        coeficientes = [Fraction(0) for _ in range(cantidad)]
        for fila, columna in enumerate(pivotes):
            if columna < cantidad:
                coeficientes[columna] = rref[fila][cantidad]

        return {
            "es_combinacion": True,
            "clasificacion": "Sí es combinación lineal.",
            "coeficientes": coeficientes,
            "pasos": "Se construyó la matriz con los generadores como columnas y se aplicó Gauss-Jordan."
        }

    @staticmethod
    def _gauss_jordan(matriz, cantidad_variables):
        matriz = [fila[:] for fila in matriz]
        filas = len(matriz)
        columnas = cantidad_variables
        pivotes = []
        fila_pivote = 0

        for columna in range(columnas):
            if fila_pivote >= filas:
                break

            encontrado = None
            for i in range(fila_pivote, filas):
                if matriz[i][columna] != 0:
                    encontrado = i
                    break

            if encontrado is None:
                continue

            matriz[fila_pivote], matriz[encontrado] = matriz[encontrado], matriz[fila_pivote]
            pivote = matriz[fila_pivote][columna]
            matriz[fila_pivote] = [valor / pivote for valor in matriz[fila_pivote]]

            for i in range(filas):
                if i == fila_pivote:
                    continue
                factor = matriz[i][columna]
                if factor != 0:
                    matriz[i] = [
                        matriz[i][j] - factor * matriz[fila_pivote][j]
                        for j in range(columnas + 1)
                    ]

            pivotes.append(columna)
            fila_pivote += 1

        return matriz, pivotes

    @staticmethod
    def valor(valor):
        if isinstance(valor, Fraction):
            return str(valor.numerator) if valor.denominator == 1 else f"{valor.numerator}/{valor.denominator}"
        return str(valor)

    @staticmethod
    def formato_vector(vector):
        return "(" + ", ".join(VectorModel.valor(x) for x in vector) + ")"
