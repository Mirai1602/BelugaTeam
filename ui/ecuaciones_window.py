from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem, QTextEdit, QMessageBox, QGroupBox
)

from core.operaciones import MatrizModel


class EcuacionesWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWindowTitle("BelugaTeam - Ecuaciones Matriciales")
        self.resize(1100, 750)
        self.setup_ui()
        self.generar_tablas()

    def setup_ui(self):
        principal = QVBoxLayout(self)
        principal.addWidget(QLabel("<h2>Ecuaciones matriciales: AX = B</h2>"))
        controles = QHBoxLayout()
        controles.addWidget(QLabel("Ecuaciones:"))
        self.spin_filas = QSpinBox(); self.spin_filas.setRange(1, 15); self.spin_filas.setValue(2)
        controles.addWidget(self.spin_filas)
        controles.addWidget(QLabel("Variables:"))
        self.spin_columnas = QSpinBox(); self.spin_columnas.setRange(1, 15); self.spin_columnas.setValue(2)
        controles.addWidget(self.spin_columnas)
        btn_generar = QPushButton("Generar tablas"); btn_generar.clicked.connect(self.generar_tablas); controles.addWidget(btn_generar)
        btn_limpiar = QPushButton("Limpiar"); btn_limpiar.clicked.connect(self.limpiar); controles.addWidget(btn_limpiar)
        btn_volver = QPushButton("Volver"); btn_volver.clicked.connect(self.close); controles.addWidget(btn_volver)
        controles.addStretch(); principal.addLayout(controles)

        tablas = QHBoxLayout()
        self.tabla_a = QTableWidget(); self.tabla_b = QTableWidget()
        tablas.addWidget(self.crear_grupo("Matriz A (coeficientes)", self.tabla_a))
        tablas.addWidget(self.crear_grupo("Matriz B (independientes)", self.tabla_b))
        principal.addLayout(tablas)

        botones = QHBoxLayout()
        for texto, metodo in (("Resolver con Gauss", self.gauss), ("Resolver con Gauss-Jordan", self.gauss_jordan), ("Reducción de pivotes", self.pivotes)):
            boton = QPushButton(texto); boton.clicked.connect(metodo); botones.addWidget(boton)
        principal.addLayout(botones)
        principal.addWidget(QLabel("<b>Resultado:</b>"))
        self.lbl_resultado = QLabel("Sin resultados"); self.lbl_resultado.setWordWrap(True); principal.addWidget(self.lbl_resultado)
        principal.addWidget(QLabel("<b>Procedimiento:</b>"))
        self.bitacora = QTextEdit(); self.bitacora.setReadOnly(True); principal.addWidget(self.bitacora)

    def crear_grupo(self, titulo, tabla):
        grupo = QGroupBox(titulo); layout = QVBoxLayout(grupo); layout.addWidget(tabla); return grupo

    def generar_tablas(self):
        filas, columnas = self.spin_filas.value(), self.spin_columnas.value()
        self.tabla_a.setRowCount(filas); self.tabla_a.setColumnCount(columnas)
        self.tabla_b.setRowCount(filas); self.tabla_b.setColumnCount(1)
        for tabla in (self.tabla_a, self.tabla_b):
            for i in range(tabla.rowCount()):
                for j in range(tabla.columnCount()):
                    tabla.setItem(i, j, QTableWidgetItem("0"))
        self.lbl_resultado.setText("Sin resultados"); self.bitacora.clear()

    def limpiar(self):
        self.generar_tablas()

    def leer(self, tabla):
        matriz = []
        for i in range(tabla.rowCount()):
            fila = []
            for j in range(tabla.columnCount()):
                item = tabla.item(i, j); fila.append(float(item.text()) if item and item.text().strip() else 0.0)
            matriz.append(fila)
        return matriz

    def resolver(self, metodo, nombre):
        try:
            a, b = self.leer(self.tabla_a), self.leer(self.tabla_b)
            pasos, clasificacion, solucion, verificacion = metodo(a, b)
            if isinstance(solucion, str):
                resultado = solucion
            elif solucion and isinstance(solucion[0], list):
                resultado = "X = " + str([str(x[0]) for x in solucion])
            else:
                resultado = str(solucion)
            self.lbl_resultado.setText(f"{clasificacion}\n{resultado}")
            self.bitacora.setText(f"MÉTODO: {nombre}\n\n{pasos}\n{verificacion}")
        except Exception as error:
            QMessageBox.warning(self, "Error", str(error))

    def gauss(self): self.resolver(MatrizModel.gauss_resolver_completo, "GAUSS")
    def gauss_jordan(self): self.resolver(MatrizModel.metodo_gauss_jordan, "GAUSS-JORDAN")
    def pivotes(self): self.resolver(MatrizModel.reduccion_pivotes, "REDUCCIÓN DE PIVOTES")

    def closeEvent(self, event):
        if self.parent_window is not None:
            self.parent_window.show()
        event.accept()
