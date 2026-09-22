import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QStackedWidget, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QColor, QPainter, QBrush, QPen, QLinearGradient


# --- AVATAR CON CÍRCULO Y BURBUJAS DE ALTA RESOLUCIÓN ---
class HighResAvatar(QWidget):
    def __init__(self, ruta_imagen, parent=None):
        super().__init__(parent)
        self.setFixedSize(220, 220)
        self.pixmap = QPixmap(ruta_imagen)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

        # Círculo de fondo
        gradiente_circulo = QLinearGradient(20, 20, 200, 200)
        gradiente_circulo.setColorAt(0.0, QColor("#45E3FF"))
        gradiente_circulo.setColorAt(1.0, QColor("#86F3FF"))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(gradiente_circulo))
        painter.drawEllipse(15, 15, 190, 190)

        # Burbujas
        burbuja_brush = QBrush(QColor(255, 255, 255, 110))
        burbuja_pen = QPen(QColor(255, 255, 255, 210), 1.5)
        painter.setBrush(burbuja_brush)
        painter.setPen(burbuja_pen)

        burbujas = [
            (32, 55, 12), (26, 105, 16), (172, 60, 9),
            (178, 130, 11), (75, 182, 8), (95, 185, 6),
        ]
        for bx, by, br in burbujas:
            painter.drawEllipse(bx, by, br * 2, br * 2)

        # Renderizado de la beluguita
        if not self.pixmap.isNull():
            pix_escalado = self.pixmap.scaled(
                150, 150, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            x = (self.width() - pix_escalado.width()) // 2
            y = (self.height() - pix_escalado.height()) // 2 + 6
            painter.drawPixmap(x, y, pix_escalado)


# --- CLASE PRINCIPAL ---
class HomeWindow(QWidget):
    modulo_seleccionado = pyqtSignal(str)

    def __init__(self, ventana_principal=None):
        super().__init__(ventana_principal)
        self.ventana_principal = ventana_principal
        self.init_ui()

    def init_ui(self):
        self.stack = QStackedWidget(self)
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.addWidget(self.stack)

        self.stack.addWidget(self._crear_pantalla_bienvenida())
        self.stack.addWidget(self._crear_pantalla_eleccion())

    def _crear_pantalla_bienvenida(self):
        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget#PantallaBienvenida {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #A3F1FC,
                    stop:0.5 #C3F5FF,
                    stop:1 #E1FAFF
                );
            }
        """)
        contenedor.setObjectName("PantallaBienvenida")

        layout_contenedor = QVBoxLayout(contenedor)
        layout_contenedor.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QWidget()
        card.setFixedSize(450, 520)
        card.setStyleSheet("QWidget { background-color: #FFFFFF; border-radius: 32px; }")

        sombra = QGraphicsDropShadowEffect(card)
        sombra.setBlurRadius(45)
        sombra.setColor(QColor(25, 110, 140, 30))
        sombra.setYOffset(14)
        card.setGraphicsEffect(sombra)

        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.setSpacing(10)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_imagen = os.path.join(base_dir, "assets", "BelugaK1.png")
        avatar_widget = HighResAvatar(ruta_imagen)

        lbl_subtitulo = QLabel("DESKTOP · PRINCIPAL")
        lbl_subtitulo.setStyleSheet("""
            color: #7A9FB8; font-size: 12px; font-weight: 700; 
            font-family: 'Segoe UI Variable Text', 'Segoe UI', sans-serif;
            letter-spacing: 1.5px; background: transparent;
        """)

        lbl_titulo = QLabel("Calculadora")
        lbl_titulo.setStyleSheet("""
            color: #0E324E; font-size: 38px; font-weight: 800; 
            font-family: 'Segoe UI Variable Display', 'Segoe UI', sans-serif;
            background: transparent;
        """)

        btn_inicio = QPushButton("Inicio")
        btn_inicio.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_inicio.setFixedSize(180, 50)
        btn_inicio.setStyleSheet("""
            QPushButton {
                background-color: #38D8F7;
                color: #052438;
                font-size: 17px;
                font-weight: 800;
                font-family: 'Segoe UI Variable Small', 'Segoe UI', sans-serif;
                border-radius: 25px;
                border: none;
            }
            QPushButton:hover { background-color: #21CCEC; }
            QPushButton:pressed { background-color: #17B1CD; }
        """)
        btn_inicio.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        card_layout.addWidget(lbl_subtitulo, 0, Qt.AlignmentFlag.AlignCenter)
        card_layout.addSpacing(6)
        card_layout.addWidget(avatar_widget, 0, Qt.AlignmentFlag.AlignCenter)
        card_layout.addSpacing(6)
        card_layout.addWidget(lbl_titulo, 0, Qt.AlignmentFlag.AlignCenter)
        card_layout.addSpacing(18)
        card_layout.addWidget(btn_inicio, 0, Qt.AlignmentFlag.AlignCenter)

        layout_contenedor.addWidget(card)
        return contenedor

    def _crear_pantalla_eleccion(self):
        contenedor = QWidget()
        contenedor.setStyleSheet("""
            QWidget#PantallaEleccion {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #A3F1FC,
                    stop:0.5 #C3F5FF,
                    stop:1 #E1FAFF
                );
            }
        """)
        contenedor.setObjectName("PantallaEleccion")

        layout_principal = QVBoxLayout(contenedor)
        layout_principal.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QWidget()
        card.setFixedSize(700, 490)
        card.setStyleSheet("QWidget { background-color: #FFFFFF; border-radius: 28px; }")

        sombra = QGraphicsDropShadowEffect(card)
        sombra.setBlurRadius(40)
        sombra.setColor(QColor(25, 110, 140, 25))
        sombra.setYOffset(12)
        card.setGraphicsEffect(sombra)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(35, 25, 35, 30)

        # Header superior
        header_layout = QHBoxLayout()
        btn_volver = QPushButton("← Volver")
        btn_volver.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_volver.setStyleSheet("""
            QPushButton {
                color: #7A9FB8; font-size: 13px; font-weight: 700;
                font-family: 'Segoe UI Variable Text', sans-serif;
                border: none; background: transparent;
            }
            QPushButton:hover { color: #0E324E; }
        """)
        btn_volver.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        header_layout.addWidget(btn_volver)
        header_layout.addStretch()

        lbl_sub = QLabel("MÓDULOS DE CÁLCULO")
        lbl_sub.setStyleSheet("""
            color: #7A9FB8; font-size: 11px; font-weight: 800;
            font-family: 'Segoe UI Variable Text', sans-serif; letter-spacing: 1.5px;
            background: transparent;
        """)

        lbl_titulo = QLabel("¿Qué deseas calcular hoy?")
        lbl_titulo.setStyleSheet("""
            color: #0E324E; font-size: 26px; font-weight: 800;
            font-family: 'Segoe UI Variable Display', sans-serif;
            background: transparent;
        """)

        grid_opciones = QHBoxLayout()
        grid_opciones.setSpacing(16)

        opciones = [
            {
                "titulo": "Básica",
                "tag": "+ − ×",
                "desc": "Aritmética esencial, porcentajes y operaciones elementales.",
                "clave": "basica",
                "bg": "#F8FAFC",
                "border": "#E2E8F0"
            },
            {
                "titulo": "Avanzada",
                "tag": "f (x)",
                "desc": "Determinantes, matrices inversas y sistemas lineales.",
                "clave": "avanzada",
                "bg": "#F8FAFC",
                "border": "#E2E8F0"
            },
            {
                "titulo": "Vectores",
                "tag": "[ → ]",
                "desc": "Producto escalar, producto cruz, magnitudes y ángulos.",
                "clave": "vectores",
                "bg": "#F8FAFC",
                "border": "#E2E8F0"
            }
        ]

        for item in opciones:
            btn_card = QPushButton()
            btn_card.setFixedSize(196, 230)
            btn_card.setCursor(Qt.CursorShape.PointingHandCursor)

            layout_card_item = QVBoxLayout(btn_card)
            layout_card_item.setContentsMargins(18, 18, 18, 18)
            layout_card_item.setAlignment(Qt.AlignmentFlag.AlignTop)

            lbl_tag = QLabel(item["tag"])
            lbl_tag.setStyleSheet("""
                color: #1B889B; background-color: #E0F7FA;
                font-size: 11px; font-weight: 800;
                font-family: 'Consolas', monospace;
                padding: 4px 8px; border-radius: 6px;
            """)
            lbl_tag.setFixedHeight(24)

            lbl_card_title = QLabel(item["titulo"])
            lbl_card_title.setStyleSheet("""
                color: #0E324E; font-size: 18px; font-weight: 800;
                font-family: 'Segoe UI Variable Display', sans-serif;
                background: transparent;
            """)

            lbl_card_desc = QLabel(item["desc"])
            lbl_card_desc.setWordWrap(True)
            lbl_card_desc.setStyleSheet("""
                color: #64748B; font-size: 12px; font-weight: 500;
                font-family: 'Segoe UI Variable Text', sans-serif;
                line-height: 1.3; background: transparent;
            """)

            lbl_action = QLabel("Abrir módulo →")
            lbl_action.setStyleSheet("""
                color: #38D8F7; font-size: 12px; font-weight: 700;
                font-family: 'Segoe UI Variable Text', sans-serif;
                background: transparent;
            """)

            layout_card_item.addWidget(lbl_tag, 0, Qt.AlignmentFlag.AlignLeft)
            layout_card_item.addSpacing(10)
            layout_card_item.addWidget(lbl_card_title)
            layout_card_item.addSpacing(4)
            layout_card_item.addWidget(lbl_card_desc)
            layout_card_item.addStretch()
            layout_card_item.addWidget(lbl_action)

            btn_card.setStyleSheet(f"""
                QPushButton {{
                    background-color: {item['bg']};
                    border: 1.5px solid {item['border']};
                    border-radius: 18px;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: #FFFFFF;
                    border-color: #38D8F7;
                }}
            """)

            # Conexión para saltar a la pantalla correspondiente en MainWindow
            clave_actual = item["clave"]
            btn_card.clicked.connect(lambda _, c=clave_actual: self.abrir_modulo(c))
            grid_opciones.addWidget(btn_card)

        card_layout.addLayout(header_layout)
        card_layout.addSpacing(5)
        card_layout.addWidget(lbl_sub, 0, Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(lbl_titulo, 0, Qt.AlignmentFlag.AlignCenter)
        card_layout.addSpacing(22)
        card_layout.addLayout(grid_opciones)

        layout_principal.addWidget(card)
        return contenedor

    def abrir_modulo(self, clave):
        if self.ventana_principal and hasattr(self.ventana_principal, 'navegar_a'):
            self.ventana_principal.navegar_a(clave)
        else:
            self.modulo_seleccionado.emit(clave)