
"""Pantalla de bienvenida y menú principal de BelugaCalc."""

import os

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import (
    QColor, QPainter, QBrush, QPen, QPixmap,
    QLinearGradient, QRadialGradient,
    QPainterPath, QFont
)
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton,
    QStackedWidget, QGraphicsDropShadowEffect,
    QScrollArea, QSizePolicy
)


class BackgroundWaves(QWidget):
    """Fondo con degradados y símbolos matemáticos."""

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing, True
        )

        w = float(self.width())
        h = float(self.height())

        fondo = QLinearGradient(0, 0, w, h)
        fondo.setColorAt(0.0, QColor("#F8FAFC"))
        fondo.setColorAt(0.4, QColor("#F0F9FF"))
        fondo.setColorAt(0.8, QColor("#E0F2FE"))
        fondo.setColorAt(1.0, QColor("#BAE6FD"))

        painter.fillRect(self.rect(), QBrush(fondo))

        brillo = QRadialGradient(
            w * 0.2, h * 0.1, w * 0.4
        )
        brillo.setColorAt(
            0.0, QColor(56, 216, 247, 45)
        )
        brillo.setColorAt(
            1.0, QColor(255, 255, 255, 0)
        )

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(brillo))
        painter.drawEllipse(
            int(w * 0.2 - w * 0.4),
            int(h * 0.1 - w * 0.4),
            int(w * 0.8),
            int(w * 0.8)
        )

        ola1 = QPainterPath()
        ola1.moveTo(0, 0)
        ola1.lineTo(w * 0.55, 0)
        ola1.cubicTo(
            w * 0.4, h * 0.35,
            w * 0.15, h * 0.45,
            0, h * 0.5
        )
        ola1.closeSubpath()

        grad1 = QLinearGradient(
            0, 0, w * 0.5, h * 0.5
        )
        grad1.setColorAt(
            0.0, QColor(56, 216, 247, 50)
        )
        grad1.setColorAt(
            1.0, QColor(2, 132, 199, 10)
        )

        painter.setBrush(QBrush(grad1))
        painter.drawPath(ola1)

        ola2 = QPainterPath()
        ola2.moveTo(w, h)
        ola2.lineTo(w * 0.45, h)
        ola2.cubicTo(
            w * 0.6, h * 0.7,
            w * 0.8, h * 0.6,
            w, h * 0.45
        )
        ola2.closeSubpath()

        grad2 = QLinearGradient(
            w * 0.5, h * 0.5, w, h
        )
        grad2.setColorAt(
            0.0, QColor(2, 132, 199, 15)
        )
        grad2.setColorAt(
            1.0, QColor(56, 216, 247, 45)
        )

        painter.setBrush(QBrush(grad2))
        painter.drawPath(ola2)

        painter.setPen(
            QPen(QColor(2, 101, 151, 45), 1)
        )

        fuente = QFont("Georgia", 13)
        fuente.setItalic(True)
        painter.setFont(fuente)

        painter.drawText(
            int(w * 0.03), int(h * 0.08),
            "[ a₁₁  a₁₂ ]"
        )
        painter.drawText(
            int(w * 0.05), int(h * 0.13),
            "[ a₂₁  a₂₂ ]"
        )
        painter.drawText(
            int(w * 0.03), int(h * 0.20),
            "det(A) ≠ 0"
        )
        painter.drawText(
            int(w * 0.03), int(h * 0.26),
            "A⁻¹ = adj(A) / det(A)"
        )
        painter.drawText(
            int(w * 0.73), int(h * 0.84),
            "u · v = ||u|| ||v|| cos θ"
        )
        painter.drawText(
            int(w * 0.78), int(h * 0.90),
            "u × v = det([i, j, k])"
        )

        painter.end()


