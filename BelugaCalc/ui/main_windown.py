from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)

from BelugaTeam.BelugaCalc.ui.vectoriales_window import CalculadoraVectores, VectorialesWindow
from ui.basica_window import CalculadoraMatrices
from ui.avanzada_window import CalculadoraMatricesAvanzada


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BelugaCalc")
        self.resize(700, 450)

        layout_principal = QVBoxLayout()

        titulo = QLabel("<h1>BelugaCalc</h1>")
        subtitulo = QLabel(
            "Bienvenido/a a BelugaCalc, una calculadora virtual para matrices!"
        )

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(subtitulo)

        botones_layout = QHBoxLayout()

        btn_basica = QPushButton("Básica")
        btn_avanzada = QPushButton("Avanzada")

        btn_basica.clicked.connect(self.abrir_basica)
        btn_avanzada.clicked.connect(self.abrir_avanzada)

        botones_layout.addWidget(btn_basica)
        botones_layout.addWidget(btn_avanzada)
        btn_vectoriales = QPushButton("Vectoriales")
        btn_vectoriales.clicked.connect(self.abrir_vectoriales)
        botones_layout.addWidget(btn_vectoriales)

        layout_principal.addLayout(botones_layout)

        self.setLayout(layout_principal)

    def abrir_basica(self):
        self.ventana_basica = CalculadoraMatrices(self)
        self.hide()
        self.ventana_basica.show()

    def abrir_avanzada(self):
        self.ventana_avanzada = CalculadoraMatricesAvanzada(self)
        self.hide()
        self.ventana_avanzada.show()

    def abrir_vectoriales(self):
        self.ventana_vectoriales = CalculadoraVectores(self)
        self.hide()
        self.ventana_vectoriales.show()
