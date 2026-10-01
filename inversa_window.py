from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QMessageBox, QGroupBox, QScrollArea, QTextEdit
)
from qfluentwidgets import (
    TitleLabel, BodyLabel, StrongBodyLabel, PrimaryPushButton,
    PushButton, ComboBox, SpinBox
)

from core.inversa import MatrizInversa


class InversaWindow(QWidget):
    """Interfaz Fluent para el módulo independiente de matrices inversas."""

    def __init__(self, ventana_principal=None):
        super().__init__(ventana_principal)
        self.ventana_principal = ventana_principal
        self.setObjectName("inversaWindow")
        self.setWindowTitle("BelugaCalc - Matrices Inversas")
        self.resize(1100, 800)
        self.init_ui()
        self.generar_matriz()

    def init_ui(self):
        principal = QVBoxLayout(self)
        principal.setContentsMargins(28, 24, 28, 24)
        principal.setSpacing(14)

        principal.addWidget(TitleLabel("Matrices Inversas"))
        principal.addWidget(BodyLabel(
            "Valida la matriz, selecciona el método de operación y observa el procedimiento paso a paso."
        ))

        controles = QHBoxLayout()
        controles.addWidget(StrongBodyLabel("Filas:"))
        self.spin_filas = SpinBox()
        self.spin_filas.setRange(1, 20)
        self.spin_filas.setValue(3)
        controles.addWidget(self.spin_filas)

        controles.addWidget(StrongBodyLabel("Columnas:"))
        self.spin_columnas = SpinBox()
        self.spin_columnas.setRange(1, 20)
        self.spin_columnas.setValue(3)
        controles.addWidget(self.spin_columnas)

        controles.addWidget(StrongBodyLabel("Operación:"))
        self.combo_operacion = ComboBox()
        self.combo_operacion.addItems([
            "Matriz inversa",
            "Matriz inversa de una matriz inversa",
        ])
        self.combo_operacion.setMinimumWidth(260)
        controles.addWidget(self.combo_operacion)

        btn_generar = PrimaryPushButton("Generar matriz")
        btn_generar.clicked.connect(self.generar_matriz)
        controles.addWidget(btn_generar)

        btn_limpiar = PushButton("Limpiar")
        btn_limpiar.clicked.connect(self.limpiar)
        controles.addWidget(btn_limpiar)
        controles.addStretch()
        principal.addLayout(controles)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        contenedor = QWidget()
        layout_matriz = QVBoxLayout(contenedor)

        grupo = QGroupBox("Matriz A")
        grupo_layout = QVBoxLayout(grupo)
        self.tabla_matriz = QTableWidget()
        self.tabla_matriz.setAlternatingRowColors(True)
        grupo_layout.addWidget(self.tabla_matriz)
        layout_matriz.addWidget(grupo)
        layout_matriz.addStretch()
        self.scroll.setWidget(contenedor)
        principal.addWidget(self.scroll, 3)

        acciones = QHBoxLayout()
        btn_calcular = PrimaryPushButton("Calcular inversa")
        btn_calcular.clicked.connect(self.calcular)
        acciones.addWidget(btn_calcular)
        acciones.addStretch()
        principal.addLayout(acciones)

        principal.addWidget(StrongBodyLabel("Resultado:"))
        self.tabla_resultado = QTableWidget()
        self.tabla_resultado.setMaximumHeight(180)
        self.tabla_resultado.setAlternatingRowColors(True)
        principal.addWidget(self.tabla_resultado)

        principal.addWidget(StrongBodyLabel("Validaciones y procedimiento:"))
        self.txt_bitacora = QTextEdit()
        self.txt_bitacora.setReadOnly(True)
        principal.addWidget(self.txt_bitacora, 2)

    def generar_matriz(self):
        filas = self.spin_filas.value()
        columnas = self.spin_columnas.value()
        self.tabla_matriz.setRowCount(filas)
        self.tabla_matriz.setColumnCount(columnas)

        for i in range(filas):
            self.tabla_matriz.setVerticalHeaderItem(i, QTableWidgetItem(str(i + 1)))
            for j in range(columnas):
                self.tabla_matriz.setHorizontalHeaderItem(j, QTableWidgetItem(str(j + 1)))
                if self.tabla_matriz.item(i, j) is None:
                    self.tabla_matriz.setItem(i, j, QTableWidgetItem("0"))

        self.tabla_resultado.clear()
        self.tabla_resultado.setRowCount(0)
        self.tabla_resultado.setColumnCount(0)
        self.txt_bitacora.clear()

    def limpiar(self):
        for i in range(self.tabla_matriz.rowCount()):
            for j in range(self.tabla_matriz.columnCount()):
                self.tabla_matriz.setItem(i, j, QTableWidgetItem("0"))
        self.tabla_resultado.clear()
        self.tabla_resultado.setRowCount(0)
        self.tabla_resultado.setColumnCount(0)
        self.txt_bitacora.clear()

    def leer_matriz(self):
        matriz = []
        for i in range(self.tabla_matriz.rowCount()):
            fila = []
            for j in range(self.tabla_matriz.columnCount()):
                item = self.tabla_matriz.item(i, j)
                texto = item.text().strip() if item else "0"
                if texto == "":
                    texto = "0"
                try:
                    fila.append(MatrizInversa.a_fraction(texto))
                except (ValueError, ZeroDivisionError):
                    raise ValueError(f"El valor de la posición ({i + 1}, {j + 1}) no es válido: {texto}")
            matriz.append(fila)
        return matriz

    def mostrar_resultado(self, matriz):
        filas = len(matriz)
        columnas = len(matriz[0]) if matriz else 0
        self.tabla_resultado.setRowCount(filas)
        self.tabla_resultado.setColumnCount(columnas)

        for i in range(filas):
            for j in range(columnas):
                item = QTableWidgetItem(MatrizInversa.formato_valor(matriz[i][j]))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_resultado.setItem(i, j, item)

    def calcular(self):
        try:
            matriz = self.leer_matriz()
            operacion = self.combo_operacion.currentText()
            respuesta = MatrizInversa.inversa(matriz, operacion)

            self.mostrar_resultado(respuesta["resultado"])
            reporte = (
                "========================================\n"
                "      MÓDULO DE MATRICES INVERSAS\n"
                "========================================\n\n"
                f"OPERACIÓN: {operacion}\n"
                f"MÉTODO: {respuesta['metodo']}\n\n"
                "VALIDACIONES:\n"
                f"{respuesta['validaciones']}\n\n"
                "PROCEDIMIENTO:\n"
                f"{respuesta['pasos']}"
            )
            self.txt_bitacora.setPlainText(reporte)
        except Exception as e:
            self.tabla_resultado.clear()
            self.tabla_resultado.setRowCount(0)
            self.tabla_resultado.setColumnCount(0)
            self.txt_bitacora.setPlainText(f"VALIDACIÓN / ERROR:\n{e}")
            QMessageBox.warning(self, "Matriz inversa", str(e))
