# ui/determinantes_window.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QSpinBox, QTableWidget, QTableWidgetItem, 
    QPushButton, QTextEdit, QComboBox, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt
from core.determinantes import CalculadoraDeterminantes


class DeterminantesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Determinante de una Matriz")
        self.resize(720, 620)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)

        # Panel de controles superiores (Dimensión y Método)
        controls_layout = QHBoxLayout()
        
        lbl_n = QLabel("Dimensión (N x N):")
        self.spin_n = QSpinBox()
        self.spin_n.setRange(2, 6)
        self.spin_n.setValue(3)
        self.spin_n.valueChanged.connect(self.crear_matriz)
        
        lbl_metodo = QLabel("Método de cálculo:")
        self.combo_metodo = QComboBox()
        self.combo_metodo.addItems(["Cofactores", "Eliminación Gaussiana"])

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
        self.btn_calcular = QPushButton("Calcular Determinante")
        self.btn_calcular.clicked.connect(self.calcular_determinante)
        main_layout.addWidget(self.btn_calcular)

        # Visor del Paso a Paso / Resultado
        self.txt_pasos = QTextEdit()
        self.txt_pasos.setReadOnly(True)
        self.txt_pasos.setPlaceholderText("Aquí se mostrará el procedimiento paso a paso...")
        main_layout.addWidget(self.txt_pasos)

        self.setLayout(main_layout)

        # Inicializar la matriz por primera vez
        self.crear_matriz()

    def crear_matriz(self):
        """Genera la cuadrícula N x N con formato centrado y tamaño adaptativo."""
        n = self.spin_n.value()
        self.tabla_matriz.setRowCount(n)
        self.tabla_matriz.setColumnCount(n)

        # Ajustar dimensiones de filas y columnas para mantener aspecto equilibrado
        header_h = self.tabla_matriz.horizontalHeader()
        header_v = self.tabla_matriz.verticalHeader()

        for i in range(n):
            header_h.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
            header_v.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        for i in range(n):
            for j in range(n):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_matriz.setItem(i, j, item)

    def obtener_matriz_datos(self):
        """Lee los datos ingresados en la tabla como matriz de listas nativa."""
        n = self.spin_n.value()
        matriz = []

        for i in range(n):
            fila = []
            for j in range(n):
                item = self.tabla_matriz.item(i, j)
                texto = item.text().strip() if item else ""
                if not texto:
                    val = 0.0
                else:
                    val = float(texto.replace(",", "."))
                fila.append(val)
            matriz.append(fila)

        return matriz

    def calcular_determinante(self):
        """Invoca la lógica de cálculo según el método seleccionado."""
        try:
            matriz = self.obtener_matriz_datos()
            metodo = self.combo_metodo.currentText()

            if metodo == "Cofactores":
                det, pasos = CalculadoraDeterminantes.determinante_cofactores(matriz)
            else:
                det, pasos = CalculadoraDeterminantes.determinante_gauss(matriz)

            self.txt_pasos.setText(pasos)

        except ValueError as ve:
            QMessageBox.warning(self, "Valor Inválido", f"Por favor verifica los números ingresados:\n{ve}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al calcular el determinante:\n{e}")