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
    def valor(valor):
        if isinstance(valor, Fraction):
            return str(valor.numerator) if valor.denominator == 1 else f"{valor.numerator}/{valor.denominator}"
        return str(valor)

    @staticmethod
    def formato_vector(vector):
        return "(" + ", ".join(VectorModel.valor(x) for x in vector) + ")"

    @staticmethod
    def _formatear_matriz(matriz):
        lineas = []
        for fila in matriz:
            valores = [VectorModel.valor(v) for v in fila]
            lineas.append("   [ " + "  ".join(f"{v:>6}" for v in valores) + " ]")
        return "\n".join(lineas)

    @staticmethod
    def suma(a, b):
        VectorModel.validar_misma_dimension(a, b)
        
        pasos = [
            "=== SUMA DE VECTORES PASO A PASO ===",
            f"Vector A = {VectorModel.formato_vector(a)}",
            f"Vector B = {VectorModel.formato_vector(b)}",
            "\n1. REGLA GENERAL:",
            "   La suma se realiza sumando las componentes correspondientes: (A_i + B_i)",
            "\n2. DESARROLLO POR COMPONENTES:"
        ]
        
        resultado = []
        for i, (x, y) in enumerate(zip(a, b)):
            res_comp = x + y
            resultado.append(res_comp)
            pasos.append(f"   • Componente {i+1}: {VectorModel.valor(x)} + {VectorModel.valor(y)} = {VectorModel.valor(res_comp)}")
        
        pasos.append(f"\n3. RESULTADO FINAL: A + B = {VectorModel.formato_vector(resultado)}")
        
        return {
            "resultado": resultado,
            "pasos": "\n".join(pasos)
        }

    @staticmethod
    def resta(a, b):
        VectorModel.validar_misma_dimension(a, b)
        
        pasos = [
            "=== RESTA DE VECTORES PASO A PASO ===",
            f"Vector A = {VectorModel.formato_vector(a)}",
            f"Vector B = {VectorModel.formato_vector(b)}",
            "\n1. REGLA GENERAL:",
            "   La resta se realiza sustrayendo las componentes correspondientes: (A_i - B_i)",
            "\n2. DESARROLLO POR COMPONENTES:"
        ]
        
        resultado = []
        for i, (x, y) in enumerate(zip(a, b)):
            res_comp = x - y
            resultado.append(res_comp)
            pasos.append(f"   • Componente {i+1}: {VectorModel.valor(x)} - ({VectorModel.valor(y)}) = {VectorModel.valor(res_comp)}")
        
        pasos.append(f"\n3. RESULTADO FINAL: A - B = {VectorModel.formato_vector(resultado)}")
        
        return {
            "resultado": resultado,
            "pasos": "\n".join(pasos)
        }

    @staticmethod
    def escalar(vector, factor):
        k = VectorModel.a_fraction(factor)
        
        pasos = [
            "=== MULTIPLICACIÓN POR ESCALAR PASO A PASO ===",
            f"Vector v = {VectorModel.formato_vector(vector)}",
            f"Escalar k = {VectorModel.valor(k)}",
            "\n1. REGLA GENERAL:",
            "   Cada componente del vector se multiplica por el escalar: k · v_i",
            "\n2. DESARROLLO POR COMPONENTES:"
        ]
        
        resultado = []
        for i, x in enumerate(vector):
            res_comp = k * x
            resultado.append(res_comp)
            pasos.append(f"   • Componente {i+1}: {VectorModel.valor(k)} · ({VectorModel.valor(x)}) = {VectorModel.valor(res_comp)}")
        
        pasos.append(f"\n3. RESULTADO FINAL: k · v = {VectorModel.formato_vector(resultado)}")
        
        return {
            "resultado": resultado,
            "pasos": "\n".join(pasos)
        }

    @staticmethod
    def _gauss_jordan_con_pasos(matriz, cantidad_variables):
        matriz = [fila[:] for fila in matriz]
        filas = len(matriz)
        columnas = cantidad_variables
        pivotes = []
        fila_pivote = 0
        historial = []

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

            if encontrado != fila_pivote:
                matriz[fila_pivote], matriz[encontrado] = matriz[encontrado], matriz[fila_pivote]
                historial.append(f"• Intercambio R{fila_pivote+1} <-> R{encontrado+1}:")
                historial.append(VectorModel._formatear_matriz(matriz))

            pivote = matriz[fila_pivote][columna]
            if pivote != 1:
                matriz[fila_pivote] = [valor / pivote for valor in matriz[fila_pivote]]
                historial.append(f"• Normalizar R{fila_pivote+1} (R{fila_pivote+1} / {VectorModel.valor(pivote)}):")
                historial.append(VectorModel._formatear_matriz(matriz))

            for i in range(filas):
                if i == fila_pivote:
                    continue
                factor = matriz[i][columna]
                if factor != 0:
                    matriz[i] = [
                        matriz[i][j] - factor * matriz[fila_pivote][j]
                        for j in range(columnas + 1)
                    ]
                    historial.append(f"• R{i+1} -> R{i+1} - ({VectorModel.valor(factor)})*R{fila_pivote+1}:")
                    historial.append(VectorModel._formatear_matriz(matriz))

            pivotes.append(columna)
            fila_pivote += 1

        return matriz, pivotes, historial

    @staticmethod
    def combinacion_lineal(generadores, objetivo):
        if not generadores:
            raise ValueError("Debe existir al menos un vector generador.")
        VectorModel.validar_misma_dimension(*generadores, objetivo)

        filas = len(objetivo)
        cantidad = len(generadores)
        aumentada = []
        pasos = ["=== COMBINACION LINEAL PASO A PASO ===", "\n1. PLANTEAMIENTO DEL SISTEMA:"]

        term_str = " + ".join([f"c{i+1}*v{i+1}" for i in range(cantidad)])
        pasos.append(f"   Ecuacion buscada: {term_str} = b")
        for i, g in enumerate(generadores):
            pasos.append(f"   v{i+1} = {VectorModel.formato_vector(g)}")
        pasos.append(f"   b  = {VectorModel.formato_vector(objetivo)}")

        for i in range(filas):
            fila = [generadores[j][i] for j in range(cantidad)]
            fila.append(objetivo[i])
            aumentada.append(fila)

        pasos.append("\n2. MATRIZ AUMENTADA INICIAL [A | b]:")
        pasos.append(VectorModel._formatear_matriz(aumentada))

        rref, pivotes, historial_gauss = VectorModel._gauss_jordan_con_pasos(aumentada, cantidad)
        
        pasos.append("\n3. PROCESO DE ELIMINACION DE GAUSS-JORDAN:")
        if historial_gauss:
            pasos.extend(historial_gauss)
        else:
            pasos.append("   (La matriz ya se encuentra en su forma reducida).")

        pasos.append("\n4. MATRIZ REDUCIDA POR FILAS FINAL (RREF):")
        pasos.append(VectorModel._formatear_matriz(rref))

        pasos.append("\n5. EVALUACION DIDACTICA Y CONCLUSION:")

        inconsistencias = []
        for i, fila in enumerate(rref):
            if all(fila[j] == 0 for j in range(cantidad)) and fila[cantidad] != 0:
                inconsistencias.append((i + 1, fila[cantidad]))

        if inconsistencias:
            for fila_num, val_b in inconsistencias:
                pasos.append(f"   INCONSISTENCIA EN FILA {fila_num}: 0 = {VectorModel.valor(val_b)}")
            
            pasos.append("\n   EXPLICACION:")
            pasos.append("    Al reducir la matriz se llega a una contradiccion matematica (0 igual a un valor no nulo).")
            pasos.append("    Esto significa que el sistema de ecuaciones NO tiene solucion.")
            pasos.append("    Por lo tanto, el vector objetivo 'b' NO se puede expresar como combinacion lineal del conjunto de generadores.")
            
            return {
                "es_combinacion": False,
                "clasificacion": "No es combinacion lineal: sistema incompatible.",
                "coeficientes": None,
                "pasos": "\n".join(pasos)
            }

        if len(pivotes) < cantidad:
            pasos.append("   VARIABLES LIBRES DETECTADAS:")
            pasos.append("    El sistema tiene infinitas soluciones. Existen multiples combinaciones lineales posibles.")
            return {
                "es_combinacion": True,
                "clasificacion": "Si es combinacion lineal (Infinitas soluciones).",
                "coeficientes": "Infinitos coeficientes posibles.",
                "pasos": "\n".join(pasos)
            }

        coeficientes = [Fraction(0) for _ in range(cantidad)]
        for fila, columna in enumerate(pivotes):
            if columna < cantidad:
                coeficientes[columna] = rref[fila][cantidad]

        coefs_fmt = [VectorModel.valor(c) for c in coeficientes]
        pasos.append("   SISTEMA COMPATIBLE DETERMINADO:")
        pasos.append(f"    Los coeficientes unicos hallados son: c = ({', '.join(coefs_fmt)})")

        return {
            "es_combinacion": True,
            "clasificacion": "Si es combinacion lineal.",
            "coeficientes": coeficientes,
            "pasos": "\n".join(pasos)
        }