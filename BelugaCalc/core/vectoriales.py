class OperacionesVectoriales:
    @staticmethod
    def producto_punto(u, v):
        # Verificamos que tengan la misma dimensión
        if len(u) != len(v):
            raise ValueError("Los vectores deben tener la misma dimensión")
        resultado = 0
        for i in range(len(u)):
            resultado += u[i] * v[i]
        return resultado

    @staticmethod
    def producto_cruz(u, v):
        # Solo definido en R^3
        if len(u) != 3 or len(v) != 3:
            raise ValueError("El producto cruz solo está definido en R^3")
        return [
            u[1]*v[2] - u[2]*v[1],
            u[2]*v[0] - u[0]*v[2],
            u[0]*v[1] - u[1]*v[0]
        ]

    @staticmethod
    def vector_norma(u):
        # Norma = raíz cuadrada de la suma de cuadrados
        suma_cuadrados = 0
        for x in u:
            suma_cuadrados += x * x

        # Implementamos sqrt manualmente (método de Newton)
        if suma_cuadrados == 0:
            return 0
        aprox = suma_cuadrados / 2
        for _ in range(20):  # iteraciones para mejorar precisión
            aprox = (aprox + suma_cuadrados / aprox) / 2
        return aprox

    @staticmethod
    def angulo_vectores(u, v):
        if len(u) != len(v):
            raise ValueError("Los vectores deben tener la misma dimensión")

        dot = OperacionesVectoriales.producto_punto(u, v)
        norma_u = OperacionesVectoriales.vector_norma(u)
        norma_v = OperacionesVectoriales.vector_norma(v)

        if norma_u == 0 or norma_v == 0:
            raise ValueError("No se puede calcular el ángulo con un vector nulo")

        cos_theta = dot / (norma_u * norma_v)

        # Limitar cos_theta entre -1 y 1
        if cos_theta > 1: cos_theta = 1
        if cos_theta < -1: cos_theta = -1

        # Aproximación de arccos usando serie de Taylor (simplificada)
        # arccos(x) ≈ π/2 - (x + x^3/6 + 3x^5/40)
        pi = 3.141592653589793
        x = cos_theta
        angulo_rad = pi/2 - (x + (x**3)/6 + (3*(x**5))/40)

        # Convertimos a grados manualmente
        return angulo_rad * (180 / pi)
