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
        # Qallariy (Inicio)
        self.addSubInterface(
            self.home_window,
            icon=FIF.HOME,
            text="Inicio"
        )

        # Módulos (Iconokuna allinchasqa)
        self.addSubInterface(
            self.ventana_basica,
            icon=FIF.APPLICATION,
            text="Básica"
        )
        self.addSubInterface(
            self.ventana_avanzada,
            icon=FIF.EDIT,
            text="Avanzada"
        )
        self.addSubInterface(
            self.ventana_vectoriales,
            icon=FIF.CODE,
            text="Vectores"
        )
        self.addSubInterface(
            self.ventana_ecuaciones,
            icon=FIF.DOCUMENT,
            text="Ecuaciones Matriciales"
        )

    def navegar_a(self, clave):
        mapa_modulos = {
            "home": self.home_window,
            "basica": self.ventana_basica,
            "avanzada": self.ventana_avanzada,
            "vectores": self.ventana_vectoriales,
            "ecuaciones": self.ventana_ecuaciones
        }
        
        target = mapa_modulos.get(clave)
        if target:
            self.switchTo(target)