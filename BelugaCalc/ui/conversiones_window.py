from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QLineEdit, QPushButton, QTextEdit, QScrollArea, QWidget,
    QMessageBox, QGroupBox
)

from core.conversiones import Conversiones


class ConversionesWindow(QDialog):
    """Ventana independiente para las conversiones de sistemas numéricos."""

    def __init__(self, ventana_padre=None):
        super().__init__(ventana_padre)
        self.setWindowTitle("BelugaCalc - Conversiones")
        self.resize(650, 600)
        self.setModal(False)
        self.init_ui()

    def init_ui(self):
        layout_principal = QVBoxLayout(self)

        titulo = QLabel("<h2>Conversiones de Sistemas Numéricos</h2>")
        layout_principal.addWidget(titulo)

        descripcion = QLabel(
            "Seleccione la conversión, introduzca el número y consulte "
            "el resultado junto con el procedimiento."
        )
        descripcion.setWordWrap(True)
        layout_principal.addWidget(descripcion)

        area_scroll = QScrollArea()
        area_scroll.setWidgetResizable(True)

        contenido = QWidget()
        contenido_layout = QVBoxLayout(contenido)

        grupo_entrada = QGroupBox("Datos de conversión")
        entrada_layout = QVBoxLayout(grupo_entrada)

        fila_tipo = QHBoxLayout()
        fila_tipo.addWidget(QLabel("Tipo de conversión:"))
        self.combo_conversion = QComboBox()
        self.combo_conversion.addItems([
            "Decimal → Binario",
            "Binario → Decimal",
            "Decimal → Octal",
            "Octal → Decimal",
            "Decimal → Hexadecimal",
            "Hexadecimal → Decimal"
        ])
        fila_tipo.addWidget(self.combo_conversion)
        entrada_layout.addLayout(fila_tipo)

        fila_numero = QHBoxLayout()
        fila_numero.addWidget(QLabel("Número:"))
        self.txt_conversion = QLineEdit()
        self.txt_conversion.setPlaceholderText("Ingrese el número aquí...")
        fila_numero.addWidget(self.txt_conversion)
        entrada_layout.addLayout(fila_numero)

        fila_botones = QHBoxLayout()
        btn_convertir = QPushButton("Convertir")
        btn_convertir.clicked.connect(self.ejecutar_conversion)
        fila_botones.addWidget(btn_convertir)

        btn_limpiar = QPushButton("Limpiar")
        btn_limpiar.clicked.connect(self.limpiar)
        fila_botones.addWidget(btn_limpiar)
        entrada_layout.addLayout(fila_botones)

        contenido_layout.addWidget(grupo_entrada)

        self.lbl_conversion_resultado = QLabel("Resultado: ")
        self.lbl_conversion_resultado.setWordWrap(True)
        contenido_layout.addWidget(self.lbl_conversion_resultado)

        contenido_layout.addWidget(QLabel("<b>Procedimiento:</b>"))
        self.txt_procedimiento = QTextEdit()
        self.txt_procedimiento.setReadOnly(True)
        self.txt_procedimiento.setMinimumHeight(250)
        contenido_layout.addWidget(self.txt_procedimiento)

        area_scroll.setWidget(contenido)
        layout_principal.addWidget(area_scroll)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.close)
        layout_principal.addWidget(btn_cerrar)

    def ejecutar_conversion(self):
        try:
            valor = self.txt_conversion.text().strip()
            opcion = self.combo_conversion.currentText()

            if not valor:
                raise ValueError("Ingrese un número para convertir.")

            if opcion == "Decimal → Binario":
                resultado, procedimiento = Conversiones.decimal_a_binario_con_procedimiento(valor)
            elif opcion == "Binario → Decimal":
                resultado, procedimiento = Conversiones.binario_a_decimal_con_procedimiento(valor)
            elif opcion == "Decimal → Octal":
                resultado, procedimiento = Conversiones.decimal_a_octal_con_procedimiento(valor)
            elif opcion == "Octal → Decimal":
                resultado, procedimiento = Conversiones.octal_a_decimal_con_procedimiento(valor)
            elif opcion == "Decimal → Hexadecimal":
                resultado, procedimiento = Conversiones.decimal_a_hexadecimal_con_procedimiento(valor)
            elif opcion == "Hexadecimal → Decimal":
                resultado, procedimiento = Conversiones.hexadecimal_a_decimal_con_procedimiento(valor)
            else:
                return

            self.lbl_conversion_resultado.setText(f"<b>Resultado:</b> {resultado}")
            self.txt_procedimiento.setPlainText(procedimiento)

        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error durante la conversión: {e}")

    def limpiar(self):
        self.txt_conversion.clear()
        self.lbl_conversion_resultado.setText("Resultado: ")
        self.txt_procedimiento.clear()
