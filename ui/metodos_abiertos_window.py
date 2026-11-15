
"""Pantalla compartida de Newton-Raphson y Secante para BelugaCalc."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
)

from ui.newton_raphson_window import NewtonRaphsonWindow
from ui.secante_window import SecanteWindow


class MetodosAbiertosWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._crear_interfaz()
        self.seleccionar_metodo("newton")

    def _crear_interfaz(self):
        principal = QVBoxLayout(self)
        principal.setContentsMargins(14, 12, 14, 12)
        principal.setSpacing(8)

        titulo = QLabel("Newton-Raphson y Secante")
        titulo.setStyleSheet("""
            color: #031E36;
            font-size: 23px;
            font-weight: 800;
        """)
        principal.addWidget(titulo)

        subtitulo = QLabel(
            "Selecciona el método numérico que deseas utilizar."
        )
        subtitulo.setStyleSheet(
            "color: #64748B; font-size: 13px;"
        )
        principal.addWidget(subtitulo)

        botones = QHBoxLayout()
        botones.setSpacing(8)

        self.btn_newton = QPushButton("Newton-Raphson")
        self.btn_secante = QPushButton("Secante")

        estilo = """
            QPushButton {
                background: white;
                color: #04335A;
                border: 1px solid #C4D4E6;
                border-radius: 8px;
                font-weight: 700;
                padding: 9px;
            }
            QPushButton:hover {
                background: #EAF5FC;
            }
            QPushButton:checked {
                background: #04335A;
                color: white;
                border: 1px solid #04335A;
            }
        """

        for boton in (self.btn_newton, self.btn_secante):
            boton.setCheckable(True)
            boton.setMinimumHeight(40)
            boton.setCursor(Qt.CursorShape.PointingHandCursor)
            boton.setStyleSheet(estilo)
            botones.addWidget(boton)

        principal.addLayout(botones)

        # Las ventanas originales se conservan.
        self.paginas = QStackedWidget()

        self.ventana_newton = NewtonRaphsonWindow()
        self.ventana_secante = SecanteWindow()

        self.paginas.addWidget(self.ventana_newton)
        self.paginas.addWidget(self.ventana_secante)

        principal.addWidget(self.paginas, 1)

        self.btn_newton.clicked.connect(
            lambda: self.seleccionar_metodo("newton")
        )

        self.btn_secante.clicked.connect(
            lambda: self.seleccionar_metodo("secante")
        )

    def seleccionar_metodo(self, metodo):
        if metodo == "newton":
            self.paginas.setCurrentWidget(self.ventana_newton)
            self.btn_newton.setChecked(True)
            self.btn_secante.setChecked(False)

        elif metodo == "secante":
            self.paginas.setCurrentWidget(self.ventana_secante)
            self.btn_newton.setChecked(False)
            self.btn_secante.setChecked(True)

        else:
            raise ValueError("Método desconocido.")

    def mostrar_newton(self):
        self.seleccionar_metodo("newton")

    def mostrar_secante(self):
        self.seleccionar_metodo("secante")
