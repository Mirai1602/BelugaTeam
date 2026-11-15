"""Interfaz compartida para Newton-Raphson y Secante."""

import math
import numpy as np

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QDoubleSpinBox,
    QSpinBox, QFrame, QTableWidget,
    QTableWidgetItem, QTextEdit, QMessageBox,
    QHeaderView, QSplitter, QScrollArea,
    QSizePolicy
)

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas
)
from matplotlib.figure import Figure

from core.biseccion import preparar_funcion


class BaseMetodoWindow(QWidget):

    def __init__(self, metodo, parent=None):
        super().__init__(parent)

        if metodo not in ("newton", "secante"):
            raise ValueError("Método desconocido.")

        self.metodo = metodo
        self.es_secante = metodo == "secante"

        self.nombre = (
            "Secante" if self.es_secante
            else "Newton-Raphson"
        )

        self.setStyleSheet("background-color:#F4F8FB;")
        self._crear_interfaz()

    def _crear_interfaz(self):
        exterior = QVBoxLayout(self)
        exterior.setContentsMargins(0, 0, 0, 0)

        # Permite desplazarse cuando la ventana es pequeña.
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet(
            "QScrollArea{border:none;background:#F4F8FB;}"
        )

        contenido = QWidget()
        principal = QVBoxLayout(contenido)
        principal.setContentsMargins(12, 12, 12, 16)
        principal.setSpacing(10)

        titulo = QLabel(f"Método de {self.nombre}")
        titulo.setStyleSheet(
            "color:#031E36;font-size:22px;font-weight:800;"
        )
        principal.addWidget(titulo)

        descripcion = QLabel(
            "Escribe f(x), dos valores iniciales X0 y X1, "
            "la tolerancia y las iteraciones."
            if self.es_secante else
            "Escribe f(x), el valor inicial X0 y la tolerancia. "
            "La derivada se calcula automáticamente."
        )
        descripcion.setWordWrap(True)
        descripcion.setStyleSheet("color:#64748B;")
        principal.addWidget(descripcion)

        # ---------------- ENTRADAS ----------------

        tarjeta = QFrame()
        tarjeta.setObjectName("tarjetaEntradas")
        tarjeta.setStyleSheet("""
            QFrame#tarjetaEntradas {
                background:white;
                border:1px solid #C4D4E6;
                border-radius:12px;
            }
        """)

        campos = QHBoxLayout(tarjeta)
        campos.setContentsMargins(12, 12, 12, 12)
        campos.setSpacing(9)

        self.txt_funcion = QLineEdit("x^3-x-2")
        self.txt_x0 = QLineEdit(
            "1" if self.es_secante else "1.5"
        )

        self.txt_x1 = QLineEdit("2")

        self.spin_tolerancia = QDoubleSpinBox()
        self.spin_tolerancia.setDecimals(10)
        self.spin_tolerancia.setRange(1e-10, 1e6)
        self.spin_tolerancia.setValue(0.000001)
        self.spin_tolerancia.setSingleStep(0.000001)

        self.spin_n = QSpinBox()
        self.spin_n.setRange(1, 10000)
        self.spin_n.setValue(100)

        entradas = [
            ("f(x):", self.txt_funcion, 4),
            ("X0:", self.txt_x0, 1),
        ]

        if self.es_secante:
            entradas.append(("X1:", self.txt_x1, 1))

        entradas.extend([
            ("Tolerancia:", self.spin_tolerancia, 2),
            ("Iteraciones:", self.spin_n, 1),
        ])

        for nombre, widget, ancho in entradas:
            grupo = QVBoxLayout()
            grupo.setSpacing(5)

            etiqueta = QLabel(nombre)
            etiqueta.setStyleSheet(
                "color:#04335A;font-weight:700;"
            )

            widget.setMinimumHeight(38)
            widget.setStyleSheet("""
                background:#FAFCFE;
                color:#031E36;
                border:1px solid #C4D4E6;
                border-radius:7px;
                padding:5px;
            """)

            grupo.addWidget(etiqueta)
            grupo.addWidget(widget)
            campos.addLayout(grupo, ancho)

        principal.addWidget(tarjeta)

        # ---------------- BOTONES ----------------

        acciones = QHBoxLayout()
        acciones.setSpacing(9)

        botones = [
            ("Graficar función", self.graficar),
            (f"Calcular {self.nombre}", self.calcular),
            ("Limpiar", self.limpiar),
        ]

        for nombre, accion in botones:
            boton = QPushButton(nombre)
            boton.setMinimumHeight(42)
            boton.setCursor(
                Qt.CursorShape.PointingHandCursor
            )
            boton.setStyleSheet("""
                QPushButton {
                    background:#04335A;
                    color:white;
                    font-weight:700;
                    border:none;
                    border-radius:9px;
                    padding:9px 15px;
                }
                QPushButton:hover {
                    background:#4474A3;
                }
            """)
            boton.clicked.connect(accion)
            acciones.addWidget(boton)

        acciones.addStretch()
        principal.addLayout(acciones)

        # ---------------- RESULTADO ----------------

        self.lbl_estado = QLabel(
            "Lista para graficar o calcular."
        )
        self.lbl_estado.setWordWrap(True)
        self.lbl_estado.setMinimumHeight(43)
        self.lbl_estado.setStyleSheet("""
            background:#EAF5FC;
            color:#04335A;
            border:1px solid #C4D4E6;
            border-radius:8px;
            padding:9px;
            font-weight:700;
        """)
        principal.addWidget(self.lbl_estado)

        # ---------------- PANELES ----------------

        self.splitter = QSplitter(
            Qt.Orientation.Vertical
        )
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setHandleWidth(8)

        # Tabla
        frame_tabla = QFrame()
        tabla_layout = QVBoxLayout(frame_tabla)
        tabla_layout.setContentsMargins(4, 4, 4, 4)

        lbl_tabla = QLabel("Tabla de iteraciones")
        lbl_tabla.setStyleSheet(
            "color:#031E36;font-weight:700;"
        )
        tabla_layout.addWidget(lbl_tabla)

        columnas = (
            [
                "i", "X anterior", "X actual",
                "f(X anterior)", "f(X actual)",
                "X nuevo", "f(X nuevo)",
                "Cambio", "Residuo"
            ]
            if self.es_secante else
            [
                "i", "X anterior", "f(X)",
                "f'(X)", "X nuevo",
                "f(X nuevo)", "Cambio", "Residuo"
            ]
        )

        self.tabla = QTableWidget(0, len(columnas))
        self.tabla.setHorizontalHeaderLabels(columnas)

        self.tabla.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.tabla.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self.tabla.verticalHeader().setVisible(False)
        self.tabla.verticalHeader().setDefaultSectionSize(30)

        self.tabla.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.tabla.setMinimumHeight(220)
        self.tabla.setStyleSheet("""
            QTableWidget {
                background:#FAFCFE;
                color:#031E36;
                gridline-color:#C4D4E6;
                alternate-background-color:#F0F6FC;
                border:1px solid #C4D4E6;
                border-radius:7px;
            }
            QHeaderView::section {
                background:#C4D4E6;
                color:#04335A;
                font-weight:700;
                padding:6px;
                border:1px solid #B5C9DE;
            }
        """)

        tabla_layout.addWidget(self.tabla)
        self.splitter.addWidget(frame_tabla)

        # Panel inferior
        inferior = QSplitter(
            Qt.Orientation.Horizontal
        )
        inferior.setChildrenCollapsible(False)
        inferior.setHandleWidth(8)

        # Bitácora
        frame_bitacora = QFrame()
        bitacora_layout = QVBoxLayout(frame_bitacora)
        bitacora_layout.setContentsMargins(4, 4, 4, 4)

        lbl_bitacora = QLabel(
            "Procedimiento / Bitácora"
        )
        lbl_bitacora.setStyleSheet(
            "color:#031E36;font-weight:700;"
        )
        bitacora_layout.addWidget(lbl_bitacora)

        self.bitacora = QTextEdit()
        self.bitacora.setReadOnly(True)
        self.bitacora.setMinimumHeight(330)
        self.bitacora.setStyleSheet("""
            QTextEdit {
                background:white;
                color:#1E293B;
                font-family:Consolas;
                font-size:12px;
                border:1px solid #C4D4E6;
                border-radius:8px;
                padding:10px;
            }
        """)

        bitacora_layout.addWidget(self.bitacora)
        inferior.addWidget(frame_bitacora)

        # Gráfica
        frame_grafica = QFrame()
        grafica_layout = QVBoxLayout(frame_grafica)
        grafica_layout.setContentsMargins(4, 4, 4, 4)

        lbl_grafica = QLabel(
            "Gráfica de f(x) y aproximaciones"
        )
        lbl_grafica.setStyleSheet(
            "color:#031E36;font-weight:700;"
        )
        grafica_layout.addWidget(lbl_grafica)

        self.figura = Figure(
            figsize=(7, 4.5),
            dpi=100,
            facecolor="white"
        )

        self.canvas = FigureCanvas(self.figura)
        self.canvas.setMinimumHeight(330)
        self.canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        self.ax = self.figura.add_subplot(111)

        self.figura.subplots_adjust(
            left=0.13,
            right=0.97,
            top=0.88,
            bottom=0.24
        )

        grafica_layout.addWidget(self.canvas)
        inferior.addWidget(frame_grafica)

        inferior.setSizes([520, 650])

        self.splitter.addWidget(inferior)
        self.splitter.setSizes([280, 400])

        principal.addWidget(self.splitter)

        # Altura suficiente para los dos paneles.
        self.splitter.setMinimumHeight(650)

        scroll.setWidget(contenido)
        exterior.addWidget(scroll)

    # ---------------- GRÁFICA ----------------

    def _dibujar(self, filas=None):
        _, f = preparar_funcion(
            self.txt_funcion.text().strip()
        )

        x0 = float(self.txt_x0.text())
        valores = [x0]

        if self.es_secante:
            x1 = float(self.txt_x1.text())
            valores.append(x1)

        if filas:
            valores.extend(
                float(fila["x_nuevo"])
                for fila in filas
            )

        if not all(math.isfinite(x) for x in valores):
            raise ValueError(
                "Los valores iniciales y las aproximaciones "
                "deben ser finitos."
            )

        minimo = min(valores)
        maximo = max(valores)

        margen = max(
            1.5,
            (maximo - minimo) * 0.5
        )

        xs = np.linspace(
            minimo - margen,
            maximo + margen,
            1200
        )

        ys = []

        for x in xs:
            try:
                y = float(f(float(x)))
                ys.append(
                    y if math.isfinite(y) else np.nan
                )
            except (
                ValueError, TypeError,
                ZeroDivisionError, OverflowError
            ):
                ys.append(np.nan)

        ys = np.asarray(ys, dtype=float)

        self.ax.clear()

        # Detectar saltos grandes para no unir
        # visualmente ramas de una discontinuidad.
        finitos = ys[np.isfinite(ys)]

        if finitos.size:
            p5, p95 = np.percentile(
                finitos, [5, 95]
            )
            escala = max(p95 - p5, 1e-9)

            diferencias = np.abs(np.diff(ys))

            saltos = np.where(
                diferencias > 4 * escala
            )[0]

            for indice in saltos:
                ys[indice + 1] = np.nan

        self.ax.plot(
            xs,
            ys,
            color="#2563EB",
            linewidth=2,
            label="f(x)"
        )

        self.ax.axhline(
            0,
            color="#64748B",
            linewidth=1
        )

        # Puntos iniciales
        iniciales = [x0]

        if self.es_secante:
            iniciales.append(x1)

        for indice, valor in enumerate(iniciales):
            try:
                y = float(f(valor))

                if math.isfinite(y):
                    self.ax.scatter(
                        [valor],
                        [y],
                        s=45,
                        zorder=5,
                        color=(
                            "#16A34A"
                            if indice == 0
                            else "#9333EA"
                        ),
                        label=f"X{indice}"
                    )
            except (
                ValueError, TypeError,
                ZeroDivisionError, OverflowError
            ):
                pass

        # Aproximaciones
        if filas:
            puntos_x = []
            puntos_y = []

            for fila in filas:
                x = float(fila["x_nuevo"])
                y = float(fila["fx_nuevo"])

                if math.isfinite(x) and math.isfinite(y):
                    puntos_x.append(x)
                    puntos_y.append(y)

            if puntos_x:
                self.ax.scatter(
                    puntos_x,
                    puntos_y,
                    color="#E68A25",
                    s=35,
                    zorder=6,
                    label="Aproximaciones"
                )

        # Escala vertical sin valores extremos.
        finitos = ys[np.isfinite(ys)]

        if finitos.size:
            inferior = float(np.percentile(finitos, 5))
            superior = float(np.percentile(finitos, 95))

            if inferior < superior:
                margen_y = max(
                    (superior - inferior) * 0.12,
                    0.1
                )

                self.ax.set_ylim(
                    inferior - margen_y,
                    superior + margen_y
                )

        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.set_title(
            f"Método de {self.nombre}",
            fontsize=12,
            pad=12
        )

        self.ax.grid(True, alpha=0.25)

        # Leyenda dentro de la gráfica, sin recortes.
        self.ax.legend(
            loc="upper right",
            fontsize=9,
            framealpha=0.9
        )

        self.canvas.draw_idle()

    def graficar(self):
        try:
            self._dibujar()
            self.lbl_estado.setText(
                "Función graficada correctamente."
            )
        except Exception as exc:
            QMessageBox.warning(
                self,
                "Error al graficar",
                str(exc)
            )

    # ---------------- RESULTADOS ----------------

    def mostrar_resultados(
        self, filas, raiz, residuo, resumen
    ):
        claves = (
            [
                "it", "x_anterior", "x_actual",
                "fx_anterior", "fx_actual",
                "x_nuevo", "fx_nuevo",
                "cambio", "residuo"
            ]
            if self.es_secante else
            [
                "it", "x_anterior", "fx",
                "dfx", "x_nuevo", "fx_nuevo",
                "cambio", "residuo"
            ]
        )

        self.tabla.setRowCount(len(filas))

        for i, fila in enumerate(filas):
            for j, clave in enumerate(claves):
                valor = fila[clave]

                texto = (
                    str(valor)
                    if clave == "it"
                    else f"{valor:.10g}"
                )

                item = QTableWidgetItem(texto)
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )
                self.tabla.setItem(i, j, item)

        # Mostrar desde la primera iteración.
        if filas:
            self.tabla.scrollToTop()

        self.bitacora.setPlainText(resumen)
        self.bitacora.moveCursor(
            self.bitacora.textCursor().MoveOperation.Start
        )

        self.lbl_estado.setText(
            f"Raíz aproximada: {raiz:.10f} "
            f"| Residuo: {residuo:.3g}"
        )

        self._dibujar(filas)

    def limpiar(self):
        self.txt_funcion.clear()
        self.txt_x0.clear()

        if self.es_secante:
            self.txt_x1.clear()

        self.spin_tolerancia.setValue(0.000001)
        self.spin_n.setValue(100)

        self.tabla.setRowCount(0)
        self.bitacora.clear()

        self.ax.clear()
        self.canvas.draw_idle()

        self.lbl_estado.setText(
            "Lista para graficar o calcular."
        )

    def calcular(self):
        raise NotImplementedError(
            "Cada método debe implementar su cálculo."
        )