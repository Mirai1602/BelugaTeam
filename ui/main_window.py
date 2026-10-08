from qfluentwidgets import FluentWindow, FluentIcon as FIF
from ui.home_window import HomeWindow
from ui.basica_window import CalculadoraMatrices
from ui.avanzada_window import CalculadoraMatricesAvanzada
from ui.vectoriales_window import VectorialesWindow
from ui.ecuaciones_window import EcuacionesWindow
from ui.inversa_window import InversaWindow
from ui.determinantes_window import DeterminantesWindow 


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BelugaCalc")
        self.resize(1100, 750)

        # 1. Instanciar Pantallas
        self.home_window = HomeWindow(self)
        self.ventana_basica = CalculadoraMatrices(self)
        self.ventana_determinantes = DeterminantesWindow()
        self.ventana_inversa = InversaWindow(self)
        self.ventana_avanzada = CalculadoraMatricesAvanzada(self)
        self.ventana_ecuaciones = EcuacionesWindow(self)
        self.ventana_vectoriales = VectorialesWindow(self)

        # 2. Conectar la señal de navegación de las tarjetas del Home
        self.home_window.modulo_seleccionado.connect(self.navegar_a)

        # 3. Asignar Nombres de Objeto
        self.home_window.setObjectName("homeWindow")
        self.ventana_basica.setObjectName("basicaWindow")
        self.ventana_determinantes.setObjectName("determinantesWindow")
        self.ventana_inversa.setObjectName("inversaWindow")
        self.ventana_avanzada.setObjectName("avanzadaWindow")
        self.ventana_ecuaciones.setObjectName("ecuacionesWindow")
        self.ventana_vectoriales.setObjectName("vectorialesWindow")

        # 4. Inicializar Navegación Lateral Organizada
        self.init_navigation()

    def init_navigation(self):
        """Registra las pantallas con iconos 100% garantizados."""
        
        # --- INICIO ---
        self.addSubInterface(self.home_window, FIF.HOME, 'Inicio')
        self.navigationInterface.addSeparator()

        # --- BLOQUE 1: MATRICES Y PROPIEDADES ---
        self.addSubInterface(self.ventana_basica, FIF.EDIT, 'Básica')
        self.addSubInterface(self.ventana_determinantes, FIF.DOCUMENT, 'Determinantes')
        self.addSubInterface(self.ventana_inversa, FIF.BOOK_SHELF if hasattr(FIF, 'BOOK_SHELF') else FIF.DOCUMENT, 'Inversa')

        self.navigationInterface.addSeparator()

        # --- BLOQUE 2: SISTEMAS Y GEOMETRÍA ---
        self.addSubInterface(self.ventana_avanzada, FIF.SETTING, 'Avanzada')
        self.addSubInterface(self.ventana_ecuaciones, FIF.DOCUMENT, 'Ecuaciones')
        self.addSubInterface(self.ventana_vectoriales, FIF.CODE if hasattr(FIF, 'CODE') else FIF.EDIT, 'Vectores')
    def navegar_a(self, modulo: str):
        """Redirige el cambio de pantalla según la clave emitida por las tarjetas del Home."""
        modulos = {
            "basica": self.ventana_basica,
            "determinantes": self.ventana_determinantes,
            "inversa": self.ventana_inversa,
            "avanzada": self.ventana_avanzada,
            "ecuaciones": self.ventana_ecuaciones,
            "vectores": self.ventana_vectoriales
        }
        if modulo in modulos:
            self.switchTo(modulos[modulo])