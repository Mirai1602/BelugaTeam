# ui/avanzada_window.py

import os
from fractions import Fraction
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
    QTextEdit, QFrame, QGraphicsDropShadowEffect, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from core.operaciones import MatrizModel
from ui.conversiones_window import ConversionesWindow


# PALETA DE COLORES AZUL GLACIAL / ÁRTICO
COLOR_FONDO_APP = "#F4F8FB"
COLOR_TARJETA_BG = "#FFFFFF"
COLOR_TEXTO_MAIN = "#031E36"
COLOR_AZUL_PRIMARIO = "#04335A"
COLOR_AZUL_MEDIO = "#4474A3"
COLOR_CELESTE_HIELO = "#9ABCE0"
COLOR_AZUL_CLARO = "#C4D4E6"


class CalculadoraMatricesAvanzada(QWidget):
    def __init__(self, ventana_principal=None):
        super().__init__()

        self.ventana_principal = ventana_principal
        self.setWindowTitle("BelugaCalc - Avanzada")
        self.resize(1100, 800)

        self.tablas = []
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(f"background-color: {COLOR_FONDO_APP};")

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(24, 20, 24, 20)
        layout_principal.setSpacing(16)

        # 1. TÍTULO DE CABECERA
        titulo = QLabel("Calculadora Avanzada (Sistemas AX = B)", self)
        titulo.setStyleSheet(f"""
            color: {COLOR_TEXTO_MAIN};
            font-size: 26px;
            font-weight: 900;
            font-family: 'Segoe UI', sans-serif;
        """)
        layout_principal.addWidget(titulo)

        # 2. BARRA DE CONTROLES SUPERIORES (STEPPER + Y -)
        controles = QHBoxLayout()

        # Stepper Filas
        lbl_f = QLabel("Ecuaciones (filas):", self)
        lbl_f.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 13px; font-weight: 700;")

        btn_f_menos = QPushButton("−", self)
        btn_f_menos.setFixedSize(36, 36)
        btn_f_menos.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_f_menos.clicked.connect(lambda: self.spin_filas.setValue(self.spin_filas.value() - 1))

        self.spin_filas = QSpinBox(self)
        self.spin_filas.setRange(1, 10)
        self.spin_filas.setValue(3)
        self.spin_filas.setFixedHeight(36)
        self.spin_filas.valueChanged.connect(self.generar_tablas)

        btn_f_mas = QPushButton("+", self)
        btn_f_mas.setFixedSize(36, 36)
        btn_f_mas.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_f_mas.clicked.connect(lambda: self.spin_filas.setValue(self.spin_filas.value() + 1))

        # Stepper Columnas
        lbl_c = QLabel("Variables (columnas):", self)
        lbl_c.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 13px; font-weight: 700;")

        btn_c_menos = QPushButton("−", self)
        btn_c_menos.setFixedSize(36, 36)
        btn_c_menos.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_c_menos.clicked.connect(lambda: self.spin_columnas.setValue(self.spin_columnas.value() - 1))

        self.spin_columnas = QSpinBox(self)
        self.spin_columnas.setRange(1, 10)
        self.spin_columnas.setValue(3)
        self.spin_columnas.setFixedHeight(36)
        self.spin_columnas.valueChanged.connect(self.generar_tablas)

        btn_c_mas = QPushButton("+", self)
        btn_c_mas.setFixedSize(36, 36)
        btn_c_mas.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_c_mas.clicked.connect(lambda: self.spin_columnas.setValue(self.spin_columnas.value() + 1))

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
        btn_f_menos.setStyleSheet(style_btn_step)
        btn_f_mas.setStyleSheet(style_btn_step)
        btn_c_menos.setStyleSheet(style_btn_step)
        btn_c_mas.setStyleSheet(style_btn_step)

        style_spin = f"""
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
        """
        self.spin_filas.setStyleSheet(style_spin)
        self.spin_columnas.setStyleSheet(style_spin)

        # Botones Secundarios
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
            QPushButton:hover {{ background-color: #F0F9FF; }}
        """)
        btn_limpiar.clicked.connect(self.limpiar_tablas)

        btn_conversiones = QPushButton("Conversiones", self)
        btn_conversiones.setFixedHeight(38)
        btn_conversiones.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_conversiones.setStyleSheet(f"""
            QPushButton {{
                background-color: #FFFFFF;
                color: {COLOR_AZUL_MEDIO};
                font-size: 13px;
                font-weight: 700;
                border-radius: 12px;
                border: 1.5px solid {COLOR_AZUL_CLARO};
                padding: 0px 16px;
            }}
            QPushButton:hover {{ background-color: #F0F9FF; }}
        """)
        btn_conversiones.clicked.connect(self.abrir_conversiones)

        btn_volver = QPushButton("Volver", self)
        btn_volver.setFixedHeight(38)
        btn_volver.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_volver.setStyleSheet(f"""
            QPushButton {{
                background-color: #FFFFFF;
                color: #64748B;
                font-size: 13px;
                font-weight: 700;
                border-radius: 12px;
                border: 1.5px solid #E2E8F0;
                padding: 0px 16px;
            }}
            QPushButton:hover {{ color: {COLOR_AZUL_PRIMARIO}; }}
        """)
        btn_volver.clicked.connect(self.volver)

        controles.addWidget(lbl_f)
        controles.addWidget(btn_f_menos)
        controles.addWidget(self.spin_filas)
        controles.addWidget(btn_f_mas)
        controles.addSpacing(10)
        controles.addWidget(lbl_c)
        controles.addWidget(btn_c_menos)
        controles.addWidget(self.spin_columnas)
        controles.addWidget(btn_c_mas)
        controles.addSpacing(16)
        controles.addWidget(btn_limpiar)
        controles.addWidget(btn_conversiones)
        controles.addWidget(btn_volver)
        controles.addStretch()

        layout_principal.addLayout(controles)

        # 3. CONTENEDOR DE MATRICES A Y B EN TARJETAS
        tablas_layout = QHBoxLayout()
        tablas_layout.setSpacing(16)

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
                padding: 4px;
            }}
        """

        # Tarjeta Matriz A
        card_A = QFrame(self)
        card_A.setStyleSheet(f"QFrame {{ background-color: {COLOR_TARJETA_BG}; border-radius: 20px; border: 1px solid {COLOR_AZUL_CLARO}; }}")
        sombra_A = QGraphicsDropShadowEffect(self)
        sombra_A.setBlurRadius(25)
        sombra_A.setColor(QColor(3, 30, 54, 20))
        sombra_A.setYOffset(6)
        card_A.setGraphicsEffect(sombra_A)

        lay_A = QVBoxLayout(card_A)
        lay_A.setContentsMargins(18, 16, 18, 16)
        lbl_A_title = QLabel("Matriz A (Coeficientes)", card_A)
        lbl_A_title.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 15px; font-weight: 800; border: none;")
        self.tabla_A = QTableWidget(card_A)
        self.tabla_A.setStyleSheet(style_tabla)
        lay_A.addWidget(lbl_A_title)
        lay_A.addWidget(self.tabla_A)

        # Tarjeta Matriz B
        card_B = QFrame(self)
        card_B.setFixedWidth(240)
        card_B.setStyleSheet(f"QFrame {{ background-color: {COLOR_TARJETA_BG}; border-radius: 20px; border: 1px solid {COLOR_AZUL_CLARO}; }}")
        sombra_B = QGraphicsDropShadowEffect(self)
        sombra_B.setBlurRadius(25)
        sombra_B.setColor(QColor(3, 30, 54, 20))
        sombra_B.setYOffset(6)
        card_B.setGraphicsEffect(sombra_B)

        lay_B = QVBoxLayout(card_B)
        lay_B.setContentsMargins(18, 16, 18, 16)
        lbl_B_title = QLabel("Matriz B (Indep.)", card_B)
        lbl_B_title.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 15px; font-weight: 800; border: none;")
        self.tabla_B = QTableWidget(card_B)
        self.tabla_B.setStyleSheet(style_tabla)
        lay_B.addWidget(lbl_B_title)
        lay_B.addWidget(self.tabla_B)

        tablas_layout.addWidget(card_A, 3)
        tablas_layout.addWidget(card_B, 1)

        layout_principal.addLayout(tablas_layout, 3)

        # 4. BOTONES DE ACCIÓN
        operaciones_layout = QHBoxLayout()

        btn_gauss = QPushButton("Resolver Gauss", self)
        btn_gauss_jordan = QPushButton("Resolver Gauss-Jordan", self)
        btn_pivotes = QPushButton("Reducción de Pivotes", self)

        style_btn_metodo = f"""
            QPushButton {{
                background-color: {COLOR_AZUL_PRIMARIO};
                color: #FFFFFF;
                font-size: 13px;
                font-weight: 700;
                border-radius: 12px;
                padding: 8px 18px;
                border: none;
            }}
            QPushButton:hover {{ background-color: {COLOR_AZUL_MEDIO}; }}
        """
        btn_gauss.setStyleSheet(style_btn_metodo)
        btn_gauss_jordan.setStyleSheet(style_btn_metodo)
        btn_pivotes.setStyleSheet(style_btn_metodo)

        btn_gauss.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_gauss_jordan.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_pivotes.setCursor(Qt.CursorShape.PointingHandCursor)

        btn_gauss.clicked.connect(self.ejecutar_gauss)
        btn_gauss_jordan.clicked.connect(self.ejecutar_gauss_jordan)
        btn_pivotes.clicked.connect(self.ejecutar_reduccion_pivotes)

        operaciones_layout.addWidget(btn_gauss)
        operaciones_layout.addWidget(btn_gauss_jordan)
        operaciones_layout.addWidget(btn_pivotes)
        operaciones_layout.addStretch()

        layout_principal.addLayout(operaciones_layout)

        # 5. TARJETAS PARALELAS: RESULTADO Y PROCEDIMIENTO
        layout_resultados = QHBoxLayout()

        # Tarjeta Resultado Doble
        box_res = QFrame(self)
        box_res.setStyleSheet(f"QFrame {{ background-color: {COLOR_TARJETA_BG}; border-radius: 18px; border: 1px solid {COLOR_AZUL_CLARO}; }}")
        lay_r = QVBoxLayout(box_res)
        lay_r.setContentsMargins(16, 14, 16, 14)

        lbl_r_title = QLabel("Vector Solución (x) / Resultado:", box_res)
        lbl_r_title.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 14px; font-weight: 800; border: none;")

        self.tabla_res = QTableWidget(box_res)
        self.tabla_res.setStyleSheet(style_tabla)

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
        lay_r.addWidget(self.tabla_res, 1)
        lay_r.addWidget(self.lbl_res_texto)

        # Tarjeta Procedimiento Paso a Paso
        box_proc = QFrame(self)
        box_proc.setStyleSheet(f"QFrame {{ background-color: {COLOR_TARJETA_BG}; border-radius: 18px; border: 1px solid {COLOR_AZUL_CLARO}; }}")
        lay_p = QVBoxLayout(box_proc)
        lay_p.setContentsMargins(16, 14, 16, 14)

        lbl_p_title = QLabel("Procedimiento Paso a Paso y Clasificación:", box_proc)
        lbl_p_title.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 14px; font-weight: 800; border: none;")

        self.txt_bitacora = QTextEdit(box_proc)
        self.txt_bitacora.setReadOnly(True)
        self.txt_bitacora.setStyleSheet("QTextEdit { border: none; background: transparent; font-size: 13px; color: #1E293B; }")

        lay_p.addWidget(lbl_p_title)
        lay_p.addWidget(self.txt_bitacora)

        layout_resultados.addWidget(box_res, 1)
        layout_resultados.addWidget(box_proc, 1)

        layout_principal.addLayout(layout_resultados, 2)

        self.generar_tablas()

    def generar_tablas(self):
        filas = self.spin_filas.value()
        columnas = self.spin_columnas.value()

        self.tabla_A.setRowCount(filas)
        self.tabla_A.setColumnCount(columnas)
        self.tabla_B.setRowCount(filas)
        self.tabla_B.setColumnCount(1)

        self.tabla_A.setHorizontalHeaderLabels([f"x{j+1}" for j in range(columnas)])
        self.tabla_B.setHorizontalHeaderLabels(["b"])

        self.tabla_A.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_B.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for i in range(filas):
            for j in range(columnas):
                if self.tabla_A.item(i, j) is None:
                    item = QTableWidgetItem("0")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.tabla_A.setItem(i, j, item)

            if self.tabla_B.item(i, 0) is None:
                item_b = QTableWidgetItem("0")
                item_b.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_B.setItem(i, 0, item_b)

        self.limpiar_resultados()
        self.tablas = [self.tabla_A, self.tabla_B]

    def limpiar_resultados(self):
        self.tabla_res.clear()
        self.tabla_res.setRowCount(0)
        self.tabla_res.setColumnCount(0)
        self.lbl_res_texto.setText("")
        self.txt_bitacora.clear()

    def limpiar_tablas(self):
        for tabla in [self.tabla_A, self.tabla_B]:
            for i in range(tabla.rowCount()):
                for j in range(tabla.columnCount()):
                    item = tabla.item(i, j)
                    if item:
                        item.setText("0")
        self.limpiar_resultados()

    def leer_matriz(self, tabla):
        matriz = []
        for i in range(tabla.rowCount()):
            fila = []
            for j in range(tabla.columnCount()):
                item = tabla.item(i, j)
                texto = item.text().strip() if item else ""
                val = float(texto.replace(",", ".")) if texto else 0.0
                fila.append(val)
            matriz.append(fila)
        return matriz

    def formatear_a_fraccion(self, valor):
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

    def mostrar_resultado_doble(self, matriz_res, clasificacion=""):
        """Renderiza la solución de forma matricial Y SIEMPRE muestra la ecuación vectorial/texto."""
        self.tabla_res.clear()

        # CASO 1: Cadena de texto directa (sistema sin solución o mensaje paramétrico)
        if isinstance(matriz_res, str):
            self.tabla_res.setRowCount(1)
            self.tabla_res.setColumnCount(1)
            self.tabla_res.setHorizontalHeaderLabels(["Solución"])
            item = QTableWidgetItem(matriz_res)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabla_res.setItem(0, 0, item)
            self.tabla_res.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            info_c = f"<b>{clasificacion}</b><br>" if clasificacion else ""
            self.lbl_res_texto.setText(f"{info_c}<b>Ecuación Solución:</b> {matriz_res}")
            return

        if not matriz_res:
            self.limpiar_resultados()
            return

        # CASO 2: Lista de resultados (numéricos o cadenas por variable como x1 = t)
        filas = len(matriz_res)
        columnas = len(matriz_res[0]) if isinstance(matriz_res[0], list) else 1

        self.tabla_res.setRowCount(filas)
        self.tabla_res.setColumnCount(columnas)
        self.tabla_res.setHorizontalHeaderLabels(["Valor"])

        elementos_str = []
        ecuaciones_list = []

        for i in range(filas):
            self.tabla_res.setVerticalHeaderItem(i, QTableWidgetItem(f"x{i+1}"))
            val = matriz_res[i][0] if isinstance(matriz_res[0], list) else matriz_res[i]

            if isinstance(val, (int, float)) or hasattr(val, "numerator"):
                txt = self.formatear_a_fraccion(val)
            else:
                txt = str(val)

            elementos_str.append(f"'{txt}'")
            ecuaciones_list.append(f"x{i+1} = {txt}")

            item = QTableWidgetItem(txt)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabla_res.setItem(i, 0, item)

        self.tabla_res.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # SIEMPRE MOSTRAR LA SOLUCIÓN EN FORMA DE ECUACIÓN Y VECTOR EN LA ETIQUETA INFERIOR
        str_vector = ", ".join(elementos_str)
        str_ecuaciones = "<br>".join(ecuaciones_list)
        info_clasif = f"<b>{clasificacion}</b><br><br>" if clasificacion else ""
        
        self.lbl_res_texto.setText(
            f"{info_clasif}"
            f"<b>Ecuación(es):</b><br>{str_ecuaciones}<br><br>"
            f"<b>Vector Solución:</b> X = [{str_vector}]ᵀ"
        )

    def formatear_reporte_html(self, metodo, clasificacion, pasos, verificacion):
        html = []
        html.append(f"<div style='background-color: #04335A; color: #FFFFFF; padding: 6px 12px; border-radius: 8px; font-weight: bold;'>MÉTODO: {metodo}</div>")
        
        if clasificacion:
            html.append(f"<p style='color: #031E36; font-weight: bold; margin: 8px 0 2px 0;'>Clasificación: <span style='color: #0284C7;'>{clasificacion}</span></p>")

        html.append("<div style='background-color: #E0F2FE; color: #04335A; padding: 6px 12px; border-radius: 8px; font-weight: bold; margin-top: 10px; margin-bottom: 6px;'>PROCEDIMIENTO PASO A PASO</div>")
        
        html.append("<pre style=\"font-family: 'Consolas', 'Courier New', monospace; font-size: 12.5px; color: #04335A; margin: 4px 0; white-space: pre-wrap;\">")
        html.append(str(pasos))
        html.append("</pre>")

        if verificacion:
            html.append("<div style='background-color: #0284C7; color: #FFFFFF; padding: 6px 12px; border-radius: 8px; font-weight: bold; margin-top: 10px; margin-bottom: 6px;'>VERIFICACIÓN AUTOMÁTICA (Ax = b)</div>")
            html.append(f"<p style='color: #334155; font-size: 12px; margin: 4px 0;'>{verificacion}</p>")

        return "".join(html)

    def ejecutar_gauss(self):
        try:
            A, B = self.obtener_A_y_B()
            if A is None:
                return

            pasos, clasificacion, solucion, verificacion = MatrizModel.gauss_resolver_completo(A, B)
            self.mostrar_resultado_doble(solucion, clasificacion)
            html = self.formatear_reporte_html("GAUSS", clasificacion, pasos, verificacion)
            self.txt_bitacora.setHtml(html)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al procesar Gauss: {e}")

    def ejecutar_gauss_jordan(self):
        try:
            A, B = self.obtener_A_y_B()
            if A is None:
                return

            pasos, clasificacion, solucion, verificacion = MatrizModel.metodo_gauss_jordan(A, B)
            self.mostrar_resultado_doble(solucion, clasificacion)
            html = self.formatear_reporte_html("GAUSS-JORDAN", clasificacion, pasos, verificacion)
            self.txt_bitacora.setHtml(html)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al procesar Gauss-Jordan: {e}")

    def ejecutar_reduccion_pivotes(self):
        try:
            A, B = self.obtener_A_y_B()
            if A is None:
                return

            pasos, clasificacion, matriz, verificacion = MatrizModel.reduccion_pivotes(A, B)
            self.mostrar_resultado_doble(matriz, clasificacion)
            html = self.formatear_reporte_html("REDUCCIÓN DE PIVOTES", clasificacion, pasos, verificacion)
            self.txt_bitacora.setHtml(html)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error en la reducción de pivotes: {e}")

    def obtener_A_y_B(self):
        A = self.leer_matriz(self.tabla_A)
        B = self.leer_matriz(self.tabla_B)

        if len(A) != len(B):
            QMessageBox.warning(self, "Error", "La Matriz A y el Vector B deben tener el mismo número de filas.")
            return None, None

        return A, B

    def abrir_conversiones(self):
        self.ventana_conversiones = ConversionesWindow(self)
        self.ventana_conversiones.show()
        self.ventana_conversiones.raise_()
        self.ventana_conversiones.activateWindow()

    def volver(self):
        self.close()

    def closeEvent(self, event):
        if self.ventana_principal is not None:
            self.ventana_principal.show()
        event.accept()