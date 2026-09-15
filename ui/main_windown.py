import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSpinBox, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QScrollArea, QTextEdit
)
from PyQt6.QtCore import Qt


class CalculadoraMatrices(QWidget):
    def _init_(self):
        super()._init_()
        self.setWindowTitle("Calculadora de Álgebra Lineal - UAM")
        self.resize(1000, 750)
        self.tablas = []
        self.init_ui()

    def init_ui(self):
        layout_principal = QVBoxLayout()

        control_layout = QHBoxLayout()
        control_layout.setSpacing(15)

        grupo_filas = QHBoxLayout()
        grupo_filas.setSpacing(6)
        grupo_filas.addWidget(QLabel("<b>Filas (m):</b>"))
        self.spin_filas = QSpinBox()
        self.spin_filas.setRange(1, 10)
        self.spin_filas.setValue(3)
        self.spin_filas.setFixedWidth(85)
        grupo_filas.addWidget(self.spin_filas)
        control_layout.addLayout(grupo_filas)

        grupo_cols = QHBoxLayout()
        grupo_cols.setSpacing(6)
        grupo_cols.addWidget(QLabel("<b>Columnas (n):</b>"))
        self.spin_columnas = QSpinBox()
        self.spin_columnas.setRange(1, 10)
        self.spin_columnas.setValue(4)
        self.spin_columnas.setFixedWidth(85)
        grupo_cols.addWidget(self.spin_columnas)
        control_layout.addLayout(grupo_cols)

        grupo_tablas = QHBoxLayout()
        grupo_tablas.setSpacing(6)
        grupo_tablas.addWidget(QLabel("<b>N° de Tablas:</b>"))
        self.spin_num_tablas = QSpinBox()
        self.spin_num_tablas.setRange(1, 5)
        self.spin_num_tablas.setValue(1)
        self.spin_num_tablas.setFixedWidth(85)
        grupo_tablas.addWidget(self.spin_num_tablas)
        control_layout.addLayout(grupo_tablas)

        btn_generar = QPushButton("Generar Tablas")
        btn_generar.clicked.connect(self.generar_tablas)
        control_layout.addWidget(btn_generar)

        btn_limpiar = QPushButton("🧹 Limpiar")
        btn_limpiar.clicked.connect(self.limpiar_tablas)
        control_layout.addWidget(btn_limpiar)

        control_layout.addStretch()
        layout_principal.addLayout(control_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.contenedor_tablas = QWidget()
        self.tablas_layout = QHBoxLayout(self.contenedor_tablas)
        self.tablas_layout.setSpacing(20)
        self.scroll_area.setWidget(self.contenedor_tablas)
        layout_principal.addWidget(self.scroll_area)

        ops_layout = QHBoxLayout()
        
        btn_suma = QPushButton("Suma (+)")
        btn_suma.clicked.connect(lambda: self.ejecutar_operacion("+"))
        ops_layout.addWidget(btn_suma)

        btn_resta = QPushButton("Resta (-)")
        btn_resta.clicked.connect(lambda: self.ejecutar_operacion("-"))
        ops_layout.addWidget(btn_resta)

        btn_mult = QPushButton("Multiplicación (*)")
        btn_mult.clicked.connect(lambda: self.ejecutar_operacion("*"))
        ops_layout.addWidget(btn_mult)

        btn_gauss = QPushButton("Resolver Gauss")
        btn_gauss.clicked.connect(self.ejecutar_gauss)
        ops_layout.addWidget(btn_gauss)

        layout_principal.addLayout(ops_layout)

        layout_principal.addWidget(QLabel("<b>Vector Solución (x):</b>"))
        self.tabla_res = QTableWidget()
        self.tabla_res.setMaximumHeight(100)
        layout_principal.addWidget(self.tabla_res)

        layout_principal.addWidget(QLabel("<b>Procedimiento Paso a Paso y Clasificación:</b>"))
        self.txt_bitacora = QTextEdit()
        self.txt_bitacora.setReadOnly(True)
        layout_principal.addWidget(self.txt_bitacora)

        self.setLayout(layout_principal)
        self.generar_tablas()

    def generar_tablas(self):
        for i in reversed(range(self.tablas_layout.count())):
            widget = self.tablas_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        
        self.tablas.clear()
        f = self.spin_filas.value()
        c = self.spin_columnas.value()
        num_tablas = self.spin_num_tablas.value()
        letras = ["A (Aumentada/Coefs)", "B (Indep)", "C", "D", "E"]

        for i in range(num_tablas):
            box = QVBoxLayout()
            box.addWidget(QLabel(f"<b>Matriz {letras[i]}</b>"))
            
            tabla = QTableWidget()
            tabla.setRowCount(f)
            tabla.setColumnCount(1 if (num_tablas >= 2 and i == 1) else c)
            box.addWidget(tabla)
            
            w = QWidget()
            w.setLayout(box)
            self.tablas_layout.addWidget(w)
            self.tablas.append(tabla)

    def limpiar_tablas(self):
        for tabla in self.tablas + [self.tabla_res]:
            tabla.clearContents()
        self.txt_bitacora.clear()

    def leer_matriz(self, tabla):
        filas = tabla.rowCount()
        columnas = tabla.columnCount()
        matriz = []
        for i in range(filas):
            fila = []
            for j in range(columnas):
                item = tabla.item(i, j)
                val = float(item.text()) if item and item.text().strip() != "" else 0.0
                fila.append(val)
            matriz.append(fila)
        return matriz

    def mostrar_resultado(self, matriz_res):
        self.tabla_res.clear()
        
        # Caso 1: Cadena de texto (Sin solución / Infinitas soluciones)
        if isinstance(matriz_res, str):
            self.tabla_res.setRowCount(1)
            self.tabla_res.setColumnCount(1)
            item = QTableWidgetItem(matriz_res)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabla_res.setItem(0, 0, item)
            self.tabla_res.setSpan(0, 0, 1, 1)
            return

        # Caso 2: Sin datos o None
        if not matriz_res:
            self.tabla_res.setRowCount(0)
            self.tabla_res.setColumnCount(0)
            return
        
        # Caso 3: Matriz de valores numéricos (Solución única)
        filas = len(matriz_res)
        columnas = len(matriz_res[0])
        self.tabla_res.setRowCount(filas)
        self.tabla_res.setColumnCount(columnas)
        
        for i in range(filas):
            for j in range(columnas):
                val = str(round(matriz_res[i][j], 4))
                self.tabla_res.setItem(i, j, QTableWidgetItem(val))

    def ejecutar_operacion(self, operacion):
        try:
            if len(self.tablas) < 2:
                QMessageBox.warning(self, "Error", "Se necesitan al menos 2 tablas para realizar operaciones aritméticas.")
                return

            matrices = [self.leer_matriz(t) for t in self.tablas]
            f_base, c_base = len(matrices[0]), len(matrices[0][0])

            if operacion in ["+", "-"]:
                for m in matrices[1:]:
                    if len(m) != f_base or len(m[0]) != c_base:
                        QMessageBox.warning(self, "Error", "Las matrices deben tener dimensiones idénticas.")
                        return
                res = MatrizModel.sumar(matrices) if operacion == "+" else MatrizModel.restar(matrices)

            elif operacion == "*":
                for i in range(len(matrices) - 1):
                    if len(matrices[i][0]) != len(matrices[i+1]):
                        QMessageBox.warning(self, "Error", "Dimensiones incompatibles para multiplicar.")
                        return
                res = MatrizModel.multiplicar(matrices)

            self.mostrar_resultado(res)
            self.txt_bitacora.setText(f"Operación {operacion} realizada con éxito.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error inesperado: {e}")

    def ejecutar_gauss(self):
        try:
            matriz_A_raw = self.leer_matriz(self.tablas[0])
            num_cols_A = len(matriz_A_raw[0])

            if len(self.tablas) == 1 or num_cols_A > len(matriz_A_raw):
                if num_cols_A < 2:
                    QMessageBox.warning(self, "Error", "La tabla debe tener al menos 2 columnas para incluir los coeficientes y el término independiente.")
                    return
                A = [fila[:-1] for fila in matriz_A_raw]
                B = [[fila[-1]] for fila in matriz_A_raw]

            else:
                A = matriz_A_raw
                B = self.leer_matriz(self.tablas[1])

                if len(A) != len(B):
                    QMessageBox.warning(self, "Error", "La Matriz A y el Vector B deben tener el mismo número de filas.")
                    return

            pasos, clasificacion, solucion, verificacion = MatrizModel.gauss_resolver_completo(A, B)

            self.mostrar_resultado(solucion)

            reporte = (
                f"======================================\n"
                f"   CLASIFICACIÓN: {clasificacion}\n"
                f"======================================\n\n"
                f"{pasos}\n"
                f"{verificacion}"
            )
            self.txt_bitacora.setText(reporte)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al procesar Gauss: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = CalculadoraMatrices()
    ventana.show()
    sys.exit(app.exec())