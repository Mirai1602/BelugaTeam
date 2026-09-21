# core/matriz.py
#Esto no lo tenía el codigo original
class Matriz:
    def __init__(self, datos):
        """
        datos: lista de listas con los valores de la matriz
        Ejemplo: [[1,2],[3,4]]
        """
        self.datos = datos

    def filas(self):
        """Devuelve el número de filas"""
        return len(self.datos)

    def columnas(self):
        """Devuelve el número de columnas"""
        return len(self.datos[0]) if self.datos else 0

    def obtener_valor(self, fila, columna):
        """Obtiene un valor en una posición específica"""
        return self.datos[fila][columna]

    def establecer_valor(self, fila, columna, valor):
        """Cambia un valor en una posición específica"""
        self.datos[fila][columna] = valor

    def __str__(self):
        """Representación en texto de la matriz"""
        return "\n".join(["\t".join(map(str, fila)) for fila in self.datos])
