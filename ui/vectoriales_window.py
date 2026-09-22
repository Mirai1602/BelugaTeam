from fractions import Fraction

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem, QComboBox, QTextEdit, QMessageBox,
    QGroupBox, QLineEdit, QScrollArea, QWidget
)

from core.vectoriales import VectorModel


class VectorialesWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.tablas_vectores = []
        self.setWindowTitle("BelugaTeam - Vectores")
        self.resize(1100, 750)
        self.setup_ui()
        self.generar_vectores()

    def setup_ui(self):
        principal = QVBoxLayout(self)
        principal.addWidget(QLabel("<h2>Módulo de Vectores</h2>"))

        controles = QHBoxLayout()
        controles.addWidget(QLabel("Dimensión:"))
        self.spin_dimension = QSpinBox()
        self.spin_dimension.setRange(1, 20)
        self.spin_dimension.setValue(3)
        controles.addWidget(self.spin_dimension)

        controles.addWidget(QLabel("Cantidad de vectores generadores:"))
        self.spin_generadores = QSpinBox()
        self.spin_generadores.setRange(1, 10)
        self.spin_generadores.setValue(2)
        controles.addWidget(self.spin_generadores)

        btn_generar = QPushButton("Generar")
        btn_generar.clicked.connect(self.generar_vectores)
        controles.addWidget(btn_generar)

        btn_limpiar = QPushButton("Limpiar")
        btn_limpiar.clicked.connect(self.limpiar)
        controles.addWidget(btn_limpiar)

        btn_volver = QPushButton("Volver")
        btn_volver.clicked.connect(self.close)
        controles.addWidget(btn_volver)
        controles.addStretch()
        principal.addLayout(controles)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.contenedor = QWidget()
        self.vectores_layout = QVBoxLayout(self.contenedor)
        self.scroll.setWidget(self.contenedor)
        principal.addWidget(self.scroll, 3)

        fila_operacion = QHBoxLayout()
        fila_operacion.addWidget(QLabel("Operación:"))
        self.combo_operacion = QComboBox()
        self.combo_operacion.addItems([
            "Suma", "Resta", "Multiplicación por escalar", "Combinación lineal"
        ])
        fila_operacion.addWidget(self.combo_operacion)
        fila_operacion.addWidget(QLabel("Escalar:"))
        self.txt_escalar = QLineEdit("2")
        self.txt_escalar.setMaximumWidth(120)
        fila_operacion.addWidget(self.txt_escalar)
        btn_ejecutar = QPushButton("Ejecutar")
        btn_ejecutar.clicked.connect(self.ejecutar)
        fila_operacion.addWidget(btn_ejecutar)
        fila_operacion.addStretch()
        principal.addLayout(fila_operacion)

        principal.addWidget(QLabel("<b>Resultado:</b>"))
        self.lbl_resultado = QLabel("Sin resultados")
        self.lbl_resultado.setWordWrap(True)
        principal.addWidget(self.lbl_resultado)

        principal.addWidget(QLabel("<b>Bitácora:</b>"))
        self.txt_bitacora = QTextEdit()
        self.txt_bitacora.setReadOnly(True)
        principal.addWidget(self.txt_bitacora, 2)

    def generar_vectores(self):
        while self.vectores_layout.count():
            item = self.vectores_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.tablas_vectores.clear()
        dimension = self.spin_dimension.value()
        cantidad = self.spin_generadores.value()

        for indice in range(cantidad):
            grupo = QGroupBox(f"Vector generador v{indice + 1}")
            layout = QVBoxLayout(grupo)
            tabla = QTableWidget(1, dimension)
            tabla.setMinimumHeight(85)
            for columna in range(dimension):
                tabla.setHorizontalHeaderItem(columna, QTableWidgetItem(str(columna + 1)))
                tabla.setItem(0, columna, QTableWidgetItem("0"))
            layout.addWidget(tabla)
            self.vectores_layout.addWidget(grupo)
            self.tablas_vectores.append(tabla)

        grupo_objetivo = QGroupBox("Vector objetivo b (para combinación lineal)")
        layout_objetivo = QVBoxLayout(grupo_objetivo)
        self.tabla_objetivo = QTableWidget(1, dimension)
        self.tabla_objetivo.setMinimumHeight(85)
        for columna in range(dimension):
            self.tabla_objetivo.setHorizontalHeaderItem(columna, QTableWidgetItem(str(columna + 1)))
            self.tabla_objetivo.setItem(0, columna, QTableWidgetItem("0"))
        layout_objetivo.addWidget(self.tabla_objetivo)
        self.vectores_layout.addWidget(grupo_objetivo)
        self.vectores_layout.addStretch()
        self.lbl_resultado.setText("Sin resultados")
        self.txt_bitacora.clear()

    def leer_vector(self, tabla):
        vector = []
        for columna in range(tabla.columnCount()):
            item = tabla.item(0, columna)
            texto = item.text().strip() if item else "0"
            vector.append(VectorModel.a_fraction(texto))
        return vector

    def ejecutar(self):
        try:
            vectores = [self.leer_vector(tabla) for tabla in self.tablas_vectores]
            operacion = self.combo_operacion.currentText()

            if operacion in ("Suma", "Resta"):
                if len(vectores) < 2:
                    raise ValueError("Se necesitan al menos dos vectores.")
                resultado = vectores[0]
                pasos = []
                for vector in vectores[1:]:
                    resultado = VectorModel.suma(resultado, vector) if operacion == "Suma" else VectorModel.resta(resultado, vector)
                simbolo = "+" if operacion == "Suma" else "-"
                texto = VectorModel.formato_vector(resultado)
                pasos.append(f"Se realizó la operación componente por componente usando el símbolo {simbolo}.")

            elif operacion == "Multiplicación por escalar":
                escalar = VectorModel.a_fraction(self.txt_escalar.text())
                resultado = VectorModel.escalar(vectores[0], escalar)
                texto = VectorModel.formato_vector(resultado)
                pasos = [f"Cada componente del primer vector se multiplicó por {VectorModel.valor(escalar)}."]

            else:
                objetivo = self.leer_vector(self.tabla_objetivo)
                respuesta = VectorModel.combinacion_lineal(vectores, objetivo)
                texto = respuesta["clasificacion"]
                if isinstance(respuesta["coeficientes"], list):
                    texto += "\nCoeficientes: " + VectorModel.formato_vector(respuesta["coeficientes"])
                pasos = [respuesta["pasos"]]

            self.lbl_resultado.setText(texto)
            self.txt_bitacora.setText("\n".join(pasos))
        except Exception as error:
            QMessageBox.warning(self, "Error", str(error))

    def limpiar(self):
        for tabla in self.tablas_vectores + [getattr(self, "tabla_objetivo", None)]:
            if tabla:
                for fila in range(tabla.rowCount()):
                    for columna in range(tabla.columnCount()):
                        tabla.setItem(fila, columna, QTableWidgetItem("0"))
        self.txt_escalar.setText("2")
        self.lbl_resultado.setText("Sin resultados")
        self.txt_bitacora.clear()

    def closeEvent(self, event):
        if self.parent_window is not None:
            self.parent_window.show()
        event.accept()
