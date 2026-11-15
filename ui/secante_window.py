
"""Interfaz gráfica del Método de la Secante para BelugaCalc."""

import sys
import math
import numpy as np

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QDoubleSpinBox,
    QSpinBox,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QMessageBox,
    QHeaderView,
    QSplitter
)

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas
)
from matplotlib.figure import Figure

from core.biseccion import preparar_funcion
from core.secante import resolver_secante


class SecanteWindow(QWidget):
    """Ventana para resolver ecuaciones mediante Secante."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("BelugaCalc - Método de la Secante")
        self.setStyleSheet("background-color: #F4F8FB;")

        self._crear_interfaz()

    def _crear_interfaz(self):

        principal = QVBoxLayout(self)
        principal.setContentsMargins(20, 16, 20, 16)
        principal.setSpacing(10)

        # =====================================
        # TÍTULO
        # =====================================

        titulo = QLabel("Método de la Secante")
        titulo.setStyleSheet(
            "color: #031E36;"
            "font-size: 24px;"
            "font-weight: 900;"
        )
        principal.addWidget(titulo)

        subtitulo = QLabel(
            "Escribe f(x), dos valores iniciales X0 y X1, "
            "la tolerancia y el máximo de iteraciones."
        )
        subtitulo.setStyleSheet(
            "color: #64748B; font-size: 13px;"
        )
        principal.addWidget(subtitulo)

        # =====================================
        # CAMPOS DE ENTRADA
        # =====================================

        tarjeta = QFrame()
        tarjeta.setStyleSheet(
            "QFrame {"
            "background: white;"
            "border: 1px solid #C4D4E6;"
            "border-radius: 12px;"
            "}"
        )

        campos = QHBoxLayout(tarjeta)
        campos.setSpacing(8)

        self.txt_funcion = QLineEdit("x^3-x-2")
        self.txt_x0 = QLineEdit("1")
        self.txt_x1 = QLineEdit("2")

        self.spin_tolerancia = QDoubleSpinBox()
        self.spin_tolerancia.setDecimals(10)
        self.spin_tolerancia.setRange(0.0000000001, 1e6)
        self.spin_tolerancia.setValue(0.000001)
        self.spin_tolerancia.setSingleStep(0.000001)

        self.spin_n = QSpinBox()
        self.spin_n.setRange(1, 10000)
        self.spin_n.setValue(100)

        entradas = [
            ("f(x):", self.txt_funcion, 4),
            ("X0:", self.txt_x0, 1),
            ("X1:", self.txt_x1, 1),
            ("Tolerancia:", self.spin_tolerancia, 2),
            ("Iteraciones:", self.spin_n, 1)
        ]

        for nombre, widget, ancho in entradas:

            grupo = QVBoxLayout()

            etiqueta = QLabel(nombre)
            etiqueta.setStyleSheet(
                "color: #04335A;"
                "font-weight: 700;"
                "border: none;"
            )

            grupo.addWidget(etiqueta)

            widget.setMinimumHeight(34)
            widget.setStyleSheet(
                "background: #FAFCFE;"
                "color: #031E36;"
                "border: 1px solid #C4D4E6;"
                "border-radius: 7px;"
                "padding: 5px;"
            )

            grupo.addWidget(widget)
            campos.addLayout(grupo, ancho)

        principal.addWidget(tarjeta)

        # =====================================
        # BOTONES
        # =====================================

        acciones = QHBoxLayout()
        acciones.setSpacing(8)

        botones = [
            ("Graficar función", self.graficar),
            ("Calcular Secante", self.calcular),
            ("Limpiar", self.limpiar)
        ]

        for nombre, accion in botones:

            boton = QPushButton(nombre)
            boton.setCursor(
                Qt.CursorShape.PointingHandCursor
            )

            boton.setStyleSheet(
                "QPushButton {"
                "background: #04335A;"
                "color: white;"
                "font-weight: 700;"
                "border: none;"
                "border-radius: 9px;"
                "padding: 10px 14px;"
                "}"
                "QPushButton:hover {"
                "background: #4474A3;"
                "}"
                "QPushButton:pressed {"
                "background: #031E36;"
                "}"
            )

            boton.clicked.connect(accion)
            acciones.addWidget(boton)

        acciones.addStretch()
        principal.addLayout(acciones)

        # =====================================
        # ESTADO DEL CÁLCULO
        # =====================================

        self.lbl_estado = QLabel(
            "Lista para graficar o calcular."
        )

        self.lbl_estado.setStyleSheet(
            "background: #EAF5FC;"
            "color: #04335A;"
            "border: 1px solid #C4D4E6;"
            "border-radius: 8px;"
            "padding: 10px;"
            "font-weight: 700;"
        )

        principal.addWidget(self.lbl_estado)

        # =====================================
        # TABLA DE ITERACIONES
        # =====================================

        splitter = QSplitter(Qt.Orientation.Vertical)

        frame_tabla = QFrame()
        layout_tabla = QVBoxLayout(frame_tabla)

        etiqueta_tabla = QLabel("Tabla de iteraciones")
        etiqueta_tabla.setStyleSheet(
            "color: #031E36;"
            "font-weight: 700;"
            "font-size: 14px;"
        )

        layout_tabla.addWidget(etiqueta_tabla)

        self.tabla = QTableWidget(0, 9)

        self.tabla.setHorizontalHeaderLabels([
            "i",
            "X anterior",
            "X actual",
            "f(X anterior)",
            "f(X actual)",
            "X nuevo",
            "f(X nuevo)",
            "Cambio",
            "Residuo"
        ])

        self.tabla.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.tabla.setAlternatingRowColors(True)

        self.tabla.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.tabla.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.tabla.setStyleSheet(
            "QTableWidget {"
            "background: #FAFCFE;"
            "color: #031E36;"
            "gridline-color: #C4D4E6;"
            "alternate-background-color: #F0F6FC;"
            "}"
            "QHeaderView::section {"
            "background: #C4D4E6;"
            "color: #04335A;"
            "font-weight: 700;"
            "padding: 5px;"
            "border: 1px solid #B4C7DB;"
            "}"
        )

        layout_tabla.addWidget(self.tabla)

        splitter.addWidget(frame_tabla)

        # =====================================
        # BITÁCORA Y GRÁFICA
        # =====================================

        inferior = QSplitter(Qt.Orientation.Horizontal)

        # Bitácora
        frame_bitacora = QFrame()
        layout_bitacora = QVBoxLayout(frame_bitacora)

        etiqueta_bitacora = QLabel(
            "Procedimiento / Bitácora"
        )
        etiqueta_bitacora.setStyleSheet(
            "color: #031E36;"
            "font-weight: 700;"
        )

        layout_bitacora.addWidget(etiqueta_bitacora)

        self.bitacora = QTextEdit()
        self.bitacora.setReadOnly(True)

        self.bitacora.setStyleSheet(
            "background: white;"
            "color: #1E293B;"
            "font-family: Consolas;"
            "font-size: 12px;"
            "border: 1px solid #C4D4E6;"
            "border-radius: 8px;"
        )

        layout_bitacora.addWidget(self.bitacora)

        inferior.addWidget(frame_bitacora)

        # Gráfica
        frame_grafica = QFrame()
        layout_grafica = QVBoxLayout(frame_grafica)

        etiqueta_grafica = QLabel(
            "Gráfica de f(x) y aproximaciones"
        )
        etiqueta_grafica.setStyleSheet(
            "color: #031E36;"
            "font-weight: 700;"
        )

        layout_grafica.addWidget(etiqueta_grafica)

        self.figura = Figure(
            figsize=(5, 3),
            tight_layout=True
        )

        self.canvas = FigureCanvas(self.figura)
        self.ax = self.figura.add_subplot(111)

        layout_grafica.addWidget(self.canvas)

        inferior.addWidget(frame_grafica)
        inferior.setSizes([500, 500])

        splitter.addWidget(inferior)
        splitter.setSizes([260, 360])

        principal.addWidget(splitter, 1)

    # =====================================
    # DIBUJAR GRÁFICA
    # =====================================

    def _dibujar(self, filas=None):

        simbolica, f = preparar_funcion(
            self.txt_funcion.text().strip()
        )

        x0 = float(self.txt_x0.text())
        x1 = float(self.txt_x1.text())

        if not math.isfinite(x0) or not math.isfinite(x1):
            raise ValueError(
                "X0 y X1 deben ser valores finitos."
            )

        valores = [x0, x1]

        if filas:
            valores.extend(
                fila["x_nuevo"] for fila in filas
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
            500
        )

        ys = []

        for x in xs:
            try:
                y = float(f(float(x)))

                if math.isfinite(y):
                    ys.append(y)
                else:
                    ys.append(np.nan)

            except (
                ValueError,
                ZeroDivisionError,
                OverflowError,
                TypeError
            ):
                ys.append(np.nan)

        ys = np.array(ys, dtype=float)

        self.ax.clear()

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

        # Valores iniciales
        for indice, valor in enumerate([x0, x1]):

            try:
                y = float(f(valor))

                if math.isfinite(y):
                    self.ax.scatter(
                        valor,
                        y,
                        color="#16A34A",
                        s=45,
                        zorder=5,
                        label=f"X{indice}"
                    )

            except (
                ValueError,
                ZeroDivisionError,
                OverflowError,
                TypeError
            ):
                pass

        # Aproximaciones calculadas
        if filas:

            puntos_x = [
                fila["x_nuevo"] for fila in filas
            ]

            puntos_y = [
                fila["fx_nuevo"] for fila in filas
            ]

            self.ax.scatter(
                puntos_x,
                puntos_y,
                color="#E68A25",
                s=32,
                zorder=6,
                label="Aproximaciones"
            )

        # Ajustar escala vertical
        finitos = ys[np.isfinite(ys)]

        if finitos.size > 0:

            inferior_y = np.percentile(finitos, 5)
            superior_y = np.percentile(finitos, 95)

            if inferior_y < superior_y:
                self.ax.set_ylim(
                    inferior_y - 1,
                    superior_y + 1
                )

        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")

        self.ax.set_title(
            "Método de la Secante",
            fontsize=11
        )

        self.ax.grid(True, alpha=0.25)
        self.ax.legend()

        self.canvas.draw()

    # =====================================
    # BOTÓN GRAFICAR
    # =====================================

    def graficar(self):

        try:
            self._dibujar()

            self.lbl_estado.setText(
                "Función graficada correctamente. "
                "Puedes calcular el método de la Secante."
            )

        except Exception as exc:

            QMessageBox.warning(
                self,
                "Error al graficar",
                str(exc)
            )

    # =====================================
    # BOTÓN CALCULAR
    # =====================================

    def calcular(self):

        try:

            (
                funcion,
                filas,
                raiz,
                residuo,
                resumen
            ) = resolver_secante(
                self.txt_funcion.text().strip(),
                self.txt_x0.text().strip(),
                self.txt_x1.text().strip(),
                self.spin_tolerancia.value(),
                self.spin_n.value()
            )

            # Limpiar tabla anterior
            self.tabla.setRowCount(len(filas))

            claves = [
                "it",
                "x_anterior",
                "x_actual",
                "fx_anterior",
                "fx_actual",
                "x_nuevo",
                "fx_nuevo",
                "cambio",
                "residuo"
            ]

            for i, fila in enumerate(filas):

                for j, clave in enumerate(claves):

                    valor = fila[clave]

                    if clave == "it":
                        texto = str(valor)
                    else:
                        texto = f"{valor:.10g}"

                    elemento = QTableWidgetItem(texto)

                    elemento.setTextAlignment(
                        Qt.AlignmentFlag.AlignCenter
                    )

                    self.tabla.setItem(
                        i,
                        j,
                        elemento
                    )

            # Mostrar resumen
            self.bitacora.setPlainText(resumen)

            # Mostrar resultado
            self.lbl_estado.setText(
                f"Raíz aproximada: {raiz:.10f} "
                f"| Residuo: {residuo:.3g}"
            )

            # Dibujar gráfica
            self._dibujar(filas)

        except Exception as exc:

            QMessageBox.warning(
                self,
                "No se pudo calcular",
                str(exc)
            )

    # =====================================
    # BOTÓN LIMPIAR
    # =====================================

    def limpiar(self):

        self.txt_funcion.clear()
        self.txt_x0.clear()
        self.txt_x1.clear()

        self.spin_tolerancia.setValue(0.000001)
        self.spin_n.setValue(100)

        self.tabla.setRowCount(0)
        self.bitacora.clear()

        self.ax.clear()
        self.canvas.draw()

        self.lbl_estado.setText(
            "Lista para graficar o calcular."
        )


# =====================================
# EJECUCIÓN INDEPENDIENTE
# =====================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    ventana = SecanteWindow()
    ventana.resize(1200, 800)
    ventana.show()

    sys.exit(app.exec())
