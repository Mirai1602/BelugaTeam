from qfluentwidgets import FluentWindow, FluentIcon as FIF

from ui.home_window import HomeWindow
from ui.basica_window import CalculadoraMatrices
from ui.avanzada_window import CalculadoraMatricesAvanzada
from ui.vectoriales_window import VectorialesWindow
from ui.ecuaciones_window import EcuacionesWindow


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BelugaCalc")
        self.resize(1100, 750)

        # Pantallakuna
        self.home_window = HomeWindow(self)
        self.ventana_basica = CalculadoraMatrices(self)
        self.ventana_avanzada = CalculadoraMatricesAvanzada(self)
        self.ventana_vectoriales = VectorialesWindow(self)
        self.ventana_ecuaciones = EcuacionesWindow(self)

        # Sutinkuna navegacionpaq
        self.home_window.setObjectName("homeWindow")
        self.ventana_basica.setObjectName("basicaWindow")
        self.ventana_avanzada.setObjectName("avanzadaWindow")
        self.ventana_vectoriales.setObjectName("vectorialesWindow")
        self.ventana_ecuaciones.setObjectName("ecuacionesWindow")

        self.init_navigation()

    def init_navigation(self):
        # Pantalla de Inicio
        self.addSubInterface(
            self.home_window,
            icon=FIF.HOME,
            text="Inicio"
        )

        # Módulos de Cálculo con íconos estándar seguros
        self.addSubInterface(
            self.ventana_basica,
            icon=FIF.APPLICATION,   # Módulo básico / Aritmética
            text="Básica"
        )
        self.addSubInterface(
            self.ventana_avanzada,
            icon=FIF.EDIT,          # Módulo avanzado / Álgebra
            text="Avanzada"
        )
        self.addSubInterface(
            self.ventana_vectoriales,
            icon=FIF.CODE,          # Vectores y estructuras
            text="Vectores"
        )
        self.addSubInterface(
            self.ventana_ecuaciones,
            icon=FIF.DOCUMENT,      # Ecuaciones y matrices
            text="Ecuaciones Matriciales"
        )