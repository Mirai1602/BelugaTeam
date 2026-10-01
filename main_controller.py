from core.operaciones import OperacionesMatriz
from core.utils import convertir_a_lista


class MainController:
    def __init__(self, ui):
        self.ui = ui

        if hasattr(self.ui, "btnSumar"):
            self.ui.btnSumar.clicked.connect(self.sumar_matrices)

    def sumar_matrices(self):
        m1 = convertir_a_lista(self.ui.tableMatriz1)
        m2 = convertir_a_lista(self.ui.tableMatriz2)
        resultado = OperacionesMatriz.sumar(m1, m2)
        self.mostrar_resultado(resultado, self.ui.tableResultado)

    def mostrar_resultado(self, matriz, tabla):
        filas, columnas = len(matriz), len(matriz[0])
        tabla.setRowCount(filas)
        tabla.setColumnCount(columnas)

        for i in range(filas):
            for j in range(columnas):
                from PyQt6.QtWidgets import QTableWidgetItem
                tabla.setItem(i, j, QTableWidgetItem(str(matriz[i][j])))
