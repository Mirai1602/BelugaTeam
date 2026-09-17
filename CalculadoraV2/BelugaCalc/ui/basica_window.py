from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
    QGroupBox, QTextEdit
)

from core.operaciones import MatrizModel


class CalculadoraMatrices(QWidget):
    def __init__(self, ventana_principal=None):
        super().__init__()

        self.ventana_principal = ventana_principal

        self.setWindowTitle("BelugaCalc - Básica")
        self.resize(1000, 750)

        self.tablas = []
        self.init_ui()

    def init_ui(self):
        layout_principal = QVBoxLayout()

        titulo = QLabel("<h2>Calculadora Básica</h2>")
        layout_principal.addWidget(titulo)

        controles = QHBoxLayout()

        grupo_A = QGroupBox("Matriz A")
        layout_A = QHBoxLayout()

        layout_A.addWidget(QLabel("Filas:"))
        self.spin_filas_A = QSpinBox()
        self.spin_filas_A.setRange(1, 10)
        self.spin_filas_A.setValue(3)
        layout_A.addWidget(self.spin_filas_A)

        layout_A.addWidget(QLabel("Columnas:"))
        self.spin_columnas_A = QSpinBox()
        self.spin_columnas_A.setRange(1, 10)
        self.spin_columnas_A.setValue(3)
        layout_A.addWidget(self.spin_columnas_A)

        grupo_A.setLayout(layout_A)
        controles.addWidget(grupo_A)

        grupo_B = QGroupBox("Matriz B")
        layout_B = QHBoxLayout()

        layout_B.addWidget(QLabel("Filas:"))
        self.spin_filas_B = QSpinBox()
        self.spin_filas_B.setRange(1, 10)
        self.spin_filas_B.setValue(3)
        layout_B.addWidget(self.spin_filas_B)

        layout_B.addWidget(QLabel("Columnas:"))
        self.spin_columnas_B = QSpinBox()
        self.spin_columnas_B.setRange(1, 10)
        self.spin_columnas_B.setValue(3)
        layout_B.addWidget(self.spin_columnas_B)

        grupo_B.setLayout(layout_B)
        controles.addWidget(grupo_B)

        btn_generar = QPushButton("Generar Tablas")
        btn_generar.clicked.connect(self.generar_tablas)
        controles.addWidget(btn_generar)

        btn_limpiar = QPushButton("Limpiar")
        btn_limpiar.clicked.connect(self.limpiar_tablas)
        controles.addWidget(btn_limpiar)

        btn_volver = QPushButton("Volver")
        btn_volver.clicked.connect(self.volver)
        controles.addWidget(btn_volver)

        layout_principal.addLayout(controles)

        tablas_layout = QHBoxLayout()

        self.tabla_A = QTableWidget()
        self.tabla_B = QTableWidget()

        tablas_layout.addWidget(self.crear_grupo_tabla("Matriz A", self.tabla_A))
        tablas_layout.addWidget(self.crear_grupo_tabla("Matriz B", self.tabla_B))

        layout_principal.addLayout(tablas_layout)

        operaciones_layout = QHBoxLayout()

        btn_suma = QPushButton("Suma (+)")
        btn_suma.clicked.connect(lambda: self.ejecutar_operacion("+"))
        operaciones_layout.addWidget(btn_suma)

        btn_resta = QPushButton("Resta (-)")
        btn_resta.clicked.connect(lambda: self.ejecutar_operacion("-"))
        operaciones_layout.addWidget(btn_resta)

        btn_mult = QPushButton("Multiplicación (*)")
        btn_mult.clicked.connect(lambda: self.ejecutar_operacion("*"))
        operaciones_layout.addWidget(btn_mult)

        layout_principal.addLayout(operaciones_layout)

        layout_principal.addWidget(QLabel("<b>Resultado:</b>"))

        self.tabla_res = QTableWidget()
        layout_principal.addWidget(self.tabla_res)

        layout_principal.addWidget(
            QLabel("<b>Procedimiento Paso a Paso:</b>")
        )

        self.txt_bitacora = QTextEdit()
        self.txt_bitacora.setReadOnly(True)
        layout_principal.addWidget(self.txt_bitacora)

        self.setLayout(layout_principal)

        self.generar_tablas()

    def crear_grupo_tabla(self, titulo, tabla):
        grupo = QGroupBox(titulo)
        layout = QVBoxLayout()
        layout.addWidget(tabla)
        grupo.setLayout(layout)
        return grupo

    def generar_tablas(self):
        self.tabla_A.setRowCount(self.spin_filas_A.value())
        self.tabla_A.setColumnCount(self.spin_columnas_A.value())

        self.tabla_B.setRowCount(self.spin_filas_B.value())
        self.tabla_B.setColumnCount(self.spin_columnas_B.value())

        self.tabla_res.clearContents()
        self.tabla_res.setRowCount(0)
        self.tabla_res.setColumnCount(0)

        self.txt_bitacora.clear()

        self.tablas = [self.tabla_A, self.tabla_B]

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

                if item and item.text().strip() != "":
                    fila.append(float(item.text()))
                else:
                    fila.append(0.0)

            matriz.append(fila)

        return matriz

    def mostrar_resultado(self, matriz_res):
        self.tabla_res.clear()

        if isinstance(matriz_res, str):
            self.tabla_res.setRowCount(1)
            self.tabla_res.setColumnCount(1)

            item = QTableWidgetItem(matriz_res)
            self.tabla_res.setItem(0, 0, item)

            return

        if not matriz_res:
            self.tabla_res.setRowCount(0)
            self.tabla_res.setColumnCount(0)
            return

        filas = len(matriz_res)
        columnas = len(matriz_res[0])

        self.tabla_res.setRowCount(filas)
        self.tabla_res.setColumnCount(columnas)

        for i in range(filas):
            for j in range(columnas):
                val = str(round(float(matriz_res[i][j]), 4))
                self.tabla_res.setItem(
                    i, j, QTableWidgetItem(val)
                )

    def ejecutar_operacion(self, operacion):
        try:
            m1 = self.leer_matriz(self.tabla_A)
            m2 = self.leer_matriz(self.tabla_B)

            if operacion == "+":
                if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
                    QMessageBox.warning(
                        self,
                        "Error",
                        "Las matrices deben tener dimensiones idénticas."
                    )
                    return

                res = MatrizModel.sumar([m1, m2])

                pasos = (
                    "=== SUMA DE MATRICES ===\n\n"
                    "Se suman las entradas que ocupan la misma posición.\n\n"
                    f"{MatrizModel.formato_matriz_str(m1, 'Matriz A')}"
                    f"{MatrizModel.formato_matriz_str(m2, 'Matriz B')}"
                    "Resultado:\n"
                    f"{MatrizModel.formato_matriz_str(res)}"
                )

            elif operacion == "-":
                if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
                    QMessageBox.warning(
                        self,
                        "Error",
                        "Las matrices deben tener dimensiones idénticas."
                    )
                    return

                res = MatrizModel.restar([m1, m2])

                pasos = (
                    "=== RESTA DE MATRICES ===\n\n"
                    "Se restan las entradas que ocupan la misma posición.\n\n"
                    f"{MatrizModel.formato_matriz_str(m1, 'Matriz A')}"
                    f"{MatrizModel.formato_matriz_str(m2, 'Matriz B')}"
                    "Resultado:\n"
                    f"{MatrizModel.formato_matriz_str(res)}"
                )

            elif operacion == "*":
                if len(m1[0]) != len(m2):
                    QMessageBox.warning(
                        self,
                        "Error",
                        "Dimensiones incompatibles para multiplicar."
                    )
                    return

                res = MatrizModel.multiplicar([m1, m2])

                pasos = "=== MULTIPLICACIÓN DE MATRICES ===\n\n"

                for i in range(len(m1)):
                    for j in range(len(m2[0])):
                        terminos = []

                        for k in range(len(m1[0])):
                            terminos.append(
                                f"({m1[i][k]})({m2[k][j]})"
                            )

                        pasos += (
                            f"Resultado[{i + 1},{j + 1}] = "
                            + " + ".join(terminos)
                            + f" = {res[i][j]}\n"
                        )

                pasos += "\n"
                pasos += MatrizModel.formato_matriz_str(
                    res, "Matriz Resultado"
                )

            else:
                return

            self.mostrar_resultado(res)
            self.txt_bitacora.setText(pasos)

        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Ocurrió un error inesperado: {e}"
            )

    def volver(self):
        self.close()

    def closeEvent(self, event):
        if self.ventana_principal is not None:
            self.ventana_principal.show()

        event.accept()
