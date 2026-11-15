import math
import re
import html
import numpy as np
import sympy as sp

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QDoubleSpinBox,
    QSpinBox, QFrame, QTableWidget, QTableWidgetItem,
    QTextEdit, QMessageBox, QHeaderView, QSplitter,
    QScrollArea
)

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas
)
from matplotlib.figure import Figure

from core.biseccion import preparar_funcion, verificar_continuidad
from core.regula_falsi import resolver_regula_falsi


# ==================================================
# CONVERSIÓN DE EXPRESIONES MATEMÁTICAS
# ==================================================

def normalizar_expresion(texto):
    """Convierte la escritura matemática a sintaxis de cálculo."""

    texto = texto.strip().lower()
    texto = re.sub(r"\s+", "", texto)

    if not texto:
        raise ValueError("Debes escribir una función.")

    texto = (
        texto.replace("−", "-")
        .replace("×", "*")
        .replace("·", "*")
        .replace("÷", "/")
        .replace("π", "pi")
        .replace("√", "sqrt")
        .replace("sen", "sin")
        .replace("ln(", "log(")
    )

    superindices = str.maketrans({
        "⁰": "0", "¹": "1", "²": "2",
        "³": "3", "⁴": "4", "⁵": "5",
        "⁶": "6", "⁷": "7", "⁸": "8",
        "⁹": "9"
    })

    texto = re.sub(
        r"[⁰¹²³⁴⁵⁶⁷⁸⁹]+",
        lambda m: "**" + m.group().translate(superindices),
        texto
    )

    texto = texto.replace("^", "**")

    # sen³(x) -> sin(x)**3
    patron = re.compile(
        r"(sin|cos|tan)\*\*(\d+)\("
    )

    while True:
        encontrado = patron.search(texto)

        if not encontrado:
            break

        inicio = encontrado.start()
        apertura = encontrado.end() - 1
        profundidad = 0
        cierre = None

        for i in range(apertura, len(texto)):
            if texto[i] == "(":
                profundidad += 1
            elif texto[i] == ")":
                profundidad -= 1
                if profundidad == 0:
                    cierre = i
                    break

        if cierre is None:
            raise ValueError("Falta cerrar un paréntesis.")

        funcion = encontrado.group(1)
        exponente = encontrado.group(2)
        argumento = texto[apertura + 1:cierre]

        reemplazo = (
            f"({funcion}({argumento})**{exponente})"
        )

        texto = (
            texto[:inicio]
            + reemplazo
            + texto[cierre + 1:]
        )

    # Multiplicación implícita con funciones
    funciones = "sin|cos|tan|sqrt|log|exp|abs"

    texto = re.sub(
        rf"(?<=[0-9x)])(?=(?:{funciones})\()",
        "*",
        texto
    )

    # 3x -> 3*x
    texto = re.sub(r"(?<=\d)(?=x)", "*", texto)

    # 2(x+1), x(x+1)
    texto = re.sub(
        r"(?<=[0-9x)])(?=\()",
        "*",
        texto
    )

    # (x+1)x, (x+1)2
    texto = re.sub(
        r"(?<=\))(?=[0-9x])",
        "*",
        texto
    )

    # 2pi, xpi
    texto = re.sub(
        r"(?<=[0-9x)])(?=pi)",
        "*",
        texto
    )

    return texto


def formato_matematico(simbolica):
    """Presentación legible de una función SymPy."""

    texto = sp.sstr(simbolica)

    texto = texto.replace("sin", "sen")

    for numero, simbolo in [
        ("9", "⁹"), ("8", "⁸"), ("7", "⁷"),
        ("6", "⁶"), ("5", "⁵"), ("4", "⁴"),
        ("3", "³"), ("2", "²")
    ]:
        texto = texto.replace("**" + numero, simbolo)

    # Solo ocultar multiplicación en presentación simple
    texto = re.sub(r"(?<=\d)\*(?=x)", "", texto)
    texto = re.sub(
        r"(?<=x)\*(?=sen|cos|tan)",
        "",
        texto
    )

    return texto


# ==================================================
# VENTANA PRINCIPAL
# ==================================================

class RegulaFalsiWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet(
            "background-color:#F4F8FB;"
        )

        self._funcion_graficada = None
        self._intervalo_verificado = None

        self._crear_interfaz()

    def _crear_interfaz(self):

        principal = QVBoxLayout(self)
        principal.setContentsMargins(18, 14, 18, 14)
        principal.setSpacing(9)

        titulo = QLabel(
            "Método Regula Falsi (Regla Falsa)"
        )
        titulo.setStyleSheet(
            "color:#031E36;"
            "font-size:24px;"
            "font-weight:900;"
        )
        principal.addWidget(titulo)

        subtitulo = QLabel(
            "Grafica la función, selecciona el intervalo "
            "[A, B] y calcula la raíz aproximada."
        )
        subtitulo.setStyleSheet("color:#64748B;")
        principal.addWidget(subtitulo)

        # ------------------------------------------
        # CAMPOS DE ENTRADA
        # ------------------------------------------

        tarjeta = QFrame()
        tarjeta.setStyleSheet(
            "QFrame {background:white;"
            "border:1px solid #C4D4E6;"
            "border-radius:12px;}"
        )

        fila = QHBoxLayout(tarjeta)
        fila.setContentsMargins(12, 9, 12, 9)
        fila.setSpacing(8)

        self.txt_funcion = QLineEdit()
        self.txt_funcion.setPlaceholderText(
            "Ejemplo: x³ − x − 2"
        )

        self.txt_a = QLineEdit()
        self.txt_a.setPlaceholderText("A")

        self.txt_b = QLineEdit()
        self.txt_b.setPlaceholderText("B")

        self.spin_n = QSpinBox()
        self.spin_n.setRange(1, 10000)
        self.spin_n.setValue(100)

        self.spin_ea = QDoubleSpinBox()
        self.spin_ea.setRange(0.00000001, 1000000)
        self.spin_ea.setDecimals(8)
        self.spin_ea.setValue(0.01)

        campos = [
            ("f(x):", self.txt_funcion, 4),
            ("A:", self.txt_a, 1),
            ("B:", self.txt_b, 1),
            ("n:", self.spin_n, 1),
            ("Ea (%):", self.spin_ea, 1)
        ]

        for nombre, widget, stretch in campos:

            grupo = QVBoxLayout()

            etiqueta = QLabel(nombre)
            etiqueta.setStyleSheet(
                "color:#04335A;font-weight:700;"
            )

            grupo.addWidget(etiqueta)

            widget.setMinimumHeight(34)
            widget.setStyleSheet(
                "background:#FAFCFE;"
                "color:#031E36;"
                "border:1px solid #C4D4E6;"
                "border-radius:7px;"
                "padding:5px;"
            )

            grupo.addWidget(widget)
            fila.addLayout(grupo, stretch)

        principal.addWidget(tarjeta)

        # ------------------------------------------
        # TECLADO MATEMÁTICO
        # ------------------------------------------

        self.btn_teclado = QPushButton(
            "Mostrar teclado matemático"
        )

        self.btn_teclado.setStyleSheet(
            "QPushButton {"
            "background:#E0F2FE;"
            "color:#04335A;"
            "border:1px solid #C4D4E6;"
            "border-radius:8px;"
            "padding:8px;"
            "font-weight:700;"
            "}"
        )

        principal.addWidget(self.btn_teclado)

        self.panel_teclado = QFrame()
        self.panel_teclado.setStyleSheet(
            "QFrame {background:white;"
            "border:1px solid #C4D4E6;"
            "border-radius:10px;}"
        )

        teclado = QGridLayout(self.panel_teclado)
        teclado.setSpacing(5)

        teclas = [
            ("7", "7"), ("8", "8"), ("9", "9"),
            ("÷", "÷"), ("x²", "²"), ("x³", "³"),

            ("4", "4"), ("5", "5"), ("6", "6"),
            ("×", "×"), ("sen", "sen("),
            ("cos", "cos("),

            ("1", "1"), ("2", "2"), ("3", "3"),
            ("−", "−"), ("tan", "tan("),
            ("√", "√("),

            ("0", "0"), (".", "."), ("x", "x"),
            ("+", "+"), ("(", "("), (")", ")"),

            ("π", "π"), ("^", "^"), ("ln", "ln("),
            ("⁴", "⁴"), ("⌫", "BORRAR"),
            ("C", "LIMPIAR")
        ]

        for i, (nombre, valor) in enumerate(teclas):

            boton = QPushButton(nombre)
            boton.setMinimumHeight(30)

            boton.setStyleSheet(
                "QPushButton {background:#F0F7FF;"
                "color:#04335A;"
                "border:1px solid #C4D4E6;"
                "border-radius:6px;"
                "font-weight:700;padding:5px;}"
                "QPushButton:hover {background:#BAE6FD;}"
            )

            boton.clicked.connect(
                lambda _, v=valor: self.insertar_tecla(v)
            )

            teclado.addWidget(
                boton,
                i // 6,
                i % 6
            )

        self.panel_teclado.hide()
        principal.addWidget(self.panel_teclado)

        self.btn_teclado.clicked.connect(
            self.alternar_teclado
        )

        # ------------------------------------------
        # BOTONES
        # ------------------------------------------

        acciones = QHBoxLayout()

        self.btn_graficar = QPushButton(
            "1. Graficar función"
        )
        self.btn_verificar = QPushButton(
            "2. Verificar A y B"
        )
        self.btn_calcular = QPushButton(
            "3. Calcular Regula Falsi"
        )
        self.btn_limpiar = QPushButton("Limpiar")

        for boton in (
            self.btn_graficar,
            self.btn_verificar,
            self.btn_calcular,
            self.btn_limpiar
        ):
            boton.setCursor(
                Qt.CursorShape.PointingHandCursor
            )
            boton.setStyleSheet(
                "QPushButton {background:#04335A;"
                "color:white;font-weight:700;"
                "border:0;border-radius:9px;"
                "padding:9px 13px;}"
                "QPushButton:hover {background:#4474A3;}"
            )
            acciones.addWidget(boton)

        self.btn_limpiar.setStyleSheet(
            "QPushButton {background:white;"
            "color:#4474A3;font-weight:700;"
            "border:1px solid #C4D4E6;"
            "border-radius:9px;padding:9px 13px;}"
        )

        acciones.addStretch()
        principal.addLayout(acciones)

        self.btn_graficar.clicked.connect(
            self.graficar_funcion
        )
        self.btn_verificar.clicked.connect(
            self.verificar_intervalo
        )
        self.btn_calcular.clicked.connect(
            self.calcular
        )
        self.btn_limpiar.clicked.connect(
            self.limpiar
        )

        # ------------------------------------------
        # ESTADO
        # ------------------------------------------

        self.lbl_estado = QLabel(
            "Paso 1: escribe la función y elige "
            "el rango de la gráfica."
        )
        self.lbl_estado.setWordWrap(True)
        principal.addWidget(self.lbl_estado)

        self._actualizar_estado(
            self.lbl_estado.text()
        )

        # ------------------------------------------
        # ÁREA DE RESULTADOS CON DESPLAZAMIENTO
        # ------------------------------------------

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(
            QFrame.Shape.NoFrame
        )

        contenido = QWidget()
        resultados = QVBoxLayout(contenido)
        resultados.setSpacing(12)

        # ------------------------------------------
        # TABLA DE ITERACIONES
        # ------------------------------------------

        frame_tabla = QFrame()
        frame_tabla.setStyleSheet(
            "QFrame {background:white;"
            "border:1px solid #C4D4E6;"
            "border-radius:11px;}"
        )

        lay_tabla = QVBoxLayout(frame_tabla)

        titulo_tabla = QLabel(
            "Tabla de iteraciones"
        )
        titulo_tabla.setStyleSheet(
            "color:#04335A;font-weight:800;"
        )

        lay_tabla.addWidget(titulo_tabla)

        self.tabla = QTableWidget(0, 8)
        self.tabla.setMinimumHeight(230)

        self.tabla.setHorizontalHeaderLabels([
            "i", "A", "B", "f(A)",
            "f(B)", "xr", "f(xr)", "Ea (%)"
        ])

        self.tabla.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.tabla.setAlternatingRowColors(True)

        self.tabla.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.tabla.setStyleSheet(
            "QTableWidget {background:#FAFCFE;"
            "color:#031E36;"
            "gridline-color:#E2E8F0;}"
            "QHeaderView::section {background:#C4D4E6;"
            "color:#04335A;font-weight:700;"
            "padding:5px;}"
        )

        lay_tabla.addWidget(self.tabla)
        resultados.addWidget(frame_tabla)

        # ------------------------------------------
        # BITÁCORA
        # ------------------------------------------

        frame_proc = QFrame()
        frame_proc.setStyleSheet(
            "QFrame {background:white;"
            "border:1px solid #C4D4E6;"
            "border-radius:11px;}"
        )

        lp = QVBoxLayout(frame_proc)

        lbl_proc = QLabel(
            "Procedimiento / Bitácora"
        )
        lbl_proc.setStyleSheet(
            "color:#04335A;font-weight:800;"
        )
        lp.addWidget(lbl_proc)

        self.bitacora = QTextEdit()
        self.bitacora.setReadOnly(True)
        self.bitacora.setMinimumHeight(250)

        self.bitacora.setStyleSheet(
            "QTextEdit {background:#FAFCFE;"
            "color:#1E293B;"
            "font-family:Consolas;"
            "font-size:10pt;"
            "border:1px solid #C4D4E6;"
            "border-radius:7px;}"
        )

        lp.addWidget(self.bitacora)
        resultados.addWidget(frame_proc)

        # ------------------------------------------
        # GRÁFICA GRANDE
        # ------------------------------------------

        frame_graf = QFrame()
        frame_graf.setStyleSheet(
            "QFrame {background:white;"
            "border:1px solid #C4D4E6;"
            "border-radius:11px;}"
        )

        lg = QVBoxLayout(frame_graf)

        lbl_graf = QLabel(
            "Gráfica de f(x) — inspección previa"
        )
        lbl_graf.setStyleSheet(
            "color:#04335A;font-weight:800;"
        )
        lg.addWidget(lbl_graf)

        rango = QHBoxLayout()

        rango.addWidget(
            QLabel("Vista X desde:")
        )

        self.spin_vista_min = QDoubleSpinBox()
        self.spin_vista_min.setRange(-1e9, 1e9)
        self.spin_vista_min.setDecimals(4)
        self.spin_vista_min.setValue(-5.0)

        rango.addWidget(self.spin_vista_min)

        rango.addWidget(QLabel("hasta:"))

        self.spin_vista_max = QDoubleSpinBox()
        self.spin_vista_max.setRange(-1e9, 1e9)
        self.spin_vista_max.setDecimals(4)
        self.spin_vista_max.setValue(5.0)

        rango.addWidget(self.spin_vista_max)
        rango.addStretch()

        lg.addLayout(rango)

        self.figura = Figure(
            figsize=(9, 5),
            facecolor="white"
        )

        self.canvas = FigureCanvas(
            self.figura
        )

        # Altura suficiente para evitar compresión
        self.canvas.setMinimumHeight(390)

        self.ax = self.figura.add_subplot(111)
        self.ax.grid(True, alpha=0.25)

        lg.addWidget(self.canvas)
        resultados.addWidget(frame_graf)

        scroll.setWidget(contenido)
        principal.addWidget(scroll, 1)

    # ==================================================
    # TECLADO
    # ==================================================

    def alternar_teclado(self):
        visible = not self.panel_teclado.isVisible()
        self.panel_teclado.setVisible(visible)

        self.btn_teclado.setText(
            "Ocultar teclado matemático"
            if visible
            else "Mostrar teclado matemático"
        )

    def insertar_tecla(self, valor):
        campo = self.txt_funcion
        campo.setFocus()

        if valor == "LIMPIAR":
            campo.clear()
            return

        if valor == "BORRAR":
            campo.backspace()
            return

        campo.insert(valor)

    # ==================================================
    # LECTURA Y VALIDACIÓN
    # ==================================================

    def _leer_funcion(self):
        expresion = normalizar_expresion(
            self.txt_funcion.text()
        )
        simbolica, f = preparar_funcion(expresion)
        return expresion, simbolica, f

    def _leer_intervalo(self):
        try:
            a = float(self.txt_a.text().strip())
            b = float(self.txt_b.text().strip())
        except ValueError as exc:
            raise ValueError(
                "A y B deben ser números válidos."
            ) from exc

        if not math.isfinite(a) or not math.isfinite(b):
            raise ValueError(
                "A y B deben ser finitos."
            )

        if a >= b:
            raise ValueError(
                "A debe ser menor que B."
            )

        return a, b

    def _leer_rango(self):
        minimo = self.spin_vista_min.value()
        maximo = self.spin_vista_max.value()

        if minimo >= maximo:
            raise ValueError(
                "El rango de X no es válido."
            )

        return minimo, maximo

    def _actualizar_estado(self, mensaje, valido=None):
        if valido is True:
            fondo, borde, color = (
                "#EAF7EE", "#86C99A", "#176534"
            )
        elif valido is False:
            fondo, borde, color = (
                "#FDECEC", "#E7A0A0", "#9B2525"
            )
        else:
            fondo, borde, color = (
                "#EAF5FC", "#C4D4E6", "#04335A"
            )

        self.lbl_estado.setStyleSheet(
            f"background:{fondo};"
            f"border:1px solid {borde};"
            f"color:{color};"
            "border-radius:8px;"
            "padding:9px;font-weight:700;"
        )

        self.lbl_estado.setText(mensaje)

    # ==================================================
    # GRAFICAR
    # ==================================================

    def graficar_funcion(self):
        try:
            expresion, simbolica, _ = self._leer_funcion()
            x_min, x_max = self._leer_rango()

            self._dibujar_grafica(
                simbolica, x_min, x_max
            )

            self._funcion_graficada = expresion
            self._intervalo_verificado = None

            self.tabla.setRowCount(0)
            self.bitacora.clear()

            self._actualizar_estado(
                "Gráfica lista. Observa la función "
                "y selecciona A y B."
            )

        except Exception as exc:
            QMessageBox.warning(
                self, "No se pudo graficar", str(exc)
            )

    # ==================================================
    # VERIFICAR INTERVALO
    # ==================================================

    def verificar_intervalo(self):
        self._intervalo_verificado = None

        try:
            expresion, simbolica, f = self._leer_funcion()

            if expresion != self._funcion_graficada:
                raise ValueError(
                    "Primero grafica la función."
                )

            a, b = self._leer_intervalo()

            verificar_continuidad(simbolica, a, b)

            fa, fb = f(a), f(b)

            if not all(
                math.isfinite(v) for v in (fa, fb)
            ):
                raise ValueError(
                    "La función no es finita en A o B."
                )

            if fa == 0 or fb == 0:
                valido = True
                mensaje = (
                    "RAÍZ EXACTA EN UN EXTREMO. "
                    f"f(A)={fa:.8g}, f(B)={fb:.8g}."
                )

            elif fa * fb < 0:
                valido = True
                mensaje = (
                    "INTERVALO VÁLIDO. "
                    f"f(A)={fa:.8g}, f(B)={fb:.8g}. "
                    "Existe cambio de signo."
                )

            else:
                valido = False
                mensaje = (
                    "INTERVALO NO VÁLIDO. "
                    f"f(A)={fa:.8g}, f(B)={fb:.8g}. "
                    "No existe cambio de signo."
                )

            if valido:
                self._intervalo_verificado = (
                    expresion, a, b
                )

            self._actualizar_estado(mensaje, valido)

            x_min, x_max = self._leer_rango()

            self._dibujar_grafica(
                simbolica,
                x_min,
                x_max,
                intervalo_inicial=(a, b)
            )

        except Exception as exc:
            self._actualizar_estado(
                f"No se pudo verificar: {exc}",
                False
            )

    # ==================================================
    # CALCULAR
    # ==================================================

    def calcular(self):
        try:
            expresion, _, _ = self._leer_funcion()

            if expresion != self._funcion_graficada:
                raise ValueError(
                    "Primero grafica la función."
                )

            a, b = self._leer_intervalo()

            if self._intervalo_verificado != (
                expresion, a, b
            ):
                raise ValueError(
                    "Primero verifica A y B."
                )

            (
                simbolica,
                filas,
                raiz,
                error,
                resumen,
                intervalo_inicial,
                intervalo_final
            ) = resolver_regula_falsi(
                expresion,
                a,
                b,
                self.spin_ea.value(),
                self.spin_n.value()
            )

            self._mostrar_tabla(filas)

            self._mostrar_bitacora(
                simbolica,
                filas,
                raiz,
                error,
                resumen,
                intervalo_inicial,
                intervalo_final
            )

            x_min, x_max = self._leer_rango()

            self._dibujar_grafica(
                simbolica,
                x_min,
                x_max,
                intervalo_inicial,
                intervalo_final,
                raiz
            )

            error_texto = (
                "No aplica"
                if error is None
                else f"{error:.8g}%"
            )

            self._actualizar_estado(
                f"Raíz aproximada: {raiz:.10g} "
                f"| Ea = {error_texto} "
                f"| Iteraciones: {len(filas)}",
                True
            )

        except Exception as exc:
            QMessageBox.warning(
                self, "Error de cálculo", str(exc)
            )

    # ==================================================
    # TABLA
    # ==================================================

    def _mostrar_tabla(self, filas):
        self.tabla.setRowCount(len(filas))

        for i, fila in enumerate(filas):
            error = (
                "—" if fila["error"] is None
                else f'{fila["error"]:.8g}'
            )

            valores = [
                str(fila["it"]),
                f'{fila["a"]:.8g}',
                f'{fila["b"]:.8g}',
                f'{fila["fa"]:.8g}',
                f'{fila["fb"]:.8g}',
                f'{fila["xr"]:.8g}',
                f'{fila["fxr"]:.8g}',
                error
            ]

            for j, valor in enumerate(valores):
                item = QTableWidgetItem(valor)
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )
                self.tabla.setItem(i, j, item)

    # ==================================================
    # BITÁCORA
    # ==================================================

    def _mostrar_bitacora(
        self, simbolica, filas, raiz, error,
        resumen, intervalo_inicial, intervalo_final
    ):
        funcion = html.escape(
            formato_matematico(simbolica)
        )

        partes = [
            "<h3 style='color:#04335A'>"
            "MÉTODO REGULA FALSI</h3>",
            f"<p><b>Función:</b> f(x) = {funcion}</p>",
            "<p><b>Fórmula:</b><br>"
            "xr = B − [f(B) × (A − B)] "
            "/ [f(A) − f(B)]</p>",
            "<p><b>Error aproximado:</b><br>"
            "Ea = |(xr actual − xr anterior) "
            "/ xr actual| × 100%</p>",
            f"<p><b>Intervalo inicial:</b> "
            f"[{intervalo_inicial[0]:.10g}, "
            f"{intervalo_inicial[1]:.10g}]</p><hr>"
        ]

        for fila in filas:
            error_texto = (
                "No aplica en la primera iteración"
                if fila["error"] is None
                else f'{fila["error"]:.10g}%'
            )

            actualizacion = html.escape(
                fila.get(
                    "actualizacion",
                    "Sin actualización."
                )
            )

            partes.append(
                f"<h4>Iteración {fila['it']}</h4>"
                f"A = {fila['a']:.10g}<br>"
                f"B = {fila['b']:.10g}<br>"
                f"f(A) = {fila['fa']:.10g}<br>"
                f"f(B) = {fila['fb']:.10g}<br><br>"
                "<b>Sustitución:</b><br>"
                f"xr = {fila['b']:.10g} − "
                f"[{fila['fb']:.10g} × "
                f"({fila['a']:.10g} − "
                f"{fila['b']:.10g})] / "
                f"[{fila['fa']:.10g} − "
                f"({fila['fb']:.10g})]<br>"
                f"<b>xr = {fila['xr']:.10g}</b><br>"
                f"f(xr) = {fila['fxr']:.10g}<br>"
                f"Ea = {error_texto}<br>"
                f"Residuo = {fila['residuo']:.10g}<br>"
                f"<b>Actualización:</b> "
                f"{actualizacion}<hr>"
            )

        partes.append(
            "<h3 style='color:#0284C7'>"
            "RESULTADO FINAL</h3>"
            f"<p><b>Raíz:</b> {raiz:.10g}<br>"
            f"<b>Intervalo final:</b> "
            f"[{intervalo_final[0]:.10g}, "
            f"{intervalo_final[1]:.10g}]</p>"
            f"<p>{html.escape(resumen)}</p>"
        )

        self.bitacora.setHtml("".join(partes))

    # ==================================================
    # GRÁFICA MEJORADA
    # ==================================================

    def _dibujar_grafica(
        self, simbolica, x_min, x_max,
        intervalo_inicial=None,
        intervalo_final=None,
        raiz=None
    ):
        if x_min >= x_max:
            raise ValueError(
                "El mínimo de X debe ser menor al máximo."
            )

        funcion = sp.lambdify(
            sp.Symbol("x"),
            simbolica,
            modules=["numpy"]
        )

        xs = np.linspace(x_min, x_max, 1200)

        with np.errstate(all="ignore"):
            ys = np.asarray(
                funcion(xs),
                dtype=float
            )

        if ys.ndim == 0:
            ys = np.full_like(xs, float(ys))

        ys = np.broadcast_to(ys, xs.shape)
        ys = np.where(np.isfinite(ys), ys, np.nan)

        self.ax.clear()

        self.ax.plot(
            xs,
            ys,
            color="#2563EB",
            linewidth=2.3,
            label="f(x)"
        )

        self.ax.axhline(
            0,
            color="#64748B",
            linewidth=1
        )

        self.ax.axvline(
            0,
            color="#94A3B8",
            linewidth=0.8
        )

        if intervalo_inicial:
            a, b = intervalo_inicial

            self.ax.axvspan(
                a, b,
                color="#F59E0B",
                alpha=0.12,
                label="Intervalo inicial"
            )

            self.ax.axvline(
                a,
                color="#16A34A",
                linestyle="--",
                linewidth=1.4,
                label=f"A = {a:.6g}"
            )

            self.ax.axvline(
                b,
                color="#DC2626",
                linestyle="--",
                linewidth=1.4,
                label=f"B = {b:.6g}"
            )

        if intervalo_final:
            af, bf = intervalo_final

            self.ax.axvspan(
                af, bf,
                color="#2563EB",
                alpha=0.25,
                label="Intervalo final"
            )

        if raiz is not None:
            self.ax.axvline(
                raiz,
                color="#7C3AED",
                linestyle="-.",
                linewidth=1.5,
                label=f"xr ≈ {raiz:.8g}"
            )

            self.ax.scatter(
                [raiz],
                [0],
                color="#7C3AED",
                edgecolors="white",
                s=55,
                zorder=6
            )

        # Respetar exactamente el rango elegido
        self.ax.set_xlim(x_min, x_max)

        self.ax.set_xlabel("x", fontsize=10)
        self.ax.set_ylabel("f(x)", fontsize=10)

        self.ax.set_title(
            "Gráfica de Regula Falsi",
            fontsize=13,
            fontweight="bold",
            color="#04335A",
            pad=15
        )

        self.ax.grid(True, alpha=0.25)

        # La leyenda queda debajo de la gráfica.
        # Así no tapa la curva ni el título.
        self.ax.legend(
            loc="upper center",
            bbox_to_anchor=(0.5, -0.17),
            ncol=3,
            fontsize=8,
            frameon=False
        )

        # Reservar espacio para título y leyenda.
        self.figura.subplots_adjust(
            left=0.09,
            right=0.97,
            top=0.88,
            bottom=0.29
        )

        self.canvas.draw_idle()

    # ==================================================
    # LIMPIAR
    # ==================================================

    def limpiar(self):
        self.txt_funcion.clear()
        self.txt_a.clear()
        self.txt_b.clear()

        self.spin_n.setValue(100)
        self.spin_ea.setValue(0.01)

        self.spin_vista_min.setValue(-5.0)
        self.spin_vista_max.setValue(5.0)

        self.tabla.setRowCount(0)
        self.bitacora.clear()

        self._funcion_graficada = None
        self._intervalo_verificado = None

        self.ax.clear()
        self.ax.grid(True, alpha=0.25)
        self.canvas.draw_idle()

        self._actualizar_estado(
            "Paso 1: escribe la función y "
            "elige el rango de la gráfica."
        )
