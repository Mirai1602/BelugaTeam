from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
    QGroupBox, QTextEdit
)

from core.operaciones import MatrizModel
from ui.conversiones_window import ConversionesWindow


class CalculadoraMatricesAvanzada(QWidget):
    def __init__(self, ventana_principal=None):
        super().__init__()

        self.ventana_principal = ventana_principal

        self.setWindowTitle("BelugaCalc - Avanzada")
        self.resize(1100, 800)

        self.tablas = []
        self.init_ui()

    def init_ui(self):
        layout_principal = QVBoxLayout()

        layout_principal.addWidget(
            QLabel("<h2>Calculadora Avanzada</h2>")
        )

        controles = QHBoxLayout()

        controles.addWidget(QLabel("Ecuaciones (filas):"))

        self.spin_filas = QSpinBox()
        self.spin_filas.setRange(1, 10)
        self.spin_filas.setValue(3)
        controles.addWidget(self.spin_filas)

        controles.addWidget(QLabel("Variables (columnas):"))

        self.spin_columnas = QSpinBox()
        self.spin_columnas.setRange(1, 10)
        self.spin_columnas.setValue(3)
        controles.addWidget(self.spin_columnas)

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

        tablas_layout.addWidget(
            self.crear_grupo_tabla(
                "Matriz A (Coeficientes)",
                self.tabla_A
            )
        )

        tablas_layout.addWidget(
            self.crear_grupo_tabla(
                "Matriz B (Independientes)",
                self.tabla_B
            )
        )

        layout_principal.addLayout(tablas_layout)

        operaciones_layout = QHBoxLayout()

        btn_gauss = QPushButton("Resolver Gauss")
        btn_gauss.clicked.connect(self.ejecutar_gauss)
        operaciones_layout.addWidget(btn_gauss)

        btn_gauss_jordan = QPushButton("Resolver Gauss-Jordan")
        btn_gauss_jordan.clicked.connect(self.ejecutar_gauss_jordan)
        operaciones_layout.addWidget(btn_gauss_jordan)

        btn_pivotes = QPushButton("Reducción de Pivotes")
        btn_pivotes.clicked.connect(self.ejecutar_reduccion_pivotes)
        operaciones_layout.addWidget(btn_pivotes)

        layout_principal.addLayout(operaciones_layout)

        layout_principal.addWidget(
            QLabel("<b>Vector Solución (x) / Resultado:</b>")
        )

        self.tabla_res = QTableWidget()
        self.tabla_res.setMaximumHeight(130)
        layout_principal.addWidget(self.tabla_res)

        layout_principal.addWidget(
            QLabel("<b>Procedimiento Paso a Paso y Clasificación:</b>")
        )

        self.txt_bitacora = QTextEdit()
        self.txt_bitacora.setReadOnly(True)
        layout_principal.addWidget(self.txt_bitacora)

        btn_conversiones = QPushButton("Conversiones")
        btn_conversiones.clicked.connect(self.abrir_conversiones)
        layout_principal.addWidget(btn_conversiones)

        self.setLayout(layout_principal)

        self.generar_tablas()

    def crear_grupo_tabla(self, titulo, tabla):
        grupo = QGroupBox(titulo)
        layout = QVBoxLayout()
        layout.addWidget(tabla)
        grupo.setLayout(layout)
        return grupo

    def generar_tablas(self):
        filas = self.spin_filas.value()
        columnas = self.spin_columnas.value()

        self.tabla_A.setRowCount(filas)
        self.tabla_A.setColumnCount(columnas)

        self.tabla_B.setRowCount(filas)
        self.tabla_B.setColumnCount(1)

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
                valor = matriz_res[i][j]

                if hasattr(valor, "numerator"):
                    if valor.denominator == 1:
                        texto = str(valor.numerator)
                    else:
                        texto = f"{valor.numerator}/{valor.denominator}"
                else:
                    texto = str(round(float(valor), 4))

                self.tabla_res.setItem(
                    i, j, QTableWidgetItem(texto)
                )

    def obtener_A_y_B(self):
        A = self.leer_matriz(self.tabla_A)
        B = self.leer_matriz(self.tabla_B)

        if len(A) != len(B):
            QMessageBox.warning(
                self,
                "Error",
                "La Matriz A y el Vector B deben tener el mismo número de filas."
            )
            return None, None

        return A, B

    def ejecutar_gauss(self):
        try:
            A, B = self.obtener_A_y_B()

            if A is None:
                return

            pasos, clasificacion, solucion, verificacion = (
                MatrizModel.gauss_resolver_completo(A, B)
            )

            self.mostrar_resultado(solucion)

            reporte = (
                "======================================\n"
                "   MÉTODO: GAUSS\n"
                f"   CLASIFICACIÓN: {clasificacion}\n"
                "======================================\n\n"
                f"{pasos}\n"
                f"{verificacion}"
            )

            self.txt_bitacora.setText(reporte)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Ocurrió un error al procesar Gauss: {e}"
            )

    def ejecutar_gauss_jordan(self):
        try:
            A, B = self.obtener_A_y_B()

            if A is None:
                return

            pasos, clasificacion, solucion, verificacion = (
                MatrizModel.metodo_gauss_jordan(A, B)
            )

            self.mostrar_resultado(solucion)

            reporte = (
                "======================================\n"
                "   MÉTODO: GAUSS-JORDAN\n"
                f"   CLASIFICACIÓN: {clasificacion}\n"
                "======================================\n\n"
                f"{pasos}\n"
                f"{verificacion}"
            )

            self.txt_bitacora.setText(reporte)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Ocurrió un error al procesar Gauss-Jordan: {e}"
            )

    def ejecutar_reduccion_pivotes(self):
        try:
            A, B = self.obtener_A_y_B()

            if A is None:
                return

            pasos, clasificacion, matriz, verificacion = (
                MatrizModel.reduccion_pivotes(A, B)
            )

            self.mostrar_resultado(matriz)

            reporte = (
                "======================================\n"
                "   MÉTODO: REDUCCIÓN DE PIVOTES\n"
                f"   CLASIFICACIÓN: {clasificacion}\n"
                "======================================\n\n"
                f"{pasos}\n"
                f"{verificacion}"
            )

            self.txt_bitacora.setText(reporte)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Ocurrió un error al realizar la reducción de pivotes: {e}"
            )

    def abrir_conversiones(self):
        self.ventana_conversiones = ConversionesWindow(self)
        self.ventana_conversiones.show()
        self.ventana_conversiones.raise_()
        self.ventana_conversiones.activateWindow()

    def volver(self):
        self.close()

    def closeEvent(self, event):
        if self.ventana_principal is not None:
            self.ventana_principal.show()

        event.accept()
