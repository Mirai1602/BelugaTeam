# ui/determinantes_window.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QSpinBox, QTableWidget, QTableWidgetItem, 
    QPushButton, QTextEdit, QComboBox, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt
from core.determinantes import CalculadoraDeterminantes


class DeterminantesWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Determinante y Regla de Cramer")
        self.resize(780, 640)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)

        # Panel de controles superiores
        controls_layout = QHBoxLayout()
        
        lbl_n = QLabel("Dimensión (N x N):")
        self.spin_n = QSpinBox()
        self.spin_n.setRange(2, 6)
        self.spin_n.setValue(3)
        self.spin_n.valueChanged.connect(self.crear_matriz)
        
        lbl_metodo = QLabel("Método de cálculo:")
        self.combo_metodo = QComboBox()
        self.combo_metodo.addItems(["Cofactores", "Eliminación Gaussiana", "Sarrus", "Regla de Cramer"])
        self.combo_metodo.currentTextChanged.connect(self.actualizar_interfaz_metodo)

        controls_layout.addWidget(lbl_n)
        controls_layout.addWidget(self.spin_n)
        controls_layout.addSpacing(20)
        controls_layout.addWidget(lbl_metodo)
        controls_layout.addWidget(self.combo_metodo)
        controls_layout.addStretch()

        main_layout.addLayout(controls_layout)

        # Tabla / Matriz
        self.tabla_matriz = QTableWidget()
        main_layout.addWidget(self.tabla_matriz)

        # Botón de Acción
        self.btn_calcular = QPushButton("Calcular / Resolver")
        self.btn_calcular.clicked.connect(self.calcular_resultado)
        main_layout.addWidget(self.btn_calcular)

        # Visor del Paso a Paso / Resultado
        self.txt_pasos = QTextEdit()
        self.txt_pasos.setReadOnly(True)
        self.txt_pasos.setPlaceholderText("Aquí se mostrará el procedimiento paso a paso...")
        main_layout.addWidget(self.txt_pasos)

        self.setLayout(main_layout)
        self.crear_matriz()

    def actualizar_interfaz_metodo(self, metodo):
        """Ajusta el rango de dimensión y redibuja la matriz si se elige Cramer."""
        if metodo == "Sarrus":
            if self.spin_n.value() > 4:
                self.spin_n.setValue(4)
            self.spin_n.setRange(2, 4)
        else:
            self.spin_n.setRange(2, 6)

        self.crear_matriz()

    def crear_matriz(self):
        """Genera la cuadrícula N x N o N x (N+1) para Cramer."""
        n = self.spin_n.value()
        metodo = self.combo_metodo.currentText()
        cols = n + 1 if metodo == "Regla de Cramer" else n

        self.tabla_matriz.setRowCount(n)
        self.tabla_matriz.setColumnCount(cols)

        header_h = self.tabla_matriz.horizontalHeader()
        header_v = self.tabla_matriz.verticalHeader()

        # Encabezados de columnas
        headers = [f"x{j+1}" for j in range(n)]
        if metodo == "Regla de Cramer":
            headers.append("T. Indep (b)")

        self.tabla_matriz.setHorizontalHeaderLabels(headers)

        for j in range(cols):
            header_h.setSectionResizeMode(j, QHeaderView.ResizeMode.Stretch)
        for i in range(n):
            header_v.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        for i in range(n):
            for j in range(cols):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_matriz.setItem(i, j, item)

    def obtener_matriz_datos(self):
        """Lee los datos ingresados separando A y b si es Cramer."""
        n = self.spin_n.value()
        metodo = self.combo_metodo.currentText()
        matriz_A = []
        vector_b = []

        for i in range(n):
            fila = []
            for j in range(n):
                item = self.tabla_matriz.item(i, j)
                texto = item.text().strip() if item else ""
                val = float(texto.replace(",", ".")) if texto else 0.0
                fila.append(val)
            matriz_A.append(fila)

            if metodo == "Regla de Cramer":
                item_b = self.tabla_matriz.item(i, n)
                texto_b = item_b.text().strip() if item_b else ""
                val_b = float(texto_b.replace(",", ".")) if texto_b else 0.0
                vector_b.append(val_b)

        return matriz_A, vector_b

    def calcular_resultado(self):
        """Invoca el cálculo correspondiente del core."""
        try:
            matriz_A, vector_b = self.obtener_matriz_datos()
            metodo = self.combo_metodo.currentText()

            if metodo == "Cofactores":
                _, pasos = CalculadoraDeterminantes.determinante_cofactores(matriz_A)
            elif metodo == "Sarrus":
                _, pasos = CalculadoraDeterminantes.determinante_sarrus(matriz_A)
            elif metodo == "Regla de Cramer":
                _, pasos = CalculadoraDeterminantes.regla_cramer(matriz_A, vector_b)
            else:
                _, pasos = CalculadoraDeterminantes.determinante_gauss(matriz_A)

            self.txt_pasos.setText(pasos)

        except ValueError as ve:
            QMessageBox.warning(self, "Aviso de Validación", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error en el cálculo:\n{e}")