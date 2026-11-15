
"""Ventana principal de BelugaCalc con barra lateral en forma de S."""

from PyQt6.QtCore import (
    Qt,
    QPropertyAnimation,
    QEasingCurve,
    QVariantAnimation,
    QSize,
    QPointF
)

from PyQt6.QtGui import (
    QPainter,
    QPainterPath,
    QColor,
    QIcon,
    QPixmap,
    QFont
)

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QStackedWidget,
    QLabel
)

from qfluentwidgets import FluentIcon as FIF

from ui.home_window import HomeWindow
from ui.basica_window import CalculadoraMatrices
from ui.avanzada_window import CalculadoraMatricesAvanzada
from ui.vectoriales_window import VectorialesWindow
from ui.ecuaciones_window import EcuacionesWindow
from ui.inversa_window import InversaWindow
from ui.determinantes_window import DeterminantesWindow
from ui.biseccion_window import BiseccionWindow
from ui.regula_falsi_window import RegulaFalsiWindow
from ui.metodos_abiertos_window import MetodosAbiertosWindow


# ==========================================
# COLORES ORIGINALES DE BELUGACALC
# ==========================================

COLOR_BARRA_FONDO = "#063D89"
COLOR_CIRCULO_ACTIVO = "#62B9FF"
COLOR_ICONO_ACTIVO = "#1A1C29"
COLOR_ICONO_INACTIVO = "#FFFFFF"


# ==========================================
# ICONOS MATEMÁTICOS
# ==========================================

def obtener_icono(*nombres):
    """
    Busca un icono disponible en FluentIcon.

    Se proporciona más de una alternativa para
    mantener compatibilidad entre versiones
    de qfluentwidgets.
    """
    for nombre in nombres:
        icono = getattr(FIF, nombre, None)

        if icono is not None:
            return icono.icon()

    return FIF.DOCUMENT.icon()


def colorear_icono(qicon, color_hex):
    """Colorea un icono sin perder su transparencia."""

    pixmap = qicon.pixmap(QSize(22, 22))

    resultado = QPixmap(pixmap.size())
    resultado.fill(Qt.GlobalColor.transparent)

    painter = QPainter(resultado)

    painter.setCompositionMode(
        QPainter.CompositionMode.CompositionMode_Source
    )
    painter.drawPixmap(0, 0, pixmap)

    painter.setCompositionMode(
        QPainter.CompositionMode.CompositionMode_SourceIn
    )
    painter.fillRect(
        resultado.rect(),
        QColor(color_hex)
    )

    painter.end()

    return QIcon(resultado)


# ==========================================
# BOTÓN INDIVIDUAL DE NAVEGACIÓN
# ==========================================

