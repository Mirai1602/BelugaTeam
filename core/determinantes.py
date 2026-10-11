# core/determinantes.py

from fractions import Fraction


def renderizar_matriz_texto(matriz, titulo=""):
    """Dibuja una matriz alineada con bordes en texto plano."""
    lineas = []
    if titulo:
        lineas.append(f"  {titulo}:")

    if not matriz or not matriz[0]:
        return ""

    num_cols = len(matriz[0])
    anchos = []
    for j in range(num_cols):
        max_len = max(len(f"{matriz[i][j]:g}") for i in range(len(matriz)))
        anchos.append(max(max_len, 3))

    for fila in matriz:
        elementos = [f"{val:g}".rjust(anchos[j]) for j, val in enumerate(fila)]
        lineas.append("  │ " + "  ".join(elementos) + " │")

    return "\n".join(lineas)


class CalculadoraDeterminantes:
    """Calculadora pedagógica que genera el paso a paso con matrices para ambos métodos."""

    @staticmethod
    def obtener_submatriz(matriz, fila_eliminar, col_eliminar):
        """Devuelve la submatriz eliminando una fila y columna."""
        return [
            [elem for j, elem in enumerate(fila) if j != col_eliminar]
            for i, fila in enumerate(matriz) if i != fila_eliminar
        ]

    @classmethod
    def _det_recursivo_puro(cls, matriz):
        """Cálculo directo para obtener valores numéricos de submatrices."""
        n = len(matriz)
        if n == 1:
            return matriz[0][0]
        if n == 2:
            return (matriz[0][0] * matriz[1][1]) - (matriz[0][1] * matriz[1][0])
        
        det = 0.0
        for j in range(n):
            signo = 1 if j % 2 == 0 else -1
            sub = cls.obtener_submatriz(matriz, 0, j)
            det += signo * matriz[0][j] * cls._det_recursivo_puro(sub)
        return det

    @classmethod
    def determinante_cofactores(cls, matriz):
        """Genera la explicación paso a paso por cofactores dibujando submatrices."""
        n = len(matriz)

        if n == 1:
            val = matriz[0][0]
            return val, f"Matriz 1x1:\nDeterminante = {val:g}"

        if n == 2:
            a, b = matriz[0][0], matriz[0][1]
            c, d = matriz[1][0], matriz[1][1]
            det = (a * d) - (b * c)
            pasos = [
                "==========================================================",
                " MÉTODO DIRECTO (MATRIZ 2x2)",
                "==========================================================\n",
                renderizar_matriz_texto(matriz, "Matriz inicial A"),
                "\n PASO 1: Identificar los elementos",
                f"  • Diagonal principal (a, d)  = {a:g}, {d:g}",
                f"  • Diagonal secundaria (b, c) = {b:g}, {c:g}",
                "\n PASO 2: Multiplicar diagonales",
                f"  • (a × d) = {a:g} × {d:g} = {a*d:g}",
                f"  • (b × c) = {b:g} × {c:g} = {b*c:g}",
                "\n PASO 3: Restar los productos",
                f"  • det(A) = (a × d) − (b × c)",
                f"  • det(A) = {a*d:g} − ({b*c:g}) = {det:g}\n",
                "==========================================================",
                f" RESULTADO FINAL: det(A) = {det:g}",
                "=========================================================="
            ]
            return det, "\n".join(pasos)

        pasos = [
            "==========================================================",
            f" DESARROLLO POR COFACTORES (Fila 1) - Matriz {n}x{n}",
            "==========================================================\n",
            renderizar_matriz_texto(matriz, "Matriz Inicial A"),
            "\nFórmula: det(A) = a₁₁·C₁₁ + a₁₂·C₁₂ + ... + a₁ₙ·C₁ₙ\n"
        ]

        det_total = 0.0

        for j in range(n):
            val = matriz[0][j]
            signo = 1 if j % 2 == 0 else -1
            str_signo = "+1" if signo == 1 else "-1"

            submatriz = cls.obtener_submatriz(matriz, 0, j)
            sub_det = cls._det_recursivo_puro(submatriz)
            termino = signo * val * sub_det
            det_total += termino

            pasos.append("----------------------------------------------------------")
            pasos.append(f"PASO {j+1}: Elemento A[1][{j+1}] = {val:g}")
            pasos.append("----------------------------------------------------------")

            if abs(val) < 1e-12:
                pasos.append("   El elemento es 0. Al multiplicar por cero el término se anula,")
                pasos.append("     por lo que no hace falta calcular su submatriz.")
                pasos.append(f"  • Término {j+1} = 0\n")
            else:
                pasos.append(f"  1. Signo del cofactor (-1)¹⁺⁽{j+1}⁾ = {str_signo}")
                pasos.append(f"  2. Eliminamos Fila 1 y Columna {j+1} para obtener la submatriz ({n-1}x{n-1}):\n")
                pasos.append(renderizar_matriz_texto(submatriz, f"Submatriz M₁{j+1} Resultante"))
                pasos.append(f"\n  3. Determinante de la Submatriz M₁{j+1}: det(M) = {sub_det:g}")
                pasos.append(f"  4. Cálculo del Término {j+1}:")
                pasos.append(f"     ({str_signo}) × ({val:g}) × ({sub_det:g}) = {termino:g}\n")

        pasos.append("==========================================================")
        pasos.append(" SUMATORIA FINAL DE TÉRMINOS:")
        pasos.append(f"   det(A) = {det_total:g}")
        pasos.append("==========================================================")

        return det_total, "\n".join(pasos)


    # Añadir dentro de CalculadoraDeterminantes en core/determinantes.py

    @classmethod
    def determinante_sarrus(cls, matriz):
        """Calcula el determinante mediante la Regla de Sarrus (Para 2x2, 3x3 y 4x4)."""
        n = len(matriz)

        if n > 4:
            raise ValueError(
                f"El método Sarrus en BelugaCalc está limitado a máximo 4x4. "
                f"Para una matriz {n}x{n}, debes utilizar Eliminación Gaussiana o Cofactores."
            )

        if n == 2:
            return cls.determinante_2x2(matriz)

        if n == 3:
            a, b, c = matriz[0][0], matriz[0][1], matriz[0][2]
            d, e, f_val = matriz[1][0], matriz[1][1], matriz[1][2]
            g, h, i_val = matriz[2][0], matriz[2][1], matriz[2][2]

            p1, p2, p3 = a * e * i_val, b * f_val * g, c * d * h
            suma_pos = p1 + p2 + p3

            s1, s2, s3 = c * e * g, a * f_val * h, b * d * i_val
            suma_neg = s1 + s2 + s3

            det = suma_pos - suma_neg

            matriz_ext = [
                f"  │ {a:g}  {b:g}  {c:g} │",
                f"  │ {d:g}  {e:g}  {f_val:g} │",
                f"  │ {g:g}  {h:g}  {i_val:g} │",
                "  ├─────────────┤ (Filas ampliadas)",
                f"  │ {a:g}  {b:g}  {c:g} │",
                f"  │ {d:g}  {e:g}  {f_val:g} │"
            ]

            pasos = [
                "==========================================================",
                " REGLA DE SARRUS (Matriz 3x3)",
                "==========================================================\n",
                "Visualización de la matriz con las 2 primeras filas copiadas al final:\n",
                "\n".join(matriz_ext),
                "\n PASO 1: Sumar los productos de las diagonales principales (↘)",
                f"  • Diagonal 1: ({a:g}) × ({e:g}) × ({i_val:g}) = {p1:g}",
                f"  • Diagonal 2: ({b:g}) × ({f_val:g}) × ({g:g}) = {p2:g}",
                f"  • Diagonal 3: ({c:g}) × ({d:g}) × ({h:g}) = {p3:g}",
                f" Suma Principales = {p1:g} + {p2:g} + {p3:g} = {suma_pos:g}",
                "\n PASO 2: Sumar los productos de las diagonales secundarias (↙)",
                f"  • Diagonal 1: ({c:g}) × ({e:g}) × ({g:g}) = {s1:g}",
                f"  • Diagonal 2: ({a:g}) × ({f_val:g}) × ({h:g}) = {s2:g}",
                f"  • Diagonal 3: ({b:g}) × ({d:g}) × ({i_val:g}) = {s3:g}",
                f"   Suma Secundarias = {s1:g} + {s2:g} + {s3:g} = {suma_neg:g}",
                "\n PASO 3: Restar Diagonales Principales − Diagonales Secundarias",
                f"  • det(A) = ({suma_pos:g}) − ({suma_neg:g}) = {det:g}\n",
                "==========================================================",
                f" RESULTADO FINAL: det(A) = {det:g}",
                "=========================================================="
            ]
            return det, "\n".join(pasos)

        # CASO 4x4 (Extensión de Sarrus copiando las primeras 3 filas)
        # Matriz ampliada
        matriz_ext_4x4 = matriz + [matriz[0], matriz[1], matriz[2]]

        # Diagonales Principales (4 de longitud 4)
        p1 = matriz_ext_4x4[0][0] * matriz_ext_4x4[1][1] * matriz_ext_4x4[2][2] * matriz_ext_4x4[3][3]
        p2 = matriz_ext_4x4[1][0] * matriz_ext_4x4[2][1] * matriz_ext_4x4[3][2] * matriz_ext_4x4[4][3]
        p3 = matriz_ext_4x4[2][0] * matriz_ext_4x4[3][1] * matriz_ext_4x4[4][2] * matriz_ext_4x4[5][3]
        p4 = matriz_ext_4x4[3][0] * matriz_ext_4x4[4][1] * matriz_ext_4x4[5][2] * matriz_ext_4x4[6][3]
        suma_pos = p1 + p2 + p3 + p4

        # Diagonales Secundarias (4 de longitud 4)
        s1 = matriz_ext_4x4[0][3] * matriz_ext_4x4[1][2] * matriz_ext_4x4[2][1] * matriz_ext_4x4[3][0]
        s2 = matriz_ext_4x4[1][3] * matriz_ext_4x4[2][2] * matriz_ext_4x4[3][1] * matriz_ext_4x4[4][0]
        s3 = matriz_ext_4x4[2][3] * matriz_ext_4x4[3][2] * matriz_ext_4x4[4][1] * matriz_ext_4x4[5][0]
        s4 = matriz_ext_4x4[3][3] * matriz_ext_4x4[4][2] * matriz_ext_4x4[5][1] * matriz_ext_4x4[6][0]
        suma_neg = s1 + s2 + s3 + s4

        det = suma_pos - suma_neg

        lineas_ext = [renderizar_matriz_texto(matriz, "Matriz Original 4x4"), "  ├─────────────┤ (Filas ampliadas R1-R3)"]
        for row in [matriz[0], matriz[1], matriz[2]]:
            lineas_ext.append("  │ " + "  ".join(f"{x:g}".rjust(3) for x in row) + " │")

        pasos = [
            "==========================================================",
            " MÉTODO DE SARRUS EXTENDIDO (Matriz 4x4)",
            "==========================================================\n",
            "\n".join(lineas_ext),
            "\n PASO 1: Sumar las 4 diagonales principales (↘)",
            f"  • Diag 1 = {p1:g}",
            f"  • Diag 2 = {p2:g}",
            f"  • Diag 3 = {p3:g}",
            f"  • Diag 4 = {p4:g}",
            f"   Suma Principales = {suma_pos:g}",
            "\n PASO 2: Sumar las 4 diagonales secundarias (↙)",
            f"  • Diag 1 = {s1:g}",
            f"  • Diag 2 = {s2:g}",
            f"  • Diag 3 = {s3:g}",
            f"  • Diag 4 = {s4:g}",
            f"   Suma Secundarias = {suma_neg:g}",
            "\n PASO 3: Restar Suma Principales − Suma Secundarias",
            f"  • det(A) = ({suma_pos:g}) − ({suma_neg:g}) = {det:g}\n",
            "   NOTA PEDAGÓGICA: Sarrus extendido en 4x4 es un esquema visual.",
            "  Para análisis formal estricto, se recomienda usar Cofactores o Gauss.\n",
            "==========================================================",
            f" RESULTADO ESTIMADO: det(A) = {det:g}",
            "=========================================================="
        ]

        return det, "\n".join(pasos)
    @staticmethod
    def determinante_gauss(matriz):
        """Genera la explicación por Eliminación Gaussiana mostrando cada matriz resultante."""
        n = len(matriz)
        A = [[Fraction(val).limit_denominator() for val in fila] for fila in matriz]

        pasos = [
            "==========================================================",
            " ELIMINACIÓN GAUSSIANA (Forma Triangular Superior)",
            "==========================================================\n",
            "Objetivo: Convertir los elementos debajo de la diagonal en cero.",
            "Cada cambio en la matriz se muestra a continuación:\n",
            renderizar_matriz_texto([[float(x) for x in f] for f in A], "Matriz Inicial A"),
            "\n" + "=" * 58
        ]

        det_mult = Fraction(1, 1)
        paso_num = 1

        for i in range(n):
            if A[i][i] == 0:
                swap_idx = -1
                for k in range(i + 1, n):
                    if A[k][i] != 0:
                        swap_idx = k
                        break

                if swap_idx == -1:
                    pasos.append(f"\n PASO {paso_num}: La columna {i+1} no tiene pivote no nulo.")
                    pasos.append("   det(A) = 0")
                    return 0.0, "\n".join(pasos)

                A[i], A[swap_idx] = A[swap_idx], A[i]
                det_mult *= -1
                pasos.append(f"\n PASO {paso_num}: Intercambiar Fila {i+1} ↔ Fila {swap_idx+1}")
                pasos.append("    Regla: Intercambiar dos filas multiplica det por -1.\n")
                pasos.append(renderizar_matriz_texto([[float(x) for x in f] for f in A], "Matriz resultante"))
                paso_num += 1

            pivote = A[i][i]
            for k in range(i + 1, n):
                if A[k][i] != 0:
                    factor = A[k][i] / pivote
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]

                    valor_factor = float(factor)
                    pasos.append(f"\n PASO {paso_num}: Hacer 0 el elemento A[{k+1}][{i+1}]")
                    pasos.append(f"  • Operación: Fila {k+1} = Fila {k+1} − ({valor_factor:g}) × Fila {i+1}\n")
                    pasos.append(renderizar_matriz_texto([[float(x) for x in f] for f in A], "Estado actual de la matriz"))
                    paso_num += 1

        diag_prod = Fraction(1, 1)
        elementos_diag = []
        for i in range(n):
            diag_prod *= A[i][i]
            elementos_diag.append(f"{float(A[i][i]):g}")

        det_final = det_mult * diag_prod

        pasos.append("\n==========================================================")
        pasos.append("PASO FINAL: MATRIZ TRIANGULAR ALCANZADA")
        pasos.append("==========================================================\n")
        pasos.append(renderizar_matriz_texto([[float(x) for x in f] for f in A], "Matriz Triangular Superior"))
        pasos.append("\n1. Producto de la diagonal principal:")
        pasos.append(f"   {' × '.join(elementos_diag)} = {float(diag_prod):g}")

        if det_mult != 1:
            pasos.append("\n2. Ajuste de signo por intercambios de fila:")
            pasos.append(f"   ({float(diag_prod):g}) × ({float(det_mult):g}) = {float(det_final):g}")

        pasos.append("==========================================================")
        pasos.append(f" RESULTADO FINAL: det(A) = {float(det_final):g}")
        pasos.append("==========================================================")

        return float(det_final), "\n".join(pasos)

    

    @classmethod
    def regla_cramer(cls, matriz_A, vector_b):
        """
        Resuelve un sistema A*x = b mediante la Regla de Cramer,
        mostrando el determinante principal D y cada subdeterminante Dx_i.
        """
        n = len(matriz_A)
        
        # 1. Determinante Principal D
        det_A, _ = cls.determinante_cofactores(matriz_A)
        
        pasos = [
            "==========================================================",
            f" REGLA DE CRAMER (Sistema {n}x{n})",
            "==========================================================\n",
            renderizar_matriz_texto(matriz_A, "Matriz Coeficientes A"),
            f"\nVector Términos Independientes b = [ {', '.join(f'{x:g}' for x in vector_b)} ]",
            "\n PASO 1: Calcular el Determinante Principal (D)",
            f"  • D = det(A) = {det_A:g}\n"
        ]

        if abs(det_A) < 1e-12:
            pasos.append(" EL DETERMINANTE PRINCIPAL D ES IGUAL A 0.")
            pasos.append("   • Según la Regla de Cramer, si D = 0 el sistema NO tiene solución única")
            pasos.append("     (puede ser Incompatible sin solución o Compatible Indeterminado con infinitas soluciones).")
            pasos.append("==========================================================")
            return None, "\n".join(pasos)

        pasos.append(" PASO 2: Reemplazar el vector b en cada columna y calcular Dx_i\n")
        
        soluciones = []

        for col in range(n):
            # Crear matriz A_i reemplazando la columna col por vector_b
            matriz_Ai = [fila[:] for fila in matriz_A]
            for fila in range(n):
                matriz_Ai[fila][col] = vector_b[fila]

            det_Ai, _ = cls.determinante_cofactores(matriz_Ai)
            val_var = det_Ai / det_A
            soluciones.append(val_var)

            pasos.append(f"--- Incógnita x_{col+1} ---")
            pasos.append(renderizar_matriz_texto(matriz_Ai, f"Matriz A_{col+1} (Reemplazada Columna {col+1})"))
            pasos.append(f"  • D_{col+1} = det(A_{col+1}) = {det_Ai:g}")
            pasos.append(f"  • x_{col+1} = D_{col+1} / D = {det_Ai:g} / {det_A:g} = {val_var:g}\n")

        pasos.append("==========================================================")
        pasos.append(" SOLUCIÓN DEL SISTEMA:")
        for idx, sol in enumerate(soluciones):
            pasos.append(f"   • x_{idx+1} = {sol:g}")
        pasos.append("==========================================================")

        return soluciones, "\n".join(pasos)