import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QStackedWidget, QLabel
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QVariantAnimation, QSize, QPointF
from PyQt6.QtGui import QPainter, QPainterPath, QColor, QIcon, QPixmap

from qfluentwidgets import FluentIcon as FIF

from ui.home_window import HomeWindow
from ui.basica_window import CalculadoraMatrices
from ui.avanzada_window import CalculadoraMatricesAvanzada
from ui.vectoriales_window import VectorialesWindow
from ui.ecuaciones_window import EcuacionesWindow
from ui.inversa_window import InversaWindow
from ui.determinantes_window import DeterminantesWindow 


# PALETA DE COLORES
COLOR_BARRA_FONDO = "#063D89"    
COLOR_CIRCULO_ACTIVO = "#62B9FF"  # Celeste Pastel Neón
COLOR_ICONO_ACTIVO = "#1A1C29"    # Color troquelado oscuro
COLOR_ICONO_INACTIVO = "#FFFFFF"  # Blanco puro


def colorear_icono(qicon, color_hex):
    """Convierte un QIcon a un color sólido específico (22x22)."""
    pixmap = qicon.pixmap(QSize(22, 22))
    colored_pixmap = QPixmap(pixmap.size())
    colored_pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(colored_pixmap)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
    painter.drawPixmap(0, 0, pixmap)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(colored_pixmap.rect(), QColor(color_hex))
    painter.end()

    return QIcon(colored_pixmap)


class BotonNavegacion(QWidget):
    """Botón con alineación perfecta para situar el ícono en el centro del círculo."""
    def __init__(self, icono, texto, indice, parent=None):
        super().__init__(parent)
        self.indice = indice
        self.texto_str = texto
        self.qicon_base = icono

        self.setFixedHeight(50)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.layout_intern = QHBoxLayout(self)
        self.layout_intern.setContentsMargins(0, 0, 0, 0)
        self.layout_intern.setSpacing(12)

        # Contenedor del ícono (38x38 px)
        self.btn_icon = QPushButton(self)
        self.btn_icon.setFixedSize(38, 38)
        self.btn_icon.setIconSize(QSize(22, 22))
        self.btn_icon.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_icon.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        # Texto para menú desplegable
        self.lbl_text = QLabel(texto, self)
        self.lbl_text.setStyleSheet("color: #FFFFFF; font-size: 14px; font-weight: 500;")
        self.lbl_text.hide()

        self.layout_intern.addWidget(self.btn_icon, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.layout_intern.addWidget(self.lbl_text, 1)

        self.set_estado_activo(False)

    def set_estado_activo(self, activo):
        if activo:
            # Estado activo: Centramos el ícono exactamente a 19px de margen (Centro X = 38px)
            icon_oscuro = colorear_icono(self.qicon_base, COLOR_ICONO_ACTIVO)
            self.btn_icon.setIcon(icon_oscuro)
            self.btn_icon.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    padding: 0px;
                    margin: 0px;
                }
            """)
            self.lbl_text.setStyleSheet(f"color: {COLOR_CIRCULO_ACTIVO}; font-size: 14px; font-weight: bold;")
            self.layout_intern.setContentsMargins(19, 0, 10, 0)
        else:
            # Estado inactivo: Centrado en el cuerpo estándar de la barra
            icon_blanco = colorear_icono(self.qicon_base, COLOR_ICONO_INACTIVO)
            self.btn_icon.setIcon(icon_blanco)
            self.btn_icon.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    padding: 0px;
                    margin: 0px;
                }
            """)
            self.lbl_text.setStyleSheet("color: #FFFFFF; font-size: 14px; font-weight: 500;")
            self.layout_intern.setContentsMargins(14, 0, 10, 0)

    def set_expandido(self, expandido):
        if expandido:
            self.lbl_text.show()
        else:
            self.lbl_text.hide()

    def mousePressEvent(self, event):
        if hasattr(self.parent(), "on_boton_clicked"):
            self.parent().on_boton_clicked(self.indice)
        super().mousePressEvent(event)


