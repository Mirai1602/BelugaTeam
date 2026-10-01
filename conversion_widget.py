from PyQt6.QtWidgets import (
    QGroupBox, QHBoxLayout, QVBoxLayout, QLabel, QComboBox,
    QLineEdit, QPushButton, QTextEdit, QMessageBox
)

from core.conversiones import Conversiones


class ConversionWidget(QGroupBox):
    """Panel reutilizable para conversiones entre bases numéricas."""

    def __init__(self, parent=None):
        super().__init__("Conversiones de Sistemas Numéricos", parent)
        self.init_ui()

    def init_ui(self):
        layout_principal = QVBoxLayout()

        controles = QHBoxLayout()
        controles.addWidget(QLabel("Base de origen:"))
        self.combo_origen = QComboBox()
        self.combo_origen.addItems(["Decimal (10)", "Binario (2)", "Octal (8)", "Hexadecimal (16)"])
        controles.addWidget(self.combo_origen)

        controles.addWidget(QLabel("Base destino:"))
        self.combo_destino = QComboBox()
        self.combo_destino.addItems(["Binario (2)", "Octal (8)", "Decimal (10)", "Hexadecimal (16)"])
        controles.addWidget(self.combo_destino)
        layout_principal.addLayout(controles)

        entrada_layout = QHBoxLayout()
        entrada_layout.addWidget(QLabel("Número:"))
        self.txt_numero = QLineEdit()
        self.txt_numero.setPlaceholderText("Ejemplo: 101101, 73 o 2F")
        entrada_layout.addWidget(self.txt_numero)

        btn_convertir = QPushButton("Convertir")
        btn_convertir.clicked.connect(self.ejecutar_conversion)
        entrada_layout.addWidget(btn_convertir)
        layout_principal.addLayout(entrada_layout)

        self.lbl_resultado = QLabel("Resultado: ")
        layout_principal.addWidget(self.lbl_resultado)

        layout_principal.addWidget(QLabel("Procedimiento:") )
        self.txt_procedimiento = QTextEdit()
        self.txt_procedimiento.setReadOnly(True)
        self.txt_procedimiento.setMaximumHeight(130)
        layout_principal.addWidget(self.txt_procedimiento)

        self.setLayout(layout_principal)

    def obtener_base(self, texto):
        return int(texto.split("(")[1].split(")")[0])

    def ejecutar_conversion(self):
        try:
            numero = self.txt_numero.text().strip()
            origen = self.obtener_base(self.combo_origen.currentText())
            destino = self.obtener_base(self.combo_destino.currentText())

            resultado, procedimiento = Conversiones.convertir(numero, origen, destino)
            self.lbl_resultado.setText(f"Resultado: {resultado}")
            self.txt_procedimiento.setPlainText(procedimiento)
        except ValueError as error:
            QMessageBox.warning(self, "Error de conversión", str(error))
        except Exception as error:
            QMessageBox.critical(self, "Error", f"Ocurrió un error durante la conversión: {error}")
