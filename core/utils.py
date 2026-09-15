#Todas las funciones que se encuentran en este archivo son funciones de utilidad que se utilizan en diferentes partes del programa. Estas funciones ayudan a realizar tareas comunes, como convertir una tabla de PyQt a una lista de Python, lo que facilita el manejo de los datos en la aplicación.

def convertir_a_lista(qtable):
    filas = qtable.rowCount()
    columnas = qtable.columnCount()
    matriz = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            item = qtable.item(i, j)
            fila.append(float(item.text()) if item else 0)
        matriz.append(fila)
    return matriz


