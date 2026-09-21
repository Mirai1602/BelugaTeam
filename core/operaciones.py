from fractions import Fraction


class MatrizModel:

    # Suma
    @staticmethod
    def sumar(matrices):
        f_base, c_base = len(matrices[0]), len(matrices[0][0])
        res = [fila[:] for fila in matrices[0]]

        for m in matrices[1:]:
            for i in range(f_base):
                for j in range(c_base):
                    res[i][j] += m[i][j]

        return res

    # Resta
    @staticmethod
    def restar(matrices):
        f_base, c_base = len(matrices[0]), len(matrices[0][0])
        res = [fila[:] for fila in matrices[0]]

        for m in matrices[1:]:
            for i in range(f_base):
                for j in range(c_base):
                    res[i][j] -= m[i][j]

        return res

    # Multiplicación
    @staticmethod
    def multiplicar(matrices):
        res = matrices[0]

        for m in matrices[1:]:
            f_A, c_A = len(res), len(res[0])
            f_B, c_B = len(m), len(m[0])

            if c_A != f_B:
                raise ValueError("Dimensiones incompatibles para multiplicar.")

            sub_res = []

            for i in range(f_A):
                fila = []

                for j in range(c_B):
                    suma = 0

                    for k in range(c_A):
                        suma += res[i][k] * m[k][j]

                    fila.append(suma)

                sub_res.append(fila)

            res = sub_res

        return res

    # Formato de matriz
    @staticmethod
    def formato_matriz_str(matriz, titulo=""):
        texto = f"--- {titulo} ---\n" if titulo else ""

        for fila in matriz:
            valores = []

            for val in fila:
                if isinstance(val, Fraction):
                    if val.denominator == 1:
                        valores.append(str(val.numerator))
                    else:
                        valores.append(f"{val.numerator}/{val.denominator}")
                else:
                    valores.append(f"{val:.2f}")

            if valores:
                coefs = "  ".join([f"{val:>8}" for val in valores[:-1]])
                b_val = f"{valores[-1]:>8}"
                texto += f"[ {coefs}  | {b_val} ]\n"

        return texto + "\n"

    @staticmethod
    def _matriz_a_fraction(A, B):
        Ab = []

        for i in range(len(A)):
            fila = [Fraction(str(val)) for val in A[i]]
            fila.append(Fraction(str(B[i][0])))
            Ab.append(fila)

        return Ab

    @staticmethod
    def _formatear_factor(factor):
        if isinstance(factor, Fraction):
            if factor.denominator == 1:
                return str(factor.numerator)
            return f"{factor.numerator}/{factor.denominator}"

        return str(factor)

    @staticmethod
    def _forma_escalonada(A_orig, b_orig):
        m = len(A_orig)
        n = len(A_orig[0])
        Ab = MatrizModel._matriz_a_fraction(A_orig, b_orig)

        pasos_txt = MatrizModel.formato_matriz_str(
            Ab, "Matriz Aumentada Inicial (Ab)"
        )

        fila_pivote = 0
        pivotes = []

        for col in range(n):
            if fila_pivote >= m:
                break

            max_i = None

            for i in range(fila_pivote, m):
                if Ab[i][col] != 0:
                    if max_i is None or abs(Ab[i][col]) > abs(Ab[max_i][col]):
                        max_i = i

            if max_i is None:
                pasos_txt += f"Columna {col + 1}: Sin pivote válido.\n\n"
                continue

            if max_i != fila_pivote:
                Ab[fila_pivote], Ab[max_i] = Ab[max_i], Ab[fila_pivote]

                pasos_txt += (
                    f"Paso: Intercambio de Fila {fila_pivote + 1} "
                    f"con Fila {max_i + 1}\n"
                )
                pasos_txt += MatrizModel.formato_matriz_str(Ab)

            pivote = Ab[fila_pivote][col]

            for i in range(fila_pivote + 1, m):
                factor = Ab[i][col] / pivote

                if factor != 0:
                    for j in range(col, n + 1):
                        Ab[i][j] -= factor * Ab[fila_pivote][j]

                    factor_txt = MatrizModel._formatear_factor(factor)

                    pasos_txt += (
                        f"Paso: Fila {i + 1} = Fila {i + 1} - "
                        f"({factor_txt}) * Fila {fila_pivote + 1}\n"
                    )
                    pasos_txt += MatrizModel.formato_matriz_str(Ab)

            pivotes.append(col)
            fila_pivote += 1

        return Ab, pivotes, pasos_txt

    @staticmethod
    def _forma_escalonada_reducida(A_orig, b_orig):
        m = len(A_orig)
        n = len(A_orig[0])
        Ab = MatrizModel._matriz_a_fraction(A_orig, b_orig)

        pasos_txt = MatrizModel.formato_matriz_str(
            Ab, "Matriz Aumentada Inicial (Ab)"
        )

        fila_pivote = 0
        pivotes = []

        for col in range(n):
            if fila_pivote >= m:
                break

            max_i = None

            for i in range(fila_pivote, m):
                if Ab[i][col] != 0:
                    if max_i is None or abs(Ab[i][col]) > abs(Ab[max_i][col]):
                        max_i = i

            if max_i is None:
                pasos_txt += f"Columna {col + 1}: Sin pivote válido.\n\n"
                continue

            if max_i != fila_pivote:
                Ab[fila_pivote], Ab[max_i] = Ab[max_i], Ab[fila_pivote]

                pasos_txt += (
                    f"Paso: Intercambio de Fila {fila_pivote + 1} "
                    f"con Fila {max_i + 1}\n"
                )
                pasos_txt += MatrizModel.formato_matriz_str(Ab)

            pivote = Ab[fila_pivote][col]

            for j in range(n + 1):
                Ab[fila_pivote][j] /= pivote

            pivote_txt = MatrizModel._formatear_factor(pivote)

            pasos_txt += (
                f"Paso: Fila {fila_pivote + 1} = Fila {fila_pivote + 1} / "
                f"{pivote_txt} (Convertir pivote en 1)\n"
            )
            pasos_txt += MatrizModel.formato_matriz_str(Ab)

            for i in range(m):
                if i == fila_pivote:
                    continue

                factor = Ab[i][col]

                if factor != 0:
                    for j in range(n + 1):
                        Ab[i][j] -= factor * Ab[fila_pivote][j]

                    factor_txt = MatrizModel._formatear_factor(factor)

                    pasos_txt += (
                        f"Paso: Fila {i + 1} = Fila {i + 1} - "
                        f"({factor_txt}) * Fila {fila_pivote + 1}\n"
                    )
                    pasos_txt += MatrizModel.formato_matriz_str(Ab)

            pivotes.append(col)
            fila_pivote += 1

        return Ab, pivotes, pasos_txt

    @staticmethod
    def _clasificar(Ab, pivotes, n):
        inconsistente = False

        for fila in Ab:
            coeficientes_cero = all(fila[j] == 0 for j in range(n))

            if coeficientes_cero and fila[n] != 0:
                inconsistente = True
                break

        rango_A = len(pivotes)

        if inconsistente:
            return "Sistema Inconsistente: Sin Solución (Incompatible)."

        if rango_A < n:
            return "Sistema Consistente Indeterminado: Infinitas Soluciones."

        return "Sistema Consistente Determinado: Presenta Solución Única."

    @staticmethod
    def _solucion_desde_rref(Ab, pivotes, n):
        libres = [col for col in range(n) if col not in pivotes]

        if not libres:
            solucion = []

            for fila_pivote, col_pivote in enumerate(pivotes):
                solucion.append([Ab[fila_pivote][n]])

            return solucion

        expresiones = []

        for fila_pivote, col_pivote in enumerate(pivotes):
            expresion = MatrizModel._expresion_variable(
                Ab[fila_pivote], col_pivote, libres, n
            )
            expresiones.append(expresion)

        for i, col in enumerate(libres, start=1):
            expresiones.append(f"x{col + 1} = t{i}")

        return "\n".join(expresiones)

    @staticmethod
    def _expresion_variable(fila, col_pivote, libres, n):
        base = fila[n]
        partes = []

        if base != 0:
            partes.append(MatrizModel._formatear_factor(base))

        for col in libres:
            coef = -fila[col]

            if coef == 0:
                continue

            nombre = f"t{libres.index(col) + 1}"

            if coef == 1:
                termino = nombre
            elif coef == -1:
                termino = f"- {nombre}"
            else:
                termino = f"{MatrizModel._formatear_factor(abs(coef))}{nombre}"

            if not partes:
                partes.append(termino)
            elif coef > 0:
                partes.append(f"+ {termino}")
            else:
                if coef == -1:
                    partes.append(f"- {nombre}")
                else:
                    partes.append(
                        f"- {MatrizModel._formatear_factor(abs(coef))}{nombre}"
                    )

        if not partes:
            expresion = "0"
        else:
            expresion = " ".join(partes)

        return f"x{col_pivote + 1} = {expresion}"

    @staticmethod
    def _verificacion(A_orig, b_orig, solucion, n):
        if isinstance(solucion, str):
            return "No se realiza verificación numérica porque existen variables libres o el sistema es incompatible."

        x = [solucion[i][0] for i in range(n)]

        texto = "=== VERIFICACIÓN AUTOMÁTICA (Ax = b) ===\n"

        for i in range(len(A_orig)):
            calculado = sum(
                Fraction(str(A_orig[i][j])) * x[j]
                for j in range(n)
            )

            esperado = Fraction(str(b_orig[i][0]))

            calculado_txt = MatrizModel._formatear_factor(calculado)
            esperado_txt = MatrizModel._formatear_factor(esperado)

            texto += (
                f"Ecuación {i + 1}: {calculado_txt} = {esperado_txt} "
                f"-> {'OK' if calculado == esperado else 'ERROR'}\n"
            )

        return texto

    # Gauss
    @staticmethod
    def gauss_resolver_completo(A_orig, b_orig):
        m = len(A_orig)
        n = len(A_orig[0])

        Ab, pivotes, pasos_txt = MatrizModel._forma_escalonada(
            A_orig, b_orig
        )

        clasificacion = MatrizModel._clasificar(Ab, pivotes, n)

        if "Sin Solución" in clasificacion:
            solucion = "SIN SOLUCIÓN (Sistema Incompatible)"
            verificacion_txt = (
                "El sistema contiene una ecuación imposible del tipo 0 = b, "
                "con b diferente de cero."
            )
            return pasos_txt, clasificacion, solucion, verificacion_txt

        if len(pivotes) < n:
            Ab_rref, pivotes_rref, pasos_rref = MatrizModel._forma_escalonada_reducida(
                A_orig, b_orig
            )

            solucion = MatrizModel._solucion_desde_rref(
                Ab_rref, pivotes_rref, n
            )

            verificacion_txt = (
                "Variables libres detectadas.\n"
                "La solución general se expresa mediante parámetros.\n"
                + MatrizModel._verificacion(
                    A_orig, b_orig, solucion, n
                )
            )

            return pasos_txt, clasificacion, solucion, verificacion_txt

        solucion = [None] * n

        for i in range(len(pivotes) - 1, -1, -1):
            col = pivotes[i]
            suma = Ab[i][n]

            for j in range(col + 1, n):
                suma -= Ab[i][j] * solucion[j]

            solucion[col] = suma / Ab[i][col]

        solucion = [[valor] for valor in solucion]

        verificacion_txt = MatrizModel._verificacion(
            A_orig, b_orig, solucion, n
        )

        return pasos_txt, clasificacion, solucion, verificacion_txt

    # Gauss-Jordan
    @staticmethod
    def metodo_gauss_jordan(A_orig, b_orig):
        m = len(A_orig)
        n = len(A_orig[0])

        Ab, pivotes, pasos_txt = MatrizModel._forma_escalonada_reducida(
            A_orig, b_orig
        )

        clasificacion = MatrizModel._clasificar(Ab, pivotes, n)

        if "Sin Solución" in clasificacion:
            solucion = "SIN SOLUCIÓN (Sistema Incompatible)"
            verificacion_txt = (
                "El sistema contiene una ecuación imposible del tipo 0 = b, "
                "con b diferente de cero."
            )

        else:
            solucion = MatrizModel._solucion_desde_rref(
                Ab, pivotes, n
            )

            verificacion_txt = (
                f"Columnas pivote: {', '.join(str(col + 1) for col in pivotes)}\n"
                f"Columnas libres: "
                f"{', '.join(str(col + 1) for col in range(n) if col not in pivotes) or 'Ninguna'}\n\n"
                + MatrizModel._verificacion(
                    A_orig, b_orig, solucion, n
                )
            )

        return pasos_txt, clasificacion, solucion, verificacion_txt

    # Reducción de pivotes
    @staticmethod
    def reduccion_pivotes(A_orig, b_orig):
        Ab, pivotes, pasos_txt = MatrizModel._forma_escalonada(
            A_orig, b_orig
        )

        n = len(A_orig[0])
        clasificacion = MatrizModel._clasificar(Ab, pivotes, n)

        pivotes_txt = (
            "=== INFORMACIÓN DE PIVOTES ===\n"
            f"Columnas pivote: "
            f"{', '.join(str(col + 1) for col in pivotes) or 'Ninguna'}\n"
            f"Columnas libres: "
            f"{', '.join(str(col + 1) for col in range(n) if col not in pivotes) or 'Ninguna'}\n\n"
        )

        pasos_txt = pivotes_txt + pasos_txt

        return pasos_txt, clasificacion, Ab, (
            "La matriz mostrada corresponde a la forma escalonada obtenida "
            "mediante reducción por filas."
        )

    # Formato de salida
    @staticmethod
    def formato_matriz_str(matriz, titulo=""):
        texto = f"--- {titulo} ---\n" if titulo else ""

        for fila in matriz:
            valores = []

            for val in fila:
                if isinstance(val, Fraction):
                    if val.denominator == 1:
                        valores.append(str(val.numerator))
                    else:
                        valores.append(f"{val.numerator}/{val.denominator}")
                else:
                    valores.append(f"{val:.2f}")

            if valores:
                coefs = "  ".join([f"{val:>8}" for val in valores[:-1]])
                b_val = f"{valores[-1]:>8}"
                texto += f"[ {coefs}  | {b_val} ]\n"

        return texto + "\n"

    #convertir de Binario a Decimal
    @staticmethod
    def binario_a_decimal():
        numEnBinario = []
        print("ingrese el nuemero binario que desea convertir a decimal")
        binario = input()

        for bit in binario:  #Convierte de string a int y lo guarda en la lista
            numEnBinario.append(int(bit))

        decimal = 0

        for i, bit in enumerate(reversed(numEnBinario)):
            decimal += bit * (2 ** i)

        return decimal


class OperacionesMatriz:
    """Compatibilidad con el controlador anterior."""

    @staticmethod
    def sumar(m1, m2):
        return MatrizModel.sumar([m1, m2])

    @staticmethod
    def restar(m1, m2):
        return MatrizModel.restar([m1, m2])

    @staticmethod
    def multiplicar(m1, m2):
        return MatrizModel.multiplicar([m1, m2])