class BotonNavegacion(QWidget):

    def __init__(self, icono, texto, indice, parent=None):
        super().__init__(parent)

        self.indice = indice
        self.texto_str = texto
        self.qicon_base = icono

        self.es_nombre_largo = (
            texto == "Newton-Raphson y Secante"
        )

        self.setFixedHeight(50)

        self.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.layout_intern = QHBoxLayout(self)

        self.layout_intern.setContentsMargins(
            14, 0, 10, 0
        )

        self.layout_intern.setSpacing(12)

        # Icono
        self.btn_icon = QPushButton(self)

        self.btn_icon.setFixedSize(38, 38)
        self.btn_icon.setIconSize(QSize(22, 22))

        self.btn_icon.setFocusPolicy(
            Qt.FocusPolicy.NoFocus
        )

        self.btn_icon.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            True
        )

        self.btn_icon.setStyleSheet("""
            QPushButton {
                background:transparent;
                border:none;
                padding:0px;
                margin:0px;
            }
        """)

        # Texto
        self.lbl_text = QLabel(texto, self)

        self.lbl_text.setAlignment(
            Qt.AlignmentFlag.AlignVCenter
            | Qt.AlignmentFlag.AlignLeft
        )

        self.lbl_text.setWordWrap(
            self.es_nombre_largo
        )

        self.lbl_text.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            True
        )

        self.lbl_text.hide()

        self.layout_intern.addWidget(
            self.btn_icon,
            0,
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.layout_intern.addWidget(
            self.lbl_text,
            1
        )

        self.set_estado_activo(False)

    def set_estado_activo(self, activo):
        """
        Cambia el color del icono y del texto
        sin modificar la forma de la barra.
        """

        color_icono = (
            COLOR_ICONO_ACTIVO
            if activo
            else COLOR_ICONO_INACTIVO
        )

        self.btn_icon.setIcon(
            colorear_icono(
                self.qicon_base,
                color_icono
            )
        )

        color_texto = (
            COLOR_CIRCULO_ACTIVO
            if activo
            else COLOR_ICONO_INACTIVO
        )

        # Tamaño especial para el nombre más largo
        tamano = (
            12 if self.es_nombre_largo else 14
        )

        peso = (
            600 if activo else 500
        )

        fuente = QFont("Poppins")
        fuente.setPointSize(tamano)
        fuente.setWeight(
            QFont.Weight.DemiBold
            if activo
            else QFont.Weight.Medium
        )

        self.lbl_text.setFont(fuente)

        self.lbl_text.setStyleSheet(f"""
            QLabel {{
                color:{color_texto};
                background:transparent;
                border:none;
                font-weight:{peso};
            }}
        """)

        if activo:
            self.layout_intern.setContentsMargins(
                19, 0, 10, 0
            )
        else:
            self.layout_intern.setContentsMargins(
                14, 0, 10, 0
            )

    def set_expandido(self, expandido):
        self.lbl_text.setVisible(expandido)

    def mousePressEvent(self, event):
        padre = self.parent()

        if hasattr(padre, "on_boton_clicked"):
            padre.on_boton_clicked(self.indice)

        super().mousePressEvent(event)


# ==========================================
# BARRA LATERAL CON FORMA ORIGINAL DE S
# ==========================================

class PillSidebar(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.expandido = False
        self.indice_activo = 0

        self.pos_y_centro_muesca = 0.0
        self.muesca_inicializada = False

        self.botones = []
        self.callbacks = []

        self.anim_muesca = None
        self.anim = None
        self.anim_max = None

        # Mantenemos exactamente el ancho original
        self.setFixedWidth(66)

        self.init_ui()

    def init_ui(self):
        self.layout_main = QVBoxLayout(self)

        self.layout_main.setContentsMargins(
            0, 16, 0, 16
        )

        self.layout_main.setSpacing(10)

        self.btn_menu = QPushButton("☰", self)

        self.btn_menu.setFixedSize(38, 38)

        self.btn_menu.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.btn_menu.setStyleSheet("""
            QPushButton {
                background:transparent;
                color:#FFFFFF;
                font-size:20px;
                font-weight:bold;
                border:none;
                padding:0px;
                margin-left:14px;
                text-align:left;
            }

            QPushButton:hover {
                color:#62B9FF;
            }
        """)

        self.btn_menu.clicked.connect(
            self.toggle_expansion
        )

        self.layout_main.addWidget(
            self.btn_menu
        )

    def agregar_opcion(self, icono, texto, callback):
        indice = len(self.botones)

        boton = BotonNavegacion(
            icono,
            texto,
            indice,
            self
        )

        self.botones.append(boton)
        self.callbacks.append(callback)

        self.layout_main.addWidget(boton)

        if indice == 0:
            boton.set_estado_activo(True)

    def showEvent(self, event):
        super().showEvent(event)

        if (
            not self.muesca_inicializada
            and len(self.botones) > self.indice_activo
        ):
            boton = self.botones[
                self.indice_activo
            ]

            self.pos_y_centro_muesca = float(
                boton.y()
                + boton.height() / 2
            )

            self.muesca_inicializada = True
            self.update()

    def on_boton_clicked(self, indice):
        self.seleccionar_boton(indice)

    def seleccionar_boton(self, indice):
        if indice < 0 or indice >= len(self.botones):
            return

        self.indice_activo = indice

        for i, boton in enumerate(self.botones):
            boton.set_estado_activo(
                i == indice
            )

        objetivo = self.botones[indice]

        centro = float(
            objetivo.y()
            + objetivo.height() / 2
        )

        if (
            self.anim_muesca is not None
            and self.anim_muesca.state()
            == QVariantAnimation.State.Running
        ):
            self.anim_muesca.stop()

        self.anim_muesca = QVariantAnimation(self)

        self.anim_muesca.setDuration(220)

        self.anim_muesca.setStartValue(
            self.pos_y_centro_muesca
        )

        self.anim_muesca.setEndValue(
            centro
        )

        self.anim_muesca.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )

        def actualizar_muesca(valor):
            self.pos_y_centro_muesca = float(valor)
            self.update()

        self.anim_muesca.valueChanged.connect(
            actualizar_muesca
        )

        self.anim_muesca.start()

        if indice < len(self.callbacks):
            self.callbacks[indice]()

    def toggle_expansion(self):
        self.expandido = not self.expandido

        # Conservamos 230 px y 66 px
        ancho = (
            230 if self.expandido else 66
        )

        self.btn_menu.setText(
            "  ☰  Menú"
            if self.expandido
            else "☰"
        )

        self.anim = QPropertyAnimation(
            self,
            b"minimumWidth"
        )

        self.anim.setDuration(220)

        self.anim.setStartValue(
            self.width()
        )

        self.anim.setEndValue(
            ancho
        )

        self.anim.setEasingCurve(
            QEasingCurve.Type.InOutQuad
        )

        self.anim_max = QPropertyAnimation(
            self,
            b"maximumWidth"
        )

        self.anim_max.setDuration(220)

        self.anim_max.setStartValue(
            self.width()
        )

        self.anim_max.setEndValue(
            ancho
        )

        self.anim_max.setEasingCurve(
            QEasingCurve.Type.InOutQuad
        )

        for boton in self.botones:
            boton.set_expandido(
                self.expandido
            )

        self.anim.start()
        self.anim_max.start()

    # ======================================
    # FORMA DE S ORIGINAL - NO MODIFICADA
    # ======================================

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        ancho = float(self.width())
        alto = float(self.height())
        radio = 30.0

        path = QPainterPath()

        path.addRoundedRect(
            0,
            0,
            ancho,
            alto,
            radio,
            radio
        )

        if (
            self.botones
            and self.pos_y_centro_muesca > 0
        ):
            cy = self.pos_y_centro_muesca

            profundidad = (
                40.0
                if self.expandido
                else 56.0
            )

            recorte = QPainterPath()

            recorte.moveTo(
                ancho,
                cy - 52
            )

            recorte.cubicTo(
                ancho - 2,
                cy - 36,
                ancho - profundidad,
                cy - 28,
                ancho - profundidad,
                cy
            )

            recorte.cubicTo(
                ancho - profundidad,
                cy + 28,
                ancho - 2,
                cy + 36,
                ancho,
                cy + 52
            )

            recorte.lineTo(
                ancho,
                cy - 52
            )

            path = path.subtracted(
                recorte
            )

        painter.setBrush(
            QColor(COLOR_BARRA_FONDO)
        )

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.drawPath(path)

        if (
            self.botones
            and self.pos_y_centro_muesca > 0
        ):
            painter.setBrush(
                QColor(COLOR_CIRCULO_ACTIVO)
            )

            painter.drawEllipse(
                QPointF(
                    38.0,
                    self.pos_y_centro_muesca
                ),
                19.0,
                19.0
            )

        painter.end()


# ==========================================
# VENTANA PRINCIPAL
# ==========================================

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "BelugaCalc"
        )

        self.resize(
            1150,
            750
        )

        self.setStyleSheet("""
            QMainWindow {
                background-color:#F8FAFC;
            }
        """)

        central_widget = QWidget(self)

        self.setCentralWidget(
            central_widget
        )

        main_layout = QHBoxLayout(
            central_widget
        )

        main_layout.setContentsMargins(
            12, 12, 12, 12
        )

        main_layout.setSpacing(15)

        # ==================================
        # CREAR PANTALLAS
        # ==================================

        self.home_window = HomeWindow(self)

        self.ventana_basica = (
            CalculadoraMatrices(self)
        )

        self.ventana_determinantes = (
            DeterminantesWindow(self)
        )

        self.ventana_inversa = (
            InversaWindow(self)
        )

        self.ventana_avanzada = (
            CalculadoraMatricesAvanzada(self)
        )

        self.ventana_ecuaciones = (
            EcuacionesWindow(self)
        )

        self.ventana_vectoriales = (
            VectorialesWindow(self)
        )

        self.ventana_biseccion = (
            BiseccionWindow(self)
        )

        self.ventana_regula_falsi = (
            RegulaFalsiWindow(self)
        )

        self.ventana_metodos_abiertos = (
            MetodosAbiertosWindow(self)
        )

        # ==================================
        # STACK PRINCIPAL
        # ==================================

        self.stack = QStackedWidget(self)

        pantallas = [
            self.home_window,              # 0
            self.ventana_basica,           # 1
            self.ventana_determinantes,    # 2
            self.ventana_inversa,          # 3
            self.ventana_avanzada,         # 4
            self.ventana_ecuaciones,       # 5
            self.ventana_vectoriales,      # 6
            self.ventana_biseccion,        # 7
            self.ventana_regula_falsi,     # 8
            self.ventana_metodos_abiertos  # 9
        ]

        for pantalla in pantallas:
            self.stack.addWidget(
                pantalla
            )

        self.home_window.modulo_seleccionado.connect(
            self.navegar_a
        )

        # ==================================
        # BARRA LATERAL
        # ==================================

        self.sidebar = PillSidebar(self)

        # Iconos específicos para cada tema
        opciones = [
            (
                obtener_icono("HOME"),
                "Inicio",
                0
            ),
            (
                obtener_icono(
                    "CALCULATOR", "EDIT"
                ),
                "Básica",
                1
            ),
            (
                obtener_icono(
                    "TILES", "DOCUMENT"
                ),
                "Determinantes",
                2
            ),
            (
                obtener_icono(
                    "SYNC", "ROTATE", "DOCUMENT"
                ),
                "Inversa",
                3
            ),
            (
                obtener_icono(
                    "APPLICATION", "SETTING"
                ),
                "Avanzada",
                4
            ),
            (
                obtener_icono(
                    "CODE", "EDIT"
                ),
                "Ecuaciones",
                5
            ),
            (
                obtener_icono(
                    "UP", "RIGHT_ARROW", "EDIT"
                ),
                "Vectores",
                6
            ),
            (
                obtener_icono(
                    "ZOOM_IN", "SEARCH"
                ),
                "Bisección",
                7
            ),
            (
                obtener_icono(
                    "TRENDING", "CHART", "SEARCH"
                ),
                "Regula Falsi",
                8
            ),
            (
                obtener_icono(
                    "CHART", "TRENDING", "SETTING"
                ),
                "Newton-Raphson y Secante",
                9
            )
        ]

        for icono, texto, indice in opciones:
            self.sidebar.agregar_opcion(
                icono,
                texto,
                lambda i=indice: self.abrir_pantalla(i)
            )

        main_layout.addWidget(
            self.sidebar
        )

        main_layout.addWidget(
            self.stack,
            1
        )

        self.stack.setCurrentIndex(0)

    # ======================================
    # NAVEGACIÓN DESDE BARRA LATERAL
    # ======================================

    def abrir_pantalla(self, indice):
        if indice == 9:
            self.ventana_metodos_abiertos.mostrar_newton()

        self.stack.setCurrentIndex(
            indice
        )

    def abrir_metodos_abiertos(self):
        self.abrir_pantalla(9)

    # ======================================
    # NAVEGACIÓN DESDE MENÚ PRINCIPAL
    # ======================================

    def navegar_a(self, modulo: str):

        mapping = {
            "basica": 1,
            "determinantes": 2,
            "inversa": 3,
            "avanzada": 4,
            "ecuaciones": 5,
            "vectores": 6,
            "biseccion": 7,
            "regula_falsi": 8,
            "metodos_abiertos": 9,

            # Compatibilidad
            "newton_raphson": 9,
            "secante": 9
        }

        if modulo not in mapping:
            return

        indice = mapping[modulo]

        if indice == 9:
            self.ventana_metodos_abiertos.mostrar_newton()

        self.stack.setCurrentIndex(
            indice
        )

        if indice < len(self.sidebar.botones):
            self.sidebar.seleccionar_boton(
                indice
            )
