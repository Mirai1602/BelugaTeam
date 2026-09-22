from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget

from ui.home_window import HomeWindow
from ui.basica_window import CalculadoraMatrices
from ui.avanzada_window import CalculadoraMatricesAvanzada
from ui.vectoriales_window import VectorialesWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BelugaCalc")
        self.resize(1000, 700)

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget(self)
        layout_principal.addWidget(self.stack)

        # Instanciar las pantallas pasando la referencia del padre
        self.home_window = HomeWindow(self)
        self.ventana_basica = CalculadoraMatrices(self)
        self.ventana_avanzada = CalculadoraMatricesAvanzada(self)
        self.ventana_vectoriales = VectorialesWindow(self)

        # Añadir al stack
        self.stack.addWidget(self.home_window)          # Índice 0
        self.stack.addWidget(self.ventana_basica)       # Índice 1
        self.stack.addWidget(self.ventana_avanzada)     # Índice 2
        self.stack.addWidget(self.ventana_vectoriales)  # Índice 3

        # Conectar la señal
        self.home_window.modulo_seleccionado.connect(self.abrir_modulo)

    def abrir_modulo(self, clave):
        mapa_modulos = {
            "basica": self.ventana_basica,
            "avanzada": self.ventana_avanzada,
            "vectores": self.ventana_vectoriales
        }

        widget_destino = mapa_modulos.get(clave)
        if widget_destino:
            # Asegura que el widget sea visible antes de ponerlo en pantalla
            widget_destino.show()
            self.stack.setCurrentWidget(widget_destino)
            # Fuerza a PyQt a redibujar la interfaz de inmediato
            self.stack.update()
            