class PillSidebar(QWidget):
    """Barra cápsula con muesca en S suave, amplia y redondeada."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.expandido = False
        self.indice_activo = 0
        self.pos_y_centro_muesca = 0.0
        self.muesca_inicializada = False
        self.botones = []
        self.callbacks = []
        self.anim_muesca = None

        self.setFixedWidth(66)
        self.init_ui()

    def init_ui(self):
        self.layout_main = QVBoxLayout(self)
        self.layout_main.setContentsMargins(0, 16, 0, 16)
        self.layout_main.setSpacing(10)

        # Botón Hamburguesa ☰
        self.btn_menu = QPushButton("☰", self)
        self.btn_menu.setFixedSize(38, 38)
        self.btn_menu.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_menu.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #FFFFFF;
                font-size: 20px;
                font-weight: bold;
                border: none;
                padding: 0px;
                margin-left: 14px;
                text-align: left;
            }
            QPushButton:hover { color: #62B9FF; }
        """)
        self.btn_menu.clicked.connect(self.toggle_expansion)
        self.layout_main.addWidget(self.btn_menu)

    def agregar_opcion(self, icono, texto, callback):
        idx = len(self.botones)
        btn = BotonNavegacion(icono, texto, idx, self)
        
        self.botones.append(btn)
        self.callbacks.append(callback)
        self.layout_main.addWidget(btn)

        if idx == 0:
            btn.set_estado_activo(True)

    def showEvent(self, event):
        super().showEvent(event)
        if not self.muesca_inicializada and len(self.botones) > self.indice_activo:
            btn_target = self.botones[self.indice_activo]
            self.pos_y_centro_muesca = float(btn_target.y() + (btn_target.height() / 2))
            self.muesca_inicializada = True
            self.update()

    def on_boton_clicked(self, idx):
        self.seleccionar_boton(idx)

    def seleccionar_boton(self, idx):
        self.indice_activo = idx
        
        for i, b in enumerate(self.botones):
            b.set_estado_activo(i == idx)

        btn_target = self.botones[idx]
        target_center_y = float(btn_target.y() + (btn_target.height() / 2))

        if self.anim_muesca and self.anim_muesca.state() == QVariantAnimation.State.Running:
            self.anim_muesca.stop()

        self.anim_muesca = QVariantAnimation(self)
        self.anim_muesca.setDuration(220)
        self.anim_muesca.setStartValue(self.pos_y_centro_muesca)
        self.anim_muesca.setEndValue(target_center_y)
        self.anim_muesca.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        def update_muesca(val):
            self.pos_y_centro_muesca = float(val)
            self.update()

        self.anim_muesca.valueChanged.connect(update_muesca)
        self.anim_muesca.start()

        if idx < len(self.callbacks):
            self.callbacks[idx]()

    def toggle_expansion(self):
        self.expandido = not self.expandido
        ancho_objetivo = 230 if self.expandido else 66
        
        self.btn_menu.setText("  ☰  Menú" if self.expandido else "☰")

        self.anim = QPropertyAnimation(self, b"minimumWidth")
        self.anim.setDuration(220)
        self.anim.setStartValue(self.width())
        self.anim.setEndValue(ancho_objetivo)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        self.anim_max = QPropertyAnimation(self, b"maximumWidth")
        self.anim_max.setDuration(220)
        self.anim_max.setStartValue(self.width())
        self.anim_max.setEndValue(ancho_objetivo)
        self.anim_max.setEasingCurve(QEasingCurve.Type.InOutQuad)

        for b in self.botones:
            b.set_expandido(self.expandido)

        self.anim.start()
        self.anim_max.start()

    def paintEvent(self, event):
        """Muesca en 'S' más hundida y redonda, envolviendo al círculo pastel perfectamente."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = float(self.width())
        h = float(self.height())
        r = 30.0

        path = QPainterPath()
        path.addRoundedRect(0, 0, w, h, r, r)

        if len(self.botones) > 0 and self.pos_y_centro_muesca > 0:
            cy = self.pos_y_centro_muesca
            profundidad = 40.0 if self.expandido else 56.0

            # 1. Recorte Bézier amplio y suave en 'S'
            cutout = QPainterPath()
            cutout.moveTo(w, cy - 52)
            cutout.cubicTo(w - 2, cy - 36, w - profundidad, cy - 28, w - profundidad, cy)
            cutout.cubicTo(w - profundidad, cy + 28, w - 2, cy + 36, w, cy + 52)
            cutout.lineTo(w, cy - 52)

            path = path.subtracted(cutout)

            # 2. Dibujar cápsula
            painter.setBrush(QColor(COLOR_BARRA_FONDO))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPath(path)

            # 3. Dibujar círculo celeste perfectamente centrado sobre el ícono (Centro X = 19 + 19 = 38px)
            radio_circulo = 19.0  # Diámetro 38px
            centro_x = 38.0
            
            painter.setBrush(QColor(COLOR_CIRCULO_ACTIVO))
            painter.drawEllipse(QPointF(centro_x, cy), radio_circulo, radio_circulo)
        else:
            painter.setBrush(QColor(COLOR_BARRA_FONDO))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPath(path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BelugaCalc")
        self.resize(1150, 750)
        self.setStyleSheet("QMainWindow { background-color: #F8FAFC; }")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(15)

        # 1. Instanciar Pantallas
        self.home_window = HomeWindow(self)
        self.ventana_basica = CalculadoraMatrices(self)
        self.ventana_determinantes = DeterminantesWindow(self)
        self.ventana_inversa = InversaWindow(self)
        self.ventana_avanzada = CalculadoraMatricesAvanzada(self)
        self.ventana_ecuaciones = EcuacionesWindow(self)
        self.ventana_vectoriales = VectorialesWindow(self)

        # 2. StackedWidget
        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.home_window)           # 0
        self.stack.addWidget(self.ventana_basica)        # 1
        self.stack.addWidget(self.ventana_determinantes)  # 2
        self.stack.addWidget(self.ventana_inversa)       # 3
        self.stack.addWidget(self.ventana_avanzada)      # 4
        self.stack.addWidget(self.ventana_ecuaciones)     # 5
        self.stack.addWidget(self.ventana_vectoriales)   # 6

        self.home_window.modulo_seleccionado.connect(self.navegar_a)

        # 3. Sidebar Personalizado
        self.sidebar = PillSidebar(self)
        
        self.sidebar.agregar_opcion(FIF.HOME.icon(), "Inicio", lambda: self.stack.setCurrentIndex(0))
        self.sidebar.agregar_opcion(FIF.EDIT.icon(), "Básica", lambda: self.stack.setCurrentIndex(1))
        self.sidebar.agregar_opcion(FIF.DOCUMENT.icon(), "Determinantes", lambda: self.stack.setCurrentIndex(2))
        self.sidebar.agregar_opcion(FIF.BOOK_SHELF.icon() if hasattr(FIF, 'BOOK_SHELF') else FIF.DOCUMENT.icon(), "Inversa", lambda: self.stack.setCurrentIndex(3))
        self.sidebar.agregar_opcion(FIF.SETTING.icon(), "Avanzada", lambda: self.stack.setCurrentIndex(4))
        self.sidebar.agregar_opcion(FIF.DOCUMENT.icon(), "Ecuaciones", lambda: self.stack.setCurrentIndex(5))
        self.sidebar.agregar_opcion(FIF.CODE.icon() if hasattr(FIF, 'CODE') else FIF.EDIT.icon(), "Vectores", lambda: self.stack.setCurrentIndex(6))

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack, 1)

    def navegar_a(self, modulo: str):
        mapping = {
            "basica": 1,
            "determinantes": 2,
            "inversa": 3,
            "avanzada": 4,
            "ecuaciones": 5,
            "vectores": 6
        }
        if modulo in mapping:
            idx = mapping[modulo]
            self.stack.setCurrentIndex(idx)
            if idx < len(self.sidebar.botones):
                self.sidebar.seleccionar_boton(idx)