class MatrixBelugaAvatar(QWidget):
    """Ilustración de la mascota de BelugaCalc."""

    def __init__(self, ruta_imagen, parent=None):
        super().__init__(parent)

        self.setFixedSize(280, 160)
        self.pixmap = QPixmap(ruta_imagen)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing, True
        )
        painter.setRenderHint(
            QPainter.RenderHint.SmoothPixmapTransform,
            True
        )

        w = self.width()
        h = self.height()

        card_w = 160
        card_h = 135

        card_x = (w - card_w) // 2
        card_y = (h - card_h) // 2

        gradiente = QLinearGradient(
            card_x, card_y,
            card_x + card_w,
            card_y + card_h
        )
        gradiente.setColorAt(
            0.0, QColor("#E0F2FE")
        )
        gradiente.setColorAt(
            1.0, QColor("#BAE6FD")
        )

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(gradiente))
        painter.drawRoundedRect(
            card_x, card_y,
            card_w, card_h,
            20, 20
        )

        if not self.pixmap.isNull():
            imagen = self.pixmap.scaled(
                125, 125,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            x = (w - imagen.width()) // 2
            y = (h - imagen.height()) // 2

            painter.drawPixmap(x, y, imagen)

        lapiz = QPen(
            QColor("#0284C7"),
            5.5,
            Qt.PenStyle.SolidLine,
            Qt.PenCapStyle.RoundCap
        )
        lapiz.setJoinStyle(
            Qt.PenJoinStyle.RoundJoin
        )
        painter.setPen(lapiz)

        margen = 8
        radio = 10
        longitud = 16

        arriba = card_y - 4
        abajo = card_y + card_h + 4
        izquierda = card_x - margen
        derecha = card_x + card_w + margen

        path_izquierdo = QPainterPath()
        path_izquierdo.moveTo(
            izquierda + longitud, arriba
        )
        path_izquierdo.lineTo(
            izquierda + radio, arriba
        )
        path_izquierdo.quadTo(
            izquierda, arriba,
            izquierda, arriba + radio
        )
        path_izquierdo.lineTo(
            izquierda, abajo - radio
        )
        path_izquierdo.quadTo(
            izquierda, abajo,
            izquierda + radio, abajo
        )
        path_izquierdo.lineTo(
            izquierda + longitud, abajo
        )

        painter.drawPath(path_izquierdo)

        path_derecho = QPainterPath()
        path_derecho.moveTo(
            derecha - longitud, arriba
        )
        path_derecho.lineTo(
            derecha - radio, arriba
        )
        path_derecho.quadTo(
            derecha, arriba,
            derecha, arriba + radio
        )
        path_derecho.lineTo(
            derecha, abajo - radio
        )
        path_derecho.quadTo(
            derecha, abajo,
            derecha - radio, abajo
        )
        path_derecho.lineTo(
            derecha - longitud, abajo
        )

        painter.drawPath(path_derecho)
        painter.end()


class HomeWindow(QWidget):
    """Inicio de BelugaCalc con módulos unificados."""

    modulo_seleccionado = pyqtSignal(str)

    def __init__(self, ventana_principal=None):
        super().__init__(ventana_principal)

        self.ventana_principal = ventana_principal
        self.init_ui()

    def init_ui(self):
        self.stack = QStackedWidget(self)

        principal = QVBoxLayout(self)
        principal.setContentsMargins(0, 0, 0, 0)
        principal.addWidget(self.stack)

        self.stack.addWidget(
            self._crear_pantalla_bienvenida()
        )
        self.stack.addWidget(
            self._crear_pantalla_eleccion()
        )

    def _crear_pantalla_bienvenida(self):
        contenedor = BackgroundWaves()

        layout = QVBoxLayout(contenedor)
        layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        tarjeta = QWidget()
        tarjeta.setFixedSize(480, 530)
        tarjeta.setStyleSheet("""
            QWidget {
                background:#FFFFFF;
                border-radius:32px;
                border:1px solid #E2E8F0;
            }
        """)

        sombra = QGraphicsDropShadowEffect(tarjeta)
        sombra.setBlurRadius(45)
        sombra.setColor(
            QColor(0, 30, 80, 20)
        )
        sombra.setYOffset(10)
        tarjeta.setGraphicsEffect(sombra)

        contenido = QVBoxLayout(tarjeta)
        contenido.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        contenido.setContentsMargins(
            36, 32, 36, 36
        )
        contenido.setSpacing(8)

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )
        ruta_imagen = os.path.join(
            base_dir, "assets", "BelugaK1.png"
        )

        avatar = MatrixBelugaAvatar(ruta_imagen)

        subtitulo = QLabel("ÁLGEBRA LINEAL")
        subtitulo.setStyleSheet("""
            color:#0284C7;
            font-size:12px;
            font-weight:800;
            letter-spacing:3px;
            background:transparent;
            border:none;
        """)

        titulo = QLabel("BelugaCalc")
        titulo.setStyleSheet("""
            color:#0F172A;
            font-size:30px;
            font-weight:900;
            font-family:'Trebuchet MS';
            background:transparent;
            border:none;
        """)

        descripcion = QLabel(
            "Matrices, determinantes y métodos numéricos"
        )
        descripcion.setStyleSheet("""
            color:#64748B;
            font-size:14px;
            background:transparent;
            border:none;
        """)

        btn_inicio = QPushButton("Comenzar")
        btn_inicio.setFixedSize(220, 48)
        btn_inicio.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        btn_inicio.setStyleSheet("""
            QPushButton {
                background:#0284C7;
                color:white;
                font-size:15px;
                font-weight:700;
                border:none;
                border-radius:24px;
            }
            QPushButton:hover {
                background:#0369A1;
            }
        """)

        btn_inicio.clicked.connect(
            lambda: self.stack.setCurrentIndex(1)
        )

        contenido.addWidget(
            subtitulo, 0,
            Qt.AlignmentFlag.AlignCenter
        )
        contenido.addWidget(
            avatar, 0,
            Qt.AlignmentFlag.AlignCenter
        )
        contenido.addWidget(
            titulo, 0,
            Qt.AlignmentFlag.AlignCenter
        )
        contenido.addWidget(
            descripcion, 0,
            Qt.AlignmentFlag.AlignCenter
        )
        contenido.addSpacing(18)
        contenido.addWidget(
            btn_inicio, 0,
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(tarjeta)
        return contenedor

    def _crear_pantalla_eleccion(self):
        contenedor = BackgroundWaves()

        layout = QVBoxLayout(contenedor)
        layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(
            QScrollArea.Shape.NoFrame
        )
        scroll.setStyleSheet("""
            QScrollArea {
                background:transparent;
                border:none;
            }
            QScrollBar:vertical {
                background:#E0F2FE;
                width:10px;
                border-radius:5px;
            }
            QScrollBar::handle:vertical {
                background:#93C5FD;
                border-radius:5px;
            }
        """)

        contenido_scroll = QWidget()
        contenido_scroll.setStyleSheet(
            "background:transparent;"
        )

        scroll_layout = QVBoxLayout(
            contenido_scroll
        )
        scroll_layout.setContentsMargins(
            25, 35, 25, 35
        )
        scroll_layout.setAlignment(
            Qt.AlignmentFlag.AlignHCenter
        )

        tarjeta = QWidget()
        tarjeta.setMinimumWidth(750)
        tarjeta.setMaximumWidth(1120)
        tarjeta.setStyleSheet("""
            QWidget#tarjetaPrincipal {
                background:#FFFFFF;
                border:1px solid #E2E8F0;
                border-radius:32px;
            }
        """)
        tarjeta.setObjectName("tarjetaPrincipal")

        tarjeta_layout = QVBoxLayout(tarjeta)
        tarjeta_layout.setContentsMargins(
            48, 38, 48, 48
        )
        tarjeta_layout.setSpacing(14)

        etiqueta = QLabel("EXPLORA BELUGACALC")
        etiqueta.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        etiqueta.setStyleSheet("""
            color:#0284C7;
            font-size:12px;
            font-weight:800;
            letter-spacing:2px;
            background:transparent;
        """)

        titulo = QLabel("Selecciona un módulo")
        titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        titulo.setStyleSheet("""
            color:#0F172A;
            font-size:27px;
            font-weight:900;
            background:transparent;
        """)

        descripcion = QLabel(
            "Elige la herramienta matemática que deseas utilizar."
        )
        descripcion.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        descripcion.setStyleSheet("""
            color:#64748B;
            font-size:14px;
            background:transparent;
        """)

        tarjeta_layout.addWidget(etiqueta)
        tarjeta_layout.addWidget(titulo)
        tarjeta_layout.addWidget(descripcion)
        tarjeta_layout.addSpacing(14)

        grid = QGridLayout()
        grid.setHorizontalSpacing(22)
        grid.setVerticalSpacing(22)

        # IMPORTANTE:
        # Newton-Raphson y Secante son UNA SOLA TARJETA.
        opciones = [
            {
                "titulo": "Básica",
                "tag": "[ A + B ]",
                "desc": "Suma, resta y multiplicación por escalar.",
                "clave": "basica"
            },
            {
                "titulo": "Determinantes",
                "tag": "[ det(A) ]",
                "desc": "Cálculo por cofactores y reducción gaussiana.",
                "clave": "determinantes"
            },
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
            },
            {
                "titulo": "Bisección",
                "tag": "[ a, b ]",
                "desc": "Aproximación de raíces mediante intervalos.",
                "clave": "biseccion"
            },
            {
                "titulo": "Regula Falsi",
                "tag": "[ f(x) ]",
                "desc": "Método de la regla falsa para encontrar raíces.",
                "clave": "regula_falsi"
            },
            {
                "titulo": "Newton-Raphson y Secante",
                "tag": "[ f′(x) | x₀, x₁ ]",
                "desc": (
                    "Métodos abiertos para encontrar raíces "
                    "con y sin derivadas."
                ),
                "clave": "metodos_abiertos"
            }
        ]

        for index, item in enumerate(opciones):
            boton = self._crear_tarjeta_modulo(item)

            fila = index // 2
            columna = index % 2

            grid.addWidget(
                boton, fila, columna
            )

        tarjeta_layout.addLayout(grid)

        scroll_layout.addWidget(tarjeta)
        scroll.setWidget(contenido_scroll)

        layout.addWidget(scroll)
        return contenedor

    def _crear_tarjeta_modulo(self, item):
        boton = QPushButton()
        boton.setFixedHeight(170)
        boton.setMinimumWidth(300)
        boton.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        boton.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        boton.setStyleSheet("""
            QPushButton {
                background:#F8FAFC;
                border:1.5px solid #E2E8F0;
                border-radius:18px;
                text-align:left;
            }
            QPushButton:hover {
                background:#FFFFFF;
                border-color:#0284C7;
            }
        """)

        contenido = QVBoxLayout(boton)
        contenido.setContentsMargins(
            18, 16, 18, 16
        )
        contenido.setSpacing(6)

        tag = QLabel(item["tag"])
        tag.setStyleSheet("""
            color:#0284C7;
            background:#E0F2FE;
            font-size:11px;
            font-weight:800;
            font-family:Consolas;
            padding:4px 8px;
            border-radius:6px;
            border:none;
        """)
        tag.setFixedHeight(25)

        titulo = QLabel(item["titulo"])
        titulo.setWordWrap(True)
        titulo.setStyleSheet("""
            color:#0F172A;
            font-size:17px;
            font-weight:800;
            background:transparent;
            border:none;
        """)

        descripcion = QLabel(item["desc"])
        descripcion.setWordWrap(True)
        descripcion.setStyleSheet("""
            color:#64748B;
            font-size:12px;
            background:transparent;
            border:none;
        """)

        accion = QLabel("Abrir módulo →")
        accion.setStyleSheet("""
            color:#0284C7;
            font-size:12px;
            font-weight:700;
            background:transparent;
            border:none;
        """)

        contenido.addWidget(
            tag, 0,
            Qt.AlignmentFlag.AlignLeft
        )
        contenido.addWidget(titulo)
        contenido.addWidget(descripcion)
        contenido.addStretch()
        contenido.addWidget(accion)

        clave = item["clave"]

        boton.clicked.connect(
            lambda _, c=clave: self.abrir_modulo(c)
        )

        return boton

    def abrir_modulo(self, clave):
        # La señal es suficiente para navegar.
        # Evitamos llamar dos veces a navegar_a().
        self.modulo_seleccionado.emit(clave)
