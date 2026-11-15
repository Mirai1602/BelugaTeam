import math
import numpy as np
import sympy as sp

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QDoubleSpinBox, QSpinBox, QFrame, QTableWidget, QTableWidgetItem,
    QTextEdit, QMessageBox, QHeaderView, QSplitter, QFormLayout
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from core.biseccion import preparar_funcion, resolver_biseccion, verificar_continuidad


class BiseccionWindow(QWidget):
    """Interfaz del método de bisección: graficar, elegir intervalo y resolver."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #F4F8FB;")
        self._funcion_graficada = None
        self._intervalo_verificado = None
        self._crear_interfaz()

    def _crear_interfaz(self):
        principal = QVBoxLayout(self)
        principal.setContentsMargins(20, 16, 20, 16)
        principal.setSpacing(10)

        titulo = QLabel("Método de Bisección")
        titulo.setStyleSheet("color:#031E36;font-size:24px;font-weight:900;")
        principal.addWidget(titulo)
        subtitulo = QLabel(
            "Primero grafica f(x), comprueba visualmente su continuidad y selecciona el intervalo [A, B]."
        )
        subtitulo.setWordWrap(True)
        subtitulo.setStyleSheet("color:#64748B;")
        principal.addWidget(subtitulo)

        tarjeta = QFrame()
        tarjeta.setStyleSheet("QFrame{background:white;border:1px solid #C4D4E6;border-radius:12px;}")
        fila = QHBoxLayout(tarjeta)
        fila.setContentsMargins(12, 10, 12, 10)
        fila.setSpacing(8)

        self.txt_funcion = QLineEdit("x^4 - 5*x^3 + 0.5*x^2 - 11*x + 10")
        self.txt_funcion.setPlaceholderText("Ejemplo: x^3 - 2*x - 5")
        self.spin_xi = QDoubleSpinBox()
        self.spin_xi.setRange(-1e9, 1e9)
        self.spin_xi.setDecimals(10)
        self.spin_xi.setValue(0.6)
        self.spin_xf = QDoubleSpinBox()
        self.spin_xf.setRange(-1e9, 1e9)
        self.spin_xf.setDecimals(10)
        self.spin_xf.setValue(1.0)
        self.spin_n = QSpinBox()
        self.spin_n.setRange(1, 10000)
        self.spin_n.setValue(500)
        self.spin_er = QDoubleSpinBox()
        self.spin_er.setRange(1e-12, 1e6)
        self.spin_er.setDecimals(10)
        self.spin_er.setValue(0.0001)
        self.spin_er.setToolTip("Error aproximado porcentual Ea. Ejemplo: 0.0001 significa 0.0001%.")

        campos = [
            ("f(x):", self.txt_funcion), ("A (xi):", self.spin_xi),
            ("B (xf):", self.spin_xf), ("n:", self.spin_n), ("Ea (%):", self.spin_er)
        ]
        for nombre, widget in campos:
            grupo = QVBoxLayout()
            lbl = QLabel(nombre)
            lbl.setStyleSheet("color:#04335A;font-weight:700;")
            grupo.addWidget(lbl)
            widget.setMinimumHeight(34)
            widget.setStyleSheet(
                "QLineEdit,QDoubleSpinBox,QSpinBox{background:#FAFCFE;color:#031E36;"
                "border:1px solid #C4D4E6;border-radius:7px;padding:5px;}"
            )
            grupo.addWidget(widget)
            fila.addLayout(grupo, 3 if widget is self.txt_funcion else 1)
        principal.addWidget(tarjeta)

        acciones = QHBoxLayout()
        self.btn_graficar = QPushButton("1. Graficar función")
        self.btn_verificar = QPushButton("2. Verificar intervalo")
        self.btn_calcular = QPushButton("Calcular Bisección")
        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_graficar.setStyleSheet(
            "QPushButton{background:#2875A8;color:white;font-weight:700;border:0;"
            "border-radius:9px;padding:10px 16px;}QPushButton:hover{background:#3B8BC0;}"
        )
        self.btn_calcular.setStyleSheet(
            "QPushButton{background:#04335A;color:white;font-weight:700;border:0;"
            "border-radius:9px;padding:10px 16px;}QPushButton:hover{background:#4474A3;}"
        )
        self.btn_limpiar.setStyleSheet(
            "QPushButton{background:white;color:#4474A3;font-weight:700;border:1px solid #C4D4E6;"
            "border-radius:9px;padding:10px 16px;}"
        )
        self.btn_graficar.clicked.connect(self.graficar_funcion)
        self.btn_verificar.clicked.connect(self.verificar_intervalo)
        self.btn_calcular.clicked.connect(self.calcular)
        self.btn_limpiar.clicked.connect(self.limpiar)
        acciones.addWidget(self.btn_graficar)
        acciones.addWidget(self.btn_verificar)
        acciones.addWidget(self.btn_calcular)
        acciones.addWidget(self.btn_limpiar)
        acciones.addStretch()
        principal.addLayout(acciones)

        self.lbl_resultado = QLabel("Paso 1: ingresa la función y presiona 'Graficar función'.")
        self.lbl_resultado.setWordWrap(True)
        self.lbl_resultado.setStyleSheet(
            "background:#EAF5FC;color:#04335A;border:1px solid #C4D4E6;"
            "border-radius:8px;padding:9px;font-weight:700;"
        )
        principal.addWidget(self.lbl_resultado)

        splitter = QSplitter(Qt.Orientation.Vertical)
        frame_tabla = QFrame()
        frame_tabla.setStyleSheet("QFrame{background:white;border:1px solid #C4D4E6;border-radius:11px;}")
        lay_tabla = QVBoxLayout(frame_tabla)
        lay_tabla.addWidget(QLabel("Tabla de iteraciones"))
        self.tabla = QTableWidget(0, 9)
        self.tabla.setHorizontalHeaderLabels(
            ["i", "A", "B", "C", "f(A)", "f(B)", "f(C)", "Ea (%)", "|f(C)|"]
        )
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setStyleSheet(
            "QTableWidget{background:#FAFCFE;color:#031E36;gridline-color:#E2E8F0;border:0;}"
            "QHeaderView::section{background:#C4D4E6;color:#04335A;font-weight:700;padding:5px;border:0;}"
        )
        lay_tabla.addWidget(self.tabla)

        inferior = QSplitter(Qt.Orientation.Horizontal)
        frame_proc = QFrame()
        frame_proc.setStyleSheet("QFrame{background:white;border:1px solid #C4D4E6;border-radius:11px;}")
        lp = QVBoxLayout(frame_proc)
        lblp = QLabel("Procedimiento / Bitácora")
        lblp.setStyleSheet("color:#04335A;font-weight:800;")
        lp.addWidget(lblp)
        self.bitacora = QTextEdit()
        self.bitacora.setReadOnly(True)
        self.bitacora.setStyleSheet("QTextEdit{border:0;background:transparent;color:#1E293B;font-family:Consolas;}")
        lp.addWidget(self.bitacora)

        frame_graf = QFrame()
        frame_graf.setStyleSheet("QFrame{background:white;border:1px solid #C4D4E6;border-radius:11px;}")
        lg = QVBoxLayout(frame_graf)
        lblg = QLabel("Gráfica de f(x) — inspección previa")
        lblg.setStyleSheet("color:#04335A;font-weight:800;")
        lg.addWidget(lblg)

        rango = QHBoxLayout()
        rango.addWidget(QLabel("Vista X desde:"))
        self.spin_vista_min = QDoubleSpinBox()
        self.spin_vista_min.setRange(-1e9, 1e9)
        self.spin_vista_min.setDecimals(4)
        self.spin_vista_min.setValue(-2.0)
        rango.addWidget(self.spin_vista_min)
        rango.addWidget(QLabel("hasta:"))
        self.spin_vista_max = QDoubleSpinBox()
        self.spin_vista_max.setRange(-1e9, 1e9)
        self.spin_vista_max.setDecimals(4)
        self.spin_vista_max.setValue(3.0)
        rango.addWidget(self.spin_vista_max)
        rango.addStretch()
        lg.addLayout(rango)

        self.figura = Figure(figsize=(5, 3), tight_layout=True)
        self.canvas = FigureCanvas(self.figura)
        self.ax = self.figura.add_subplot(111)
        self.ax.grid(True, alpha=0.25)
        # No se conecta ningún cursor/tooltip: al mover el mouse no se despliegan datos.
        lg.addWidget(self.canvas)

        inferior.addWidget(frame_proc)
        inferior.addWidget(frame_graf)
        inferior.setSizes([500, 500])
        splitter.addWidget(frame_tabla)
        splitter.addWidget(inferior)
        splitter.setSizes([270, 360])
        principal.addWidget(splitter, 1)

    def graficar_funcion(self):
        """Grafica primero la función para que el usuario inspeccione continuidad y raíces."""
        try:
            expresion = self.txt_funcion.text()
            simbolica, _ = preparar_funcion(expresion)
            x_min = self.spin_vista_min.value()
            x_max = self.spin_vista_max.value()
            if x_min >= x_max:
                raise ValueError("En la vista gráfica, el valor 'desde' debe ser menor que 'hasta'.")
            self._funcion_graficada = expresion.strip()
            self._intervalo_verificado = None
            self._dibujar_grafica(simbolica, x_min, x_max)
            self.tabla.setRowCount(0)
            self.bitacora.clear()
            self.lbl_resultado.setText(
                "Gráfica lista. Inspecciona si la función es continua y elige A y B alrededor de un cruce con el eje X."
            )
        except ValueError as exc:
            QMessageBox.warning(self, "No se pudo graficar", str(exc))
        except Exception as exc:
            QMessageBox.critical(self, "Error de gráfica", f"No se pudo generar la gráfica.\nDetalle: {exc}")

    def verificar_intervalo(self):
        """Comprueba continuidad y cambio de signo antes de iniciar iteraciones."""
        try:
            expresion = self.txt_funcion.text().strip()
            if self._funcion_graficada != expresion:
                raise ValueError("Primero grafica la función para inspeccionar su comportamiento.")
            a, b = self.spin_xi.value(), self.spin_xf.value()
            if a >= b:
                raise ValueError("A debe ser menor que B.")
            simbolica, f = preparar_funcion(expresion)
            verificar_continuidad(simbolica, a, b)
            fa, fb = f(a), f(b)
            if fa == 0 or fb == 0:
                mensaje = "Uno de los extremos ya es una raíz exacta. Puedes calcular para mostrar el resultado."
            elif fa * fb >= 0:
                raise ValueError(
                    f"No hay cambio de signo en [{a:g}, {b:g}]. f(A)={fa:.8g}, f(B)={fb:.8g}. "
                    "Selecciona otro intervalo observando el cruce con el eje X."
                )
            else:
                mensaje = f"Intervalo válido: la función es continua en [{a:g}, {b:g}] y f(A)·f(B) < 0. Ya puedes calcular."
            self._intervalo_verificado = (expresion, a, b)
            self._dibujar_grafica(
                simbolica,
                min(self.spin_vista_min.value(), a),
                max(self.spin_vista_max.value(), b),
                intervalo_inicial=(a, b)
            )
            self.lbl_resultado.setText(mensaje)
        except ValueError as exc:
            self._intervalo_verificado = None
            QMessageBox.warning(self, "Intervalo no válido", str(exc))
        except Exception as exc:
            self._intervalo_verificado = None
            QMessageBox.critical(self, "Error al verificar", f"No se pudo verificar el intervalo.\nDetalle: {exc}")

    def calcular(self):
        """Ejecuta Bisección únicamente después de la inspección gráfica."""
        try:
            expresion = self.txt_funcion.text().strip()
            if self._funcion_graficada != expresion:
                raise ValueError("Primero presiona 'Graficar función' para inspeccionar la continuidad y elegir el intervalo.")
            if self._intervalo_verificado != (expresion, self.spin_xi.value(), self.spin_xf.value()):
                raise ValueError("Primero presiona 'Verificar intervalo' después de elegir A y B. Si cambias A o B, vuelve a verificar.")

            simbolica, filas, raiz, error, resumen, intervalo_inicial, intervalo_final = resolver_biseccion(
                expresion,
                self.spin_xi.value(),
                self.spin_xf.value(),
                self.spin_er.value(),
                self.spin_n.value()
            )
            self._mostrar_tabla(filas)
            self._mostrar_bitacora(expresion, filas, raiz, error, resumen, intervalo_inicial, intervalo_final)
            x_min = min(self.spin_vista_min.value(), intervalo_inicial[0])
            x_max = max(self.spin_vista_max.value(), intervalo_inicial[1])
            self._dibujar_grafica(
                simbolica, x_min, x_max,
                intervalo_inicial=intervalo_inicial,
                intervalo_final=intervalo_final,
                raiz=raiz
            )
            error_str = "No aplica (raíz exacta en A o B)" if error is None else f"{error:.6g}%"
            self.lbl_resultado.setText(
                f"Raíz aproximada: x = {raiz:.10g}    |    Ea = {error_str}    |    "
                f"Iteraciones: {len(filas)}"
            )
        except ValueError as exc:
            QMessageBox.warning(self, "Error de entrada o cálculo", str(exc))
        except ZeroDivisionError:
            QMessageBox.warning(self, "Error matemático", "Se detectó una división entre cero. Revisa la función y el intervalo.")
        except (TypeError, OverflowError) as exc:
            QMessageBox.warning(self, "Dato no válido", f"No se pudo procesar uno de los datos: {exc}")
        except Exception as exc:
            QMessageBox.critical(self, "Error inesperado", f"No se pudo completar el cálculo.\nDetalle: {exc}")

    def _mostrar_tabla(self, filas):
        self.tabla.setRowCount(len(filas))
        for i, fila in enumerate(filas):
            error = "—" if fila["error"] is None else f'{fila["error"]:.8g}'
            valores = [
                str(fila["it"]), f'{fila["xi"]:.8g}', f'{fila["xf"]:.8g}',
                f'{fila["xm"]:.8g}', f'{fila["fxi"]:.8g}', f'{fila["fxf"]:.8g}',
                f'{fila["fxm"]:.8g}', error, f'{fila["residuo"]:.8g}'
            ]
            for j, valor in enumerate(valores):
                item = QTableWidgetItem(valor)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla.setItem(i, j, item)

    def _mostrar_bitacora(self, expresion, filas, raiz, error, resumen, intervalo_inicial, intervalo_final):
        partes = [
            "<h3 style='color:#04335A'>MÉTODO DE BISECCIÓN</h3>",
            f"<p><b>Función:</b> f(x) = {expresion}</p>",
            "<p><b>Verificación previa:</b> continuidad comprobada simbólicamente en el intervalo y cambio de signo en los extremos.</p>",
            f"<p><b>Intervalo inicial:</b> A = {intervalo_inicial[0]:.10g}; B = {intervalo_inicial[1]:.10g}</p>",
            f"<p><b>Número máximo de iteraciones:</b> {self.spin_n.value()}</p>",
            f"<p><b>Error requerido Ea:</b> {self.spin_er.value():.10g}%</p>",
            "<p><b>Punto medio:</b> C = (A + B) / 2</p>",
            "<p><b>Error aproximado porcentual:</b> Ea = |(C actual - C anterior) / C actual| × 100%</p>",
            "<p><b>Regla:</b> si f(A)·f(C) &lt; 0, B = C; si f(C)·f(B) &lt; 0, A = C.</p><hr>"
        ]
        for fila in filas:
            err = "No aplica en la primera iteración" if fila["error"] is None else f'{fila["error"]:.10g}%'
            actualizacion = fila.get("actualizacion", "No se actualizó el intervalo (raíz exacta).")
            partes.append(
                f"<p><b>Iteración {fila['it']}</b><br>"
                f"C = ({fila['xi']:.10g} + {fila['xf']:.10g}) / 2 = {fila['xm']:.10g}<br>"
                f"f(A) = {fila['fxi']:.10g}; f(B) = {fila['fxf']:.10g}; f(C) = {fila['fxm']:.10g}<br>"
                f"Ea = {err}; |f(C)| = {fila['residuo']:.10g}<br>"
                f"<b>Actualización:</b> {actualizacion}<br><i>{fila['criterio']}</i></p><hr>"
            )
        partes.append(
            f"<h3 style='color:#0284C7'>RESULTADO FINAL</h3>"
            f"<p>{resumen}<br><b>Raíz aproximada:</b> {raiz:.10g}<br>"
            f"<b>Intervalo final:</b> [{intervalo_final[0]:.10g}, {intervalo_final[1]:.10g}]</p>"
        )
        self.bitacora.setHtml("".join(partes))

    def _dibujar_grafica(self, simbolica, x_min, x_max, intervalo_inicial=None, intervalo_final=None, raiz=None):
        """Dibuja la curva; tras resolver, marca intervalos y raíz sin tooltips de mouse."""
        self.ax.clear()
        funcion = sp.lambdify(sp.Symbol("x"), simbolica, modules=["numpy"])
        if x_min >= x_max:
            raise ValueError("El rango horizontal de la gráfica no es válido.")
        xs = np.linspace(x_min, x_max, 1000)
        with np.errstate(all="ignore"):
            ys = np.asarray(funcion(xs), dtype=float)
        if ys.ndim == 0:
            ys = np.full_like(xs, float(ys))
        ys = np.where(np.isfinite(ys), ys, np.nan)
        self.ax.plot(xs, ys, label=f"f(x) = {sp.sstr(simbolica)}", linewidth=2)
        self.ax.axhline(0, color="black", linewidth=0.9, label="Eje X (f(x)=0)")
        self.ax.axvline(0, color="#64748B", linewidth=0.7, alpha=0.7)

        if intervalo_inicial is not None:
            a0, b0 = intervalo_inicial
            self.ax.axvspan(a0, b0, color="#F59E0B", alpha=0.13, label="Intervalo inicial [A,B]")
            self.ax.axvline(a0, color="#16A34A", linestyle="--", linewidth=1.3, label=f"A inicial = {a0:.6g}")
            self.ax.axvline(b0, color="#DC2626", linestyle="--", linewidth=1.3, label=f"B inicial = {b0:.6g}")
        if intervalo_final is not None:
            af, bf = intervalo_final
            self.ax.axvspan(af, bf, color="#2563EB", alpha=0.28, label="Intervalo final")
            self.ax.axvline(af, color="#16A34A", linestyle=":", linewidth=1.5, label=f"A final = {af:.6g}")
            self.ax.axvline(bf, color="#DC2626", linestyle=":", linewidth=1.5, label=f"B final = {bf:.6g}")
        if raiz is not None:
            self.ax.axvline(raiz, color="#7C3AED", linestyle="-.", linewidth=1.3, label=f"Raíz ≈ {raiz:.8g}")
            self.ax.scatter([raiz], [0], color="#7C3AED", edgecolors="white", zorder=6, label="Aproximación sobre eje X")

        self.ax.set_xlim(x_min, x_max)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.set_title("Gráfica de la función")
        self.ax.grid(True, alpha=0.25)
        self.ax.legend(fontsize=7, loc="best")
        self.figura.tight_layout()
        self.canvas.draw()

    def limpiar(self):
        self.tabla.setRowCount(0)
        self.bitacora.clear()
        self.lbl_resultado.setText("Paso 1: ingresa la función y presiona 'Graficar función'.")
        self._funcion_graficada = None
        self._intervalo_verificado = None
        self.ax.clear()
        self.ax.grid(True, alpha=0.25)
        self.canvas.draw()
