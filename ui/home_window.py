import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
    QPushButton, QStackedWidget, QGraphicsDropShadowEffect, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import (
    QPixmap, QColor, QPainter, QBrush, QPen, 
    QLinearGradient, QRadialGradient, QPainterPath, QFont
)


class BackgroundWaves(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        w = self.width()
        h = self.height()

        # 1. Fondo principal en degradado fluido
        base_grad = QLinearGradient(0, 0, w, h)
        base_grad.setColorAt(0.0, QColor("#DFF6FF"))
        base_grad.setColorAt(0.4, QColor("#F0F9FF"))
        base_grad.setColorAt(0.8, QColor("#E0F2FE"))
        base_grad.setColorAt(1.0, QColor("#BAE6FD"))
        painter.fillRect(self.rect(), QBrush(base_grad))

        # 2. Resplandor de luz superior
        glow_top = QRadialGradient(w * 0.2, h * 0.1, w * 0.4)
        glow_top.setColorAt(0.0, QColor(56, 216, 247, 90))
        glow_top.setColorAt(1.0, QColor(255, 255, 255, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(glow_top))
        painter.drawEllipse(int(w * 0.2 - w * 0.4), int(h * 0.1 - w * 0.4), int(w * 0.8), int(w * 0.8))

        # 3. Ola superior izquierda
        path1 = QPainterPath()
        path1.moveTo(0, 0)
        path1.lineTo(w * 0.55, 0)
        path1.cubicTo(w * 0.4, h * 0.35, w * 0.15, h * 0.45, 0, h * 0.5)
        path1.closeSubpath()

        grad1 = QLinearGradient(0, 0, w * 0.5, h * 0.5)
        grad1.setColorAt(0.0, QColor(56, 216, 247, 140))
        grad1.setColorAt(1.0, QColor(2, 132, 199, 20))
        painter.setBrush(QBrush(grad1))
        painter.drawPath(path1)

        # 4. Ola inferior derecha
        path2 = QPainterPath()
        path2.moveTo(w, h)
        path2.lineTo(w * 0.45, h)
        path2.cubicTo(w * 0.6, h * 0.7, w * 0.8, h * 0.6, w, h * 0.45)
        path2.closeSubpath()

        grad2 = QLinearGradient(w * 0.5, h * 0.5, w, h)
        grad2.setColorAt(0.0, QColor(2, 132, 199, 30))
        grad2.setColorAt(1.0, QColor(56, 216, 247, 120))
        painter.setBrush(QBrush(grad2))
        painter.drawPath(path2)

        # 5. Marcas matemáticas
        painter.setPen(QPen(QColor(2, 101, 151, 140), 1))
        font_symbol = QFont("Fira Code", 13, QFont.Weight.Bold)
        font_symbol.setStyleHint(QFont.StyleHint.Monospace)
        painter.setFont(font_symbol)

        painter.drawText(int(w * 0.03), int(h * 0.08), "[ a₁₁  a₁₂ ]")
        painter.drawText(int(w * 0.05), int(h * 0.13), "[ a₂₁  a₂₂ ]")
        painter.drawText(int(w * 0.03), int(h * 0.20), "det(A) ≠ 0")
        painter.drawText(int(w * 0.03), int(h * 0.26), "A⁻¹ = adj(A)/det(A)")

        painter.drawText(int(w * 0.73), int(h * 0.84), "u · v = ||u|| ||v|| cosθ")
        painter.drawText(int(w * 0.82), int(h * 0.90), "u × v = det([i, j, k])")


class MatrixBelugaAvatar(QWidget):
    def __init__(self, ruta_imagen, parent=None):
        super().__init__(parent)
        self.setFixedSize(280, 160)
        self.pixmap = QPixmap(ruta_imagen)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

        w = self.width()
        h = self.height()

        card_w, card_h = 160, 135
        card_x = int((w - card_w) / 2)
        card_y = int((h - card_h) / 2)

        gradiente = QLinearGradient(card_x, card_y, card_x + card_w, card_y + card_h)
        gradiente.setColorAt(0.0, QColor("#E0F2FE"))
        gradiente.setColorAt(1.0, QColor("#BAE6FD"))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(gradiente))
        painter.drawRoundedRect(card_x, card_y, card_w, card_h, 20, 20)

        if not self.pixmap.isNull():
            pix_escalado = self.pixmap.scaled(
                125, 125, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            x = int((w - pix_escalado.width()) / 2)
            y = int((h - pix_escalado.height()) / 2)
            painter.drawPixmap(x, y, pix_escalado)

        pen_bracket = QPen(QColor("#0284C7"), 5.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        pen_bracket.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen_bracket)

        bracket_len = 16
        r = 10
        offset_x = 8
        offset_y = 4

        top = card_y - offset_y
        bottom = card_y + card_h + offset_y
        left = card_x - offset_x
        right = card_x + card_w + offset_x

        path_l = QPainterPath()
        path_l.moveTo(left + bracket_len, top)
        path_l.lineTo(left + r, top)
        path_l.quadTo(left, top, left, top + r)
        path_l.lineTo(left, bottom - r)
        path_l.quadTo(left, bottom, left + r, bottom)
        path_l.lineTo(left + bracket_len, bottom)
        painter.drawPath(path_l)

        path_r = QPainterPath()
        path_r.moveTo(right - bracket_len, top)
        path_r.lineTo(right - r, top)
        path_r.quadTo(right, top, right, top + r)
        path_r.lineTo(right, bottom - r)
        path_r.quadTo(right, bottom, right - r, bottom)
        path_r.lineTo(right - bracket_len, bottom)
        painter.drawPath(path_r)


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
        contenedor = BackgroundWaves()

        layout_contenedor = QVBoxLayout(contenedor)
        layout_contenedor.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QWidget()
        card.setFixedSize(500, 550)
        card.setStyleSheet("""
            QWidget { 
                background-color: rgba(255, 255, 255, 0.95); 
                border-radius: 32px;
                border: 1px solid rgba(226, 232, 240, 0.9);
            }
        """)

        sombra = QGraphicsDropShadowEffect(card)
        sombra.setBlurRadius(40)
        sombra.setColor(QColor(2, 132, 199, 25))
        sombra.setYOffset(12)
        card.setGraphicsEffect(sombra)

        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.setContentsMargins(36, 32, 36, 36)
        card_layout.setSpacing(8)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_imagen = os.path.join(base_dir, "assets", "BelugaK1.png")
        avatar_widget = MatrixBelugaAvatar(ruta_imagen)

        lbl_subtitulo = QLabel("ÁLGEBRA LINEAL")
        lbl_subtitulo.setStyleSheet("""
            color: #0284C7; 
            font-size: 12px; 
            font-weight: 800; 
            font-family: 'Segoe UI', 'Montserrat', sans-serif;
            letter-spacing: 4px; 
            background: transparent; 
            border: none;
        """)

        lbl_titulo = QLabel("Calculadora Matricial")
        lbl_titulo.setStyleSheet("""
            color: #0369A1; 
            font-size: 32px; 
            font-weight: 900; 
            font-family: 'Trebuchet MS', 'Segoe UI', sans-serif;
            letter-spacing: -0.5px;
            background: transparent; 
            border: none;
        """)

        lbl_desc = QLabel("Matrices, determinantes y vectores")
        lbl_desc.setStyleSheet("""
            color: #64748B; 
            font-size: 14px; 
            font-weight: 500;
            font-family: 'Segoe UI', 'Roboto', sans-serif;
            background: transparent; 
            border: none;
        """)

        btn_inicio = QPushButton("Comenzar")
        btn_inicio.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_inicio.setFixedSize(220, 52)
        btn_inicio.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #38D8F7, stop:1 #0284C7);
                color: #FFFFFF;
                font-size: 15px;
                font-weight: 700;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                letter-spacing: 0.5px;
                border-radius: 26px;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #21CCEC, stop:1 #0369A1);
            }
        """)
        btn_inicio.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        card_layout.addWidget(lbl_subtitulo, 0, Qt.AlignmentFlag.AlignCenter)
        card_layout.addSpacing(2)
        card_layout.addWidget(avatar_widget, 0, Qt.AlignmentFlag.AlignCenter)
        card_layout.addSpacing(2)
        card_layout.addWidget(lbl_titulo, 0, Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(lbl_desc, 0, Qt.AlignmentFlag.AlignCenter)
        card_layout.addSpacing(18)
        card_layout.addWidget(btn_inicio, 0, Qt.AlignmentFlag.AlignCenter)

        layout_contenedor.addWidget(card)
        return contenedor

    def _crear_pantalla_eleccion(self):
        contenedor = BackgroundWaves()

        layout_principal = QVBoxLayout(contenedor)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        # 1. AREA DE DESPLAZAMIENTO CON BARRA VERTICAL
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(224, 242, 254, 0.5);
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #38D8F7;
                border-radius: 5px;
                min-height: 25px;
            }
            QScrollBar::handle:vertical:hover {
                background: #0284C7;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.setContentsMargins(20, 30, 20, 30)

        # Tarjeta contenedor blanca con tamaño fijo para que no se deforme
        card = QWidget()
        card.setFixedWidth(780)
        card.setStyleSheet("""
            QWidget { 
                background-color: rgba(255, 255, 255, 0.95); 
                border-radius: 32px; 
                border: 1px solid rgba(226, 232, 240, 0.9);
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(35, 28, 35, 35)

        # Cabecera con botón Volver
        header_layout = QHBoxLayout()
        btn_volver = QPushButton("← Volver")
        btn_volver.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_volver.setStyleSheet("""
            QPushButton {
                color: #64748B; 
                font-size: 13px; 
                font-weight: 700;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                border: none; 
                background: transparent;
            }
            QPushButton:hover { color: #0284C7; }
        """)
        btn_volver.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        header_layout.addWidget(btn_volver)
        header_layout.addStretch()

        lbl_sub = QLabel("MÓDULOS DE CÁLCULO")
        lbl_sub.setStyleSheet("""
            color: #0284C7; 
            font-size: 11px; 
            font-weight: 800;
            font-family: 'Segoe UI', 'Roboto', sans-serif;
            letter-spacing: 3px; 
            background: transparent; 
            border: none;
        """)

        lbl_titulo = QLabel("¿Qué deseas calcular hoy?")
        lbl_titulo.setStyleSheet("""
            color: #0369A1; 
            font-size: 26px; 
            font-weight: 800;
            font-family: 'Trebuchet MS', 'Segoe UI', sans-serif;
            letter-spacing: -0.5px;
            background: transparent; 
            border: none;
        """)

        # 2. CUADRÍCULA DE 2 COLUMNAS (3 FILAS)
        grid_opciones = QGridLayout()
        grid_opciones.setSpacing(16)

        opciones = [
            # Fila 1
            {
                "titulo": "Básica",
                "tag": "[ + − ]",
                "desc": "Suma, resta y multiplicación por escalar.",
                "clave": "basica"
            },
            {
                "titulo": "Determinantes",
                "tag": "[ |A| ]",
                "desc": "Cálculo por cofactores y reducción gaussiana.",
                "clave": "determinantes"
            },
            # Fila 2
            {
                "titulo": "Inversa",
                "tag": "[ A⁻¹ ]",
                "desc": "Cálculo de la matriz inversa paso a paso.",
                "clave": "inversa"
            },
            {
                "titulo": "Avanzada",
                "tag": "[ AX=B ]",
                "desc": "Sistemas de ecuaciones matriciales.",
                "clave": "avanzada"
            },
            # Fila 3
            {
                "titulo": "Ecuaciones Matriciales",
                "tag": "[ A·X ]",
                "desc": "Resolución de ecuaciones matriciales complejas.",
                "clave": "ecuaciones"
            },
            {
                "titulo": "Vectores",
                "tag": "[ u · v ]",
                "desc": "Producto escalar, producto cruz y norma.",
                "clave": "vectores"
            }
        ]

        for index, item in enumerate(opciones):
            btn_card = QPushButton()
            btn_card.setFixedSize(340, 160)
            btn_card.setCursor(Qt.CursorShape.PointingHandCursor)

            layout_card_item = QVBoxLayout(btn_card)
            layout_card_item.setContentsMargins(18, 16, 18, 16)
            layout_card_item.setAlignment(Qt.AlignmentFlag.AlignTop)

            lbl_tag = QLabel(item["tag"])
            lbl_tag.setStyleSheet("""
                color: #0284C7; 
                background-color: #E0F2FE;
                font-size: 11px; 
                font-weight: 800;
                font-family: 'Consolas', monospace;
                padding: 4px 8px; 
                border-radius: 6px; 
                border: none;
            """)
            lbl_tag.setFixedHeight(24)

            lbl_card_title = QLabel(item["titulo"])
            lbl_card_title.setStyleSheet("""
                color: #0F172A; 
                font-size: 17px; 
                font-weight: 800;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                background: transparent; 
                border: none;
            """)

            lbl_card_desc = QLabel(item["desc"])
            lbl_card_desc.setWordWrap(True)
            lbl_card_desc.setStyleSheet("""
                color: #64748B; 
                font-size: 12px; 
                font-weight: 500;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                line-height: 1.2; 
                background: transparent; 
                border: none;
            """)

            lbl_action = QLabel("Abrir módulo →")
            lbl_action.setStyleSheet("""
                color: #0284C7; 
                font-size: 12px; 
                font-weight: 700;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                background: transparent; 
                border: none;
            """)

            layout_card_item.addWidget(lbl_tag, 0, Qt.AlignmentFlag.AlignLeft)
            layout_card_item.addSpacing(6)
            layout_card_item.addWidget(lbl_card_title)
            layout_card_item.addSpacing(4)
            layout_card_item.addWidget(lbl_card_desc)
            layout_card_item.addStretch()
            layout_card_item.addWidget(lbl_action)

            btn_card.setStyleSheet("""
                QPushButton {
                    background-color: #F8FAFC;
                    border: 1.5px solid #E2E8F0;
                    border-radius: 18px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #FFFFFF;
                    border-color: #38D8F7;
                }
            """)

            clave_actual = item["clave"]
            btn_card.clicked.connect(lambda _, c=clave_actual: self.abrir_modulo(c))

            # Acomodar en 2 columnas por fila
            row = index // 2
            col = index % 2
            grid_opciones.addWidget(btn_card, row, col)

        card_layout.addLayout(header_layout)
        card_layout.addSpacing(4)
        card_layout.addWidget(lbl_sub, 0, Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(lbl_titulo, 0, Qt.AlignmentFlag.AlignCenter)
        card_layout.addSpacing(18)
        card_layout.addLayout(grid_opciones)

        scroll_layout.addWidget(card)
        scroll_area.setWidget(scroll_content)
        layout_principal.addWidget(scroll_area)

        return contenedor

    def abrir_modulo(self, clave):
        self.modulo_seleccionado.emit(clave)
        if self.ventana_principal and hasattr(self.ventana_principal, 'navegar_a'):
            self.ventana_principal.navegar_a(clave)