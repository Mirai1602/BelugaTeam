from fractions import Fraction

class CalculadoraDeterminantes:
    """Clase orientada a calcular determinantes paso a paso usando únicamente Python puro."""

    @staticmethod
    def determinante_2x2(matriz):
        """Calcula el determinante de una matriz 2x2."""
        a, b = matriz[0][0], matriz[0][1]
        c, d = matriz[1][0], matriz[1][1]
        
        det = (a * d) - (b * c)
        pasos = [
            "Fórmula 2x2: (a * d) - (b * c)",
            f"= ({a:.2f} * {d:.2f}) - ({b:.2f} * {c:.2f})",
            f"= {a*d:.2f} - {b*c:.2f}",
            f"= {det:.4f}"
        ]
        return det, "\n".join(pasos)

    @staticmethod
    def obtener_submatriz(matriz, fila_eliminar, col_eliminar):
        """Devuelve una submatriz eliminando la fila y columna indicadas."""
        sub = []
        for i, fila in enumerate(matriz):
            if i == fila_eliminar:
                continue
            nueva_fila = [val for j, val in enumerate(fila) if j != col_eliminar]
            sub.append(nueva_fila)
        return sub

    @classmethod
    def determinante_cofactores(cls, matriz):
        """Calcula el determinante mediante el desarrollo por cofactores (recursivo)."""
        n = len(matriz)

        if n == 1:
            return matriz[0][0], f"Det = {matriz[0][0]:.4f}"

        if n == 2:
            return cls.determinante_2x2(matriz)

        det = 0.0
        pasos = [f"Desarrollo por cofactores en la primera fila (matriz {n}x{n}):"]

        for j in range(n):
            submatriz = cls.obtener_submatriz(matriz, 0, j)
            signo = 1 if (0 + j) % 2 == 0 else -1
            sub_det, _ = cls.determinante_cofactores(submatriz)
            
            termino = signo * matriz[0][j] * sub_det
            det += termino

            str_signo = "+1" if signo == 1 else "-1"
            pasos.append(
                f"Elemento A[0][{j}] = {matriz[0][j]:.2f} | Signo = {str_signo} | "
                f"Subdet = {sub_det:.2f} -> Término = {termino:.2f}"
            )

        pasos.append(f"\nDeterminante Total = {det:.4f}")
        return det, "\n".join(pasos)

    @staticmethod
    def determinante_gauss(matriz):
        """Calcula el determinante reduciendo la matriz a forma triangular superior."""
        n = len(matriz)
        # Crear una copia profunda de la matriz
        A = [fila[:] for fila in matriz]

        pasos = ["Transformación a forma triangular superior mediante eliminación gaussiana:"]
        det_mult = 1.0  # Rastreo de signos por intercambios de fila

        for i in range(n):
            # Pivoteo parcial si el elemento diagonal es 0
            if abs(A[i][i]) < 1e-12:
                swap_idx = -1
                for k in range(i + 1, n):
                    if abs(A[k][i]) > 1e-12:
                        swap_idx = k
                        break
                
                if swap_idx == -1:
                    pasos.append(f"Columna {i+1} no tiene pivote no nulo -> det = 0")
                    return 0.0, "\n".join(pasos)

                # Intercambiar filas (cambia el signo del determinante)
                A[i], A[swap_idx] = A[swap_idx], A[i]
                det_mult *= -1.0
                pasos.append(f"Intercambio de Fila {i+1} y Fila {swap_idx+1} (multiplica det por -1)")

            # Eliminación hacia abajo
            for k in range(i + 1, n):
                factor = A[k][i] / A[i][i]
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
                pasos.append(f"Fila {k+1} = Fila {k+1} - ({factor:.2f}) * Fila {i+1}")

        # El determinante de la matriz triangular es el producto de su diagonal
        diag_prod = 1.0
        for i in range(n):
            diag_prod *= A[i][i]

        det = det_mult * diag_prod

        pasos.append("\nMatriz Triangular Resultante:")
        for fila in A:
            pasos.append("[" + ", ".join(f"{elem:8.2f}" for elem in fila) + "]")
            
        pasos.append(f"\nProducto de la diagonal principal = {diag_prod:.4f}")
        pasos.append(f"Factor de signo (intercambios) = {det_mult}")
        pasos.append(f"Determinante Final = {det:.4f}")

        return det, "\n".join(pasos)

    