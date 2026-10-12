# ui/determinantes_window.py

from fractions import Fraction
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
    QTextEdit, QComboBox, QHeaderView, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from core.determinantes import CalculadoraDeterminantes


# PALETA DE COLORES AZUL GLACIAL / ÁRTICO
COLOR_FONDO_APP = "#F4F8FB"
COLOR_TARJETA_BG = "#FFFFFF"
COLOR_TEXTO_MAIN = "#031E36"
COLOR_AZUL_PRIMARIO = "#04335A"
COLOR_AZUL_MEDIO = "#4474A3"
COLOR_CELESTE_HIELO = "#9ABCE0"
COLOR_AZUL_CLARO = "#C4D4E6"


class DeterminantesWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("BelugaCalc - Determinantes")
        self.resize(1100, 800)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(f"background-color: {COLOR_FONDO_APP};")

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(24, 20, 24, 20)
        layout_principal.setSpacing(16)

        # 1. TÍTULO DE CABECERA
        titulo = QLabel("Determinantes y Regla de Cramer", self)
        titulo.setStyleSheet(f"""
            color: {COLOR_TEXTO_MAIN};
            font-size: 26px;
            font-weight: 900;
            font-family: 'Segoe UI', sans-serif;
        """)
        layout_principal.addWidget(titulo)

        # 2. BARRA DE CONTROLES SUPERIORES (STEPPER + Y -)
        controles = QHBoxLayout()

        lbl_n = QLabel("Dimensión (N × N):", self)
        lbl_n.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 13px; font-weight: 700;")

        btn_menos = QPushButton("−", self)
        btn_menos.setFixedSize(36, 36)
        btn_menos.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_menos.clicked.connect(lambda: self.spin_n.setValue(self.spin_n.value() - 1))

        self.spin_n = QSpinBox(self)
        self.spin_n.setRange(2, 6)
        self.spin_n.setValue(3)
        self.spin_n.setFixedHeight(36)
        self.spin_n.valueChanged.connect(self.crear_matriz)

        btn_mas = QPushButton("+", self)
        btn_mas.setFixedSize(36, 36)
        btn_mas.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_mas.clicked.connect(lambda: self.spin_n.setValue(self.spin_n.value() + 1))

        style_btn_step = f"""
            QPushButton {{
                background-color: {COLOR_AZUL_CLARO};
                color: {COLOR_AZUL_PRIMARIO};
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {COLOR_CELESTE_HIELO};
            }}
        """
        btn_menos.setStyleSheet(style_btn_step)
        btn_mas.setStyleSheet(style_btn_step)

        self.spin_n.setStyleSheet(f"""
            QSpinBox {{
                background-color: #FFFFFF;
                border: 1px solid {COLOR_AZUL_CLARO};
                border-radius: 10px;
                padding: 0px 8px;
                color: {COLOR_TEXTO_MAIN};
                font-size: 14px;
                font-weight: 800;
            }}
            QSpinBox::up-button, QSpinBox::down-button {{ width: 0px; }}
        """)

        # Selector Método
        lbl_metodo = QLabel("Método:", self)
        lbl_metodo.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 13px; font-weight: 700;")

        self.combo_metodo = QComboBox(self)
        self.combo_metodo.addItems(["Cofactores", "Eliminación Gaussiana", "Sarrus", "Regla de Cramer"])
        self.combo_metodo.setFixedHeight(36)
        self.combo_metodo.setStyleSheet(f"""
            QComboBox {{
                background-color: #FFFFFF;
                border: 1px solid {COLOR_AZUL_CLARO};
                border-radius: 10px;
                padding: 0px 12px;
                color: {COLOR_AZUL_PRIMARIO};
                font-weight: 700;
                font-size: 13px;
            }}
            QComboBox::drop-down {{ border: none; }}
        """)
        self.combo_metodo.currentTextChanged.connect(self.actualizar_interfaz_metodo)

        # Botón Calcular
        btn_calcular = QPushButton("Calcular / Resolver", self)
        btn_calcular.setFixedHeight(38)
        btn_calcular.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_calcular.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_AZUL_PRIMARIO};
                color: #FFFFFF;
                font-size: 14px;
                font-weight: 700;
                border-radius: 12px;
                padding: 0px 20px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {COLOR_AZUL_MEDIO};
            }}
        """)
        btn_calcular.clicked.connect(self.calcular_resultado)

        # Botón Limpiar
        btn_limpiar = QPushButton("Limpiar", self)
        btn_limpiar.setFixedHeight(38)
        btn_limpiar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_limpiar.setStyleSheet(f"""
            QPushButton {{
                background-color: #FFFFFF;
                color: {COLOR_AZUL_MEDIO};
                font-size: 13px;
                font-weight: 700;
                border-radius: 12px;
                border: 1.5px solid {COLOR_AZUL_CLARO};
                padding: 0px 16px;
            }}
            QPushButton:hover {{
                background-color: #F0F9FF;
            }}
        """)
        btn_limpiar.clicked.connect(self.limpiar_matriz)

        controles.addWidget(lbl_n)
        controles.addWidget(btn_menos)
        controles.addWidget(self.spin_n)
        controles.addWidget(btn_mas)
        controles.addSpacing(16)
        controles.addWidget(lbl_metodo)
        controles.addWidget(self.combo_metodo)
        controles.addSpacing(16)
        controles.addWidget(btn_calcular)
        controles.addWidget(btn_limpiar)
        controles.addStretch()

        layout_principal.addLayout(controles)

        style_tabla = f"""
            QTableWidget {{
                background-color: #FAFCFE;
                border: 1px solid {COLOR_AZUL_CLARO};
                border-radius: 12px;
                gridline-color: #E2E8F0;
                color: {COLOR_TEXTO_MAIN};
                font-weight: 600;
            }}
            QTableWidget::item {{
                border-radius: 6px;
                padding: 4px;
            }}
            QTableWidget::item:focus {{
                background-color: #E0F2FE;
                border: 1.5px solid {COLOR_AZUL_MEDIO};
            }}
            QHeaderView::section {{
                background-color: {COLOR_AZUL_CLARO};
                color: {COLOR_AZUL_PRIMARIO};
                font-weight: 700;
                border: none;
                padding: 6px;
            }}
        """

        # 3. TARJETA MATRIZ DE ENTRADA
        card_matriz = QFrame(self)
        card_matriz.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_TARJETA_BG};
                border-radius: 20px;
                border: 1px solid {COLOR_AZUL_CLARO};
            }}
        """)

        sombra = QGraphicsDropShadowEffect(self)
        sombra.setBlurRadius(25)
        sombra.setColor(QColor(3, 30, 54, 20))
        sombra.setYOffset(6)
        card_matriz.setGraphicsEffect(sombra)

        card_layout = QVBoxLayout(card_matriz)
        card_layout.setContentsMargins(18, 16, 18, 16)

        self.tabla_matriz = QTableWidget(card_matriz)
        self.tabla_matriz.setStyleSheet(style_tabla)
        card_layout.addWidget(self.tabla_matriz)

        layout_principal.addWidget(card_matriz, 3)

        # 4. DOS TARJETAS PARALELAS: RESULTADO Y PROCEDIMIENTO
        layout_resultados = QHBoxLayout()

        # Tarjeta Resultado
        box_res = QFrame(self)
        box_res.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_TARJETA_BG};
                border-radius: 18px;
                border: 1px solid {COLOR_AZUL_CLARO};
            }}
        """)
        lay_r = QVBoxLayout(box_res)
        lay_r.setContentsMargins(16, 14, 16, 14)

        lbl_r_title = QLabel("Resultado:", box_res)
        lbl_r_title.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 14px; font-weight: 800; border: none;")

        self.tabla_resultado = QTableWidget(box_res)
        self.tabla_resultado.setStyleSheet(style_tabla)

        # ETIQUETA INFERIOR PARA LA EXPRESIÓN EN FORMA DE ECUACIÓN
        self.lbl_res_texto = QLabel("", box_res)
        self.lbl_res_texto.setWordWrap(True)
        self.lbl_res_texto.setStyleSheet(f"""
            QLabel {{
                background-color: #F0F9FF;
                color: {COLOR_AZUL_PRIMARIO};
                font-weight: 700;
                font-size: 12px;
                border-radius: 8px;
                border: 1px solid {COLOR_AZUL_CLARO};
                padding: 8px 12px;
            }}
        """)

        lay_r.addWidget(lbl_r_title)
        lay_r.addWidget(self.tabla_resultado, 1)
        lay_r.addWidget(self.lbl_res_texto)

        # Tarjeta Procedimiento Paso a Paso
        box_proc = QFrame(self)
        box_proc.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_TARJETA_BG};
                border-radius: 18px;
                border: 1px solid {COLOR_AZUL_CLARO};
            }}
        """)
        lay_p = QVBoxLayout(box_proc)
        lay_p.setContentsMargins(16, 14, 16, 14)

        lbl_p_title = QLabel("Procedimiento Paso a Paso:", box_proc)
        lbl_p_title.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 14px; font-weight: 800; border: none;")

        self.txt_pasos = QTextEdit(box_proc)
        self.txt_pasos.setReadOnly(True)
        self.txt_pasos.setStyleSheet("""
            QTextEdit {
                border: none;
                background: transparent;
                font-size: 13px;
                color: #1E293B;
            }
        """)

        lay_p.addWidget(lbl_p_title)
        lay_p.addWidget(self.txt_pasos)

        layout_resultados.addWidget(box_res, 1)
        layout_resultados.addWidget(box_proc, 1)

        layout_principal.addLayout(layout_resultados, 2)

        self.crear_matriz()

    def actualizar_interfaz_metodo(self, metodo):
        if metodo == "Sarrus":
            if self.spin_n.value() > 4:
                self.spin_n.setValue(4)
            self.spin_n.setRange(2, 4)
        else:
            self.spin_n.setRange(2, 6)

        self.crear_matriz()

    def crear_matriz(self):
        n = self.spin_n.value()
        metodo = self.combo_metodo.currentText()
        cols = n + 1 if metodo == "Regla de Cramer" else n

        self.tabla_matriz.setRowCount(n)
        self.tabla_matriz.setColumnCount(cols)

        header_h = self.tabla_matriz.horizontalHeader()
        header_v = self.tabla_matriz.verticalHeader()

        headers = [f"x{j+1}" for j in range(n)]
        if metodo == "Regla de Cramer":
            headers.append("T. Indep (b)")

        self.tabla_matriz.setHorizontalHeaderLabels(headers)

        for j in range(cols):
            header_h.setSectionResizeMode(j, QHeaderView.ResizeMode.Stretch)
        for i in range(n):
            header_v.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        for i in range(n):
            for j in range(cols):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_matriz.setItem(i, j, item)

        self.limpiar_resultados()

    def limpiar_resultados(self):
        self.tabla_resultado.clear()
        self.tabla_resultado.setRowCount(0)
        self.tabla_resultado.setColumnCount(0)
        self.lbl_res_texto.setText("")
        self.txt_pasos.clear()

    def limpiar_matriz(self):
        for i in range(self.tabla_matriz.rowCount()):
            for j in range(self.tabla_matriz.columnCount()):
                item = self.tabla_matriz.item(i, j)
                if item:
                    item.setText("0")
        self.limpiar_resultados()

    def obtener_matriz_datos(self):
        n = self.spin_n.value()
        metodo = self.combo_metodo.currentText()
        matriz_A = []
        vector_b = []

        for i in range(n):
            fila = []
            for j in range(n):
                item = self.tabla_matriz.item(i, j)
                texto = item.text().strip() if item else ""
                val = float(texto.replace(",", ".")) if texto else 0.0
                fila.append(val)
            matriz_A.append(fila)

            if metodo == "Regla de Cramer":
                item_b = self.tabla_matriz.item(i, n)
                texto_b = item_b.text().strip() if item_b else ""
                val_b = float(texto_b.replace(",", ".")) if texto_b else 0.0
                vector_b.append(val_b)

        return matriz_A, vector_b

    def formatear_a_fraccion(self, valor):
        """Convierte números a fracciones simplificadas o enteros."""
        if hasattr(valor, "numerator") and hasattr(valor, "denominator"):
            if valor.denominator == 1:
                return str(valor.numerator)
            return f"{valor.numerator}/{valor.denominator}"

        if isinstance(valor, float):
            if valor.is_integer():
                return str(int(valor))
            frac = Fraction(valor).limit_denominator(1000)
            if frac.denominator == 1:
                return str(frac.numerator)
            return f"{frac.numerator}/{frac.denominator}"

        return str(valor)

    def mostrar_resultado_doble(self, res_valor, metodo):
        """Muestra la solución en la tabla Y la ecuación explicativa en la tarjeta inferior."""
        self.tabla_resultado.clear()

        if metodo == "Regla de Cramer" and isinstance(res_valor, (list, tuple)):
            filas = len(res_valor)
            self.tabla_resultado.setRowCount(filas)
            self.tabla_resultado.setColumnCount(1)
            self.tabla_resultado.setHorizontalHeaderLabels(["Solución Vectorial"])

            elementos_str = []
            ecuaciones_list = []

            for i, val in enumerate(res_valor):
                self.tabla_resultado.setVerticalHeaderItem(i, QTableWidgetItem(f"x{i+1}"))
                txt = self.formatear_a_fraccion(val)
                elementos_str.append(f"'{txt}'")
                ecuaciones_list.append(f"x{i+1} = {txt}")

                item = QTableWidgetItem(txt)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_resultado.setItem(i, 0, item)

            self.tabla_resultado.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            str_ecuaciones = "<br>".join(ecuaciones_list)
            str_vector = ", ".join(elementos_str)
            self.lbl_res_texto.setText(
                f"<b>Ecuación(es):</b><br>{str_ecuaciones}<br><br>"
                f"<b>Vector Solución:</b> X = [{str_vector}]ᵀ"
            )
        else:
            self.tabla_resultado.setRowCount(1)
            self.tabla_resultado.setColumnCount(1)
            self.tabla_resultado.setHorizontalHeaderLabels(["det(A)"])
            self.tabla_resultado.setVerticalHeaderItem(0, QTableWidgetItem("Valor"))

            txt = self.formatear_a_fraccion(res_valor) if isinstance(res_valor, (int, float, Fraction)) else str(res_valor)

            item = QTableWidgetItem(txt)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabla_resultado.setItem(0, 0, item)

            self.tabla_resultado.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            self.lbl_res_texto.setText(
                f"<b>Expresión de Resultado:</b><br>"
                f"det(A) = {txt}"
            )

    def formatear_pasos_html(self, metodo, pasos):
        """Genera una salida ordenada verticalmente en HTML."""
        html = []
        html.append(f"<div style='background-color: #04335A; color: #FFFFFF; padding: 6px 12px; border-radius: 8px; font-weight: bold;'>MÉTODO: {metodo.upper()}</div>")
        
        html.append("<div style='background-color: #E0F2FE; color: #04335A; padding: 6px 12px; border-radius: 8px; font-weight: bold; margin-top: 10px; margin-bottom: 6px;'>PROCEDIMIENTO PASO A PASO</div>")
        
        html.append("<pre style=\"font-family: 'Consolas', 'Courier New', monospace; font-size: 12.5px; color: #04335A; margin: 4px 0; white-space: pre-wrap;\">")
        html.append(str(pasos))
        html.append("</pre>")

        return "".join(html)

    def calcular_resultado(self):
        try:
            matriz_A, vector_b = self.obtener_matriz_datos()
            metodo = self.combo_metodo.currentText()

            if metodo == "Cofactores":
                val, pasos = CalculadoraDeterminantes.determinante_cofactores(matriz_A)
            elif metodo == "Sarrus":
                val, pasos = CalculadoraDeterminantes.determinante_sarrus(matriz_A)
            elif metodo == "Regla de Cramer":
                val, pasos = CalculadoraDeterminantes.regla_cramer(matriz_A, vector_b)
            else:
                val, pasos = CalculadoraDeterminantes.determinante_gauss(matriz_A)

            # Mostrar resultado en tabla Y en caja de texto explícita
            self.mostrar_resultado_doble(val, metodo)

            # Inyección de HTML formateado verticalmente
            html_procedimiento = self.formatear_pasos_html(metodo, pasos)
            self.txt_pasos.setHtml(html_procedimiento)

        except ValueError as ve:
            self.limpiar_resultados()
            QMessageBox.warning(self, "Aviso de Validación", str(ve))
        except Exception as e:
            self.limpiar_resultados()
            QMessageBox.critical(self, "Error", f"Ocurrió un error en el cálculo:\n{e}")