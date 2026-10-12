from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem, QTextEdit, QMessageBox, QFrame,
    QGraphicsDropShadowEffect, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from core.operaciones import MatrizModel


# PALETA DE COLORES AZUL GLACIAL / ÁRTICO
COLOR_FONDO_APP = "#F4F8FB"
COLOR_TARJETA_BG = "#FFFFFF"
COLOR_TEXTO_MAIN = "#031E36"
COLOR_AZUL_PRIMARIO = "#04335A"
COLOR_AZUL_MEDIO = "#4474A3"
COLOR_CELESTE_HIELO = "#9ABCE0"
COLOR_AZUL_CLARO = "#C4D4E6"


class EcuacionesWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWindowTitle("BelugaCalc - Ecuaciones Matriciales")
        self.resize(1100, 800)
        self.setup_ui()
        self.generar_tablas()

    def setup_ui(self):
        self.setStyleSheet(f"background-color: {COLOR_FONDO_APP};")

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(24, 20, 24, 20)
        layout_principal.setSpacing(16)

        # 1. TÍTULO DE CABECERA
        titulo = QLabel("Ecuaciones matriciales: AX = B", self)
        titulo.setStyleSheet(f"""
            color: {COLOR_TEXTO_MAIN};
            font-size: 26px;
            font-weight: 900;
            font-family: 'Segoe UI', sans-serif;
        """)
        layout_principal.addWidget(titulo)

        # 2. BARRA DE CONTROLES SUPERIORES (STEPPERS + / -)
        controles = QHBoxLayout()

        # Stepper Ecuaciones
        lbl_f = QLabel("Ecuaciones:", self)
        lbl_f.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 13px; font-weight: 700;")

        btn_f_menos = QPushButton("−", self)
        btn_f_menos.setFixedSize(36, 36)
        btn_f_menos.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_f_menos.clicked.connect(lambda: self.spin_filas.setValue(self.spin_filas.value() - 1))

        self.spin_filas = QSpinBox(self)
        self.spin_filas.setRange(1, 15)
        self.spin_filas.setValue(2)
        self.spin_filas.setFixedHeight(36)
        self.spin_filas.valueChanged.connect(self.generar_tablas)

        btn_f_mas = QPushButton("+", self)
        btn_f_mas.setFixedSize(36, 36)
        btn_f_mas.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_f_mas.clicked.connect(lambda: self.spin_filas.setValue(self.spin_filas.value() + 1))

        # Stepper Variables
        lbl_c = QLabel("Variables:", self)
        lbl_c.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 13px; font-weight: 700;")

        btn_c_menos = QPushButton("−", self)
        btn_c_menos.setFixedSize(36, 36)
        btn_c_menos.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_c_menos.clicked.connect(lambda: self.spin_columnas.setValue(self.spin_columnas.value() - 1))

        self.spin_columnas = QSpinBox(self)
        self.spin_columnas.setRange(1, 15)
        self.spin_columnas.setValue(2)
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

        # Botones Limpiar y Volver
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
        btn_limpiar.clicked.connect(self.limpiar)

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
        btn_volver.clicked.connect(self.close)

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
        controles.addWidget(btn_volver)
        controles.addStretch()

        layout_principal.addLayout(controles)

        # 3. TABLAS DE MATRICES A Y B EN TARJETAS
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
        lbl_A_title = QLabel("Matriz A (coeficientes)", card_A)
        lbl_A_title.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 15px; font-weight: 800; border: none;")
        self.tabla_a = QTableWidget(card_A)
        self.tabla_a.setStyleSheet(style_tabla)
        lay_A.addWidget(lbl_A_title)
        lay_A.addWidget(self.tabla_a)

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
        lbl_B_title = QLabel("Matriz B (independientes)", card_B)
        lbl_B_title.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 15px; font-weight: 800; border: none;")
        self.tabla_b = QTableWidget(card_B)
        self.tabla_b.setStyleSheet(style_tabla)
        lay_B.addWidget(lbl_B_title)
        lay_B.addWidget(self.tabla_b)

        tablas_layout.addWidget(card_A, 3)
        tablas_layout.addWidget(card_B, 1)

        layout_principal.addLayout(tablas_layout, 3)

        # 4. BOTONES DE MÉTODOS DE RESOLUCIÓN
        botones_layout = QHBoxLayout()
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

        for texto, metodo in (("Resolver con Gauss", self.gauss), ("Resolver con Gauss-Jordan", self.gauss_jordan), ("Reducción de pivotes", self.pivotes)):
            boton = QPushButton(texto, self)
            boton.setStyleSheet(style_btn_metodo)
            boton.setCursor(Qt.CursorShape.PointingHandCursor)
            boton.clicked.connect(metodo)
            botones_layout.addWidget(boton)

        botones_layout.addStretch()
        layout_principal.addLayout(botones_layout)

        # 5. DOS TARJETAS PARALELAS: RESULTADO (MATRICIAL Y TEXTO) Y PROCEDIMIENTO
        layout_resultados = QHBoxLayout()

        # Tarjeta de Resultado Doble
        box_res = QFrame(self)
        box_res.setStyleSheet(f"QFrame {{ background-color: {COLOR_TARJETA_BG}; border-radius: 18px; border: 1px solid {COLOR_AZUL_CLARO}; }}")
        lay_r = QVBoxLayout(box_res)
        lay_r.setContentsMargins(16, 14, 16, 14)

        lbl_r_title = QLabel("Resultado (Vector Solución X):", box_res)
        lbl_r_title.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 14px; font-weight: 800; border: none;")

        self.tabla_resultado = QTableWidget(box_res)
        self.tabla_resultado.setStyleSheet(style_tabla)

        # Representación del resultado en formato vectorial / texto
        self.lbl_resultado_texto = QLabel("Sin resultados", box_res)
        self.lbl_resultado_texto.setWordWrap(True)
        self.lbl_resultado_texto.setStyleSheet(f"""
            QLabel {{
                background-color: #F0F9FF;
                color: {COLOR_AZUL_PRIMARIO};
                font-weight: 700;
                font-size: 12px;
                border-radius: 8px;
                border: 1px solid {COLOR_AZUL_CLARO};
                padding: 6px 10px;
            }}
        """)

        lay_r.addWidget(lbl_r_title)
        lay_r.addWidget(self.tabla_resultado, 1)
        lay_r.addWidget(self.lbl_resultado_texto)

        # Tarjeta de Procedimiento Paso a Paso
        box_proc = QFrame(self)
        box_proc.setStyleSheet(f"QFrame {{ background-color: {COLOR_TARJETA_BG}; border-radius: 18px; border: 1px solid {COLOR_AZUL_CLARO}; }}")
        lay_p = QVBoxLayout(box_proc)
        lay_p.setContentsMargins(16, 14, 16, 14)

        lbl_p_title = QLabel("Procedimiento Paso a Paso:", box_proc)
        lbl_p_title.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 14px; font-weight: 800; border: none;")

        self.bitacora = QTextEdit(box_proc)
        self.bitacora.setReadOnly(True)
        self.bitacora.setStyleSheet("QTextEdit { border: none; background: transparent; font-size: 13px; color: #1E293B; }")

        lay_p.addWidget(lbl_p_title)
        lay_p.addWidget(self.bitacora)

        layout_resultados.addWidget(box_res, 1)
        layout_resultados.addWidget(box_proc, 1)

        layout_principal.addLayout(layout_resultados, 2)

    def generar_tablas(self):
        filas, columnas = self.spin_filas.value(), self.spin_columnas.value()
        self.tabla_a.setRowCount(filas)
        self.tabla_a.setColumnCount(columnas)
        self.tabla_b.setRowCount(filas)
        self.tabla_b.setColumnCount(1)

        self.tabla_a.setHorizontalHeaderLabels([f"x{j+1}" for j in range(columnas)])
        self.tabla_b.setHorizontalHeaderLabels(["b"])

        self.tabla_a.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_b.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for tabla in (self.tabla_a, self.tabla_b):
            for i in range(tabla.rowCount()):
                for j in range(tabla.columnCount()):
                    item = QTableWidgetItem("0")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    tabla.setItem(i, j, item)

        self.limpiar_resultados()

    def limpiar_resultados(self):
        self.tabla_resultado.clear()
        self.tabla_resultado.setRowCount(0)
        self.tabla_resultado.setColumnCount(0)
        self.lbl_resultado_texto.setText("Sin resultados")
        self.bitacora.clear()

    def limpiar(self):
        self.generar_tablas()

    def leer(self, tabla):
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

    def mostrar_resultado_doble(self, solucion, clasificacion):
        """Muestra la solución tanto en formato matricial (tabla) como explícito (texto/vectorial)."""
        self.tabla_resultado.clear()

        if isinstance(solucion, str):
            self.tabla_resultado.setRowCount(1)
            self.tabla_resultado.setColumnCount(1)
            item = QTableWidgetItem(solucion)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabla_resultado.setItem(0, 0, item)
            self.lbl_resultado_texto.setText(f"<b>{clasificacion}</b><br>{solucion}")
            return

        if not solucion:
            self.limpiar_resultados()
            return

        # 1. REPRESENTACIÓN EN TABLA MATRICIAL
        filas = len(solucion)
        cols = 1
        self.tabla_resultado.setRowCount(filas)
        self.tabla_resultado.setColumnCount(cols)
        self.tabla_resultado.setHorizontalHeaderLabels(["Valor"])

        elementos_str = []

        for i in range(filas):
            self.tabla_resultado.setVerticalHeaderItem(i, QTableWidgetItem(f"x{i+1}"))
            val = solucion[i][0] if isinstance(solucion[i], list) else solucion[i]

            if hasattr(val, "numerator"):
                txt = str(val.numerator) if val.denominator == 1 else f"{val.numerator}/{val.denominator}"
            elif isinstance(val, float) and val.is_integer():
                txt = str(int(val))
            else:
                txt = f"{val:.4f}" if isinstance(val, (float, int)) else str(val)

            elementos_str.append(txt)
            item = QTableWidgetItem(txt)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabla_resultado.setItem(i, 0, item)

        self.tabla_resultado.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # 2. REPRESENTACIÓN TEXTUAL / VECTORIAL EXPLÍCITA
        str_vector = ", ".join(f"'{x}'" for x in elementos_str)
        self.lbl_resultado_texto.setText(f"<b>{clasificacion}</b><br>X = [{str_vector}]ᵀ")

    def formatear_pasos_html(self, nombre, pasos, verificacion):
        """Genera bloques HTML para visualizar el procedimiento correctamente."""
        html = []
        html.append(f"<div style='background-color: #04335A; color: #FFFFFF; padding: 8px 12px; border-radius: 10px; font-weight: bold;'>MÉTODO: {nombre}</div>")
        
        html.append("<div style='background-color: #E0F2FE; color: #04335A; padding: 6px 12px; border-radius: 8px; font-weight: bold; margin-top: 10px;'>PROCEDIMIENTO PASO A PASO</div>")
        
        pasos_lineas = str(pasos).split("\n")
        html.append("<pre style=\"font-family: 'Consolas', 'Courier New', monospace; font-size: 12px; color: #04335A; margin: 6px 0;\">")
        for linea in pasos_lineas:
            html.append(linea)
        html.append("</pre>")

        if verificacion:
            html.append("<div style='background-color: #0284C7; color: #FFFFFF; padding: 6px 12px; border-radius: 8px; font-weight: bold; margin-top: 10px;'>VERIFICACIÓN AUTOMÁTICA</div>")
            html.append(f"<p style='color: #334155; font-size: 12px; margin: 4px 0;'>{verificacion}</p>")

        return "".join(html)

    def resolver(self, metodo, nombre):
        try:
            a, b = self.leer(self.tabla_a), self.leer(self.tabla_b)
            pasos, clasificacion, solucion, verificacion = metodo(a, b)

            # Mostrar resultado doble (tabla + etiqueta)
            self.mostrar_resultado_doble(solucion, clasificacion)

            # Procedimiento en HTML
            html_proc = self.formatear_pasos_html(nombre, pasos, verificacion)
            self.bitacora.setHtml(html_proc)

        except Exception as error:
            QMessageBox.warning(self, "Error", str(error))

    def gauss(self):
        self.resolver(MatrizModel.gauss_resolver_completo, "GAUSS")

    def gauss_jordan(self):
        self.resolver(MatrizModel.metodo_gauss_jordan, "GAUSS-JORDAN")

    def pivotes(self):
        self.resolver(MatrizModel.reduccion_pivotes, "REDUCCIÓN DE PIVOTES")

    def closeEvent(self, event):
        if self.parent_window is not None:
            self.parent_window.show()
        event.accept()