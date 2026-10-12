import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
    QTextEdit, QComboBox, QScrollArea, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from core.operaciones import MatrizModel
from ui.conversiones_window import ConversionesWindow

COLOR_FONDO_APP = "#F4F8FB"
COLOR_TARJETA_BG = "#FFFFFF"
COLOR_TEXTO_MAIN = "#031E36"
COLOR_AZUL_PRIMARIO = "#04335A"
COLOR_AZUL_MEDIO = "#4474A3"
COLOR_CELESTE_HIELO = "#9ABCE0"
COLOR_AZUL_CLARO = "#C4D4E6"


class TarjetaMatriz(QFrame):
    """Tarjeta de Matriz con controles inline ‹ / › para Filas y Columnas."""
    def __init__(self, numero, tabla, parent=None):
        super().__init__(parent)
        self.numero = numero
        self.tabla = tabla
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(f"""
            TarjetaMatriz {{
                background-color: {COLOR_TARJETA_BG};
                border-radius: 20px;
                border: 1px solid {COLOR_AZUL_CLARO};
            }}
        """)

        sombra = QGraphicsDropShadowEffect(self)
        sombra.setBlurRadius(25)
        sombra.setColor(QColor(3, 30, 54, 20))
        sombra.setYOffset(6)
        self.setGraphicsEffect(sombra)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(12)

        header = QHBoxLayout()
        header.setSpacing(6)

        self.lbl_titulo = QLabel(f"Matriz {self.numero}", self)
        self.lbl_titulo.setStyleSheet(f"""
            color: {COLOR_TEXTO_MAIN};
            font-size: 16px;
            font-weight: 800;
            font-family: 'Segoe UI', sans-serif;
            border: none;
        """)

        # Control Stepper Filas con flechas modernas
        lbl_f = QLabel("F:", self)
        lbl_f.setStyleSheet(f"color: {COLOR_AZUL_MEDIO}; font-size: 12px; font-weight: 800; border: none;")

        btn_f_menos = QPushButton("‹", self)
        btn_f_menos.setFixedSize(24, 24)
        btn_f_menos.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_f_menos.clicked.connect(lambda: self.spin_filas.setValue(self.spin_filas.value() - 1))

        self.spin_filas = QSpinBox(self)
        self.spin_filas.setRange(1, 15)
        self.spin_filas.setValue(self.tabla.rowCount())
        self.spin_filas.setFixedSize(32, 26)

        btn_f_mas = QPushButton("›", self)
        btn_f_mas.setFixedSize(24, 24)
        btn_f_mas.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_f_mas.clicked.connect(lambda: self.spin_filas.setValue(self.spin_filas.value() + 1))

        # Control Stepper Columnas
        lbl_c = QLabel("C:", self)
        lbl_c.setStyleSheet(f"color: {COLOR_AZUL_MEDIO}; font-size: 12px; font-weight: 800; border: none;")

        btn_c_menos = QPushButton("‹", self)
        btn_c_menos.setFixedSize(24, 24)
        btn_c_menos.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_c_menos.clicked.connect(lambda: self.spin_cols.setValue(self.spin_cols.value() - 1))

        self.spin_cols = QSpinBox(self)
        self.spin_cols.setRange(1, 15)
        self.spin_cols.setValue(self.tabla.columnCount())
        self.spin_cols.setFixedSize(32, 26)

        btn_c_mas = QPushButton("›", self)
        btn_c_mas.setFixedSize(24, 24)
        btn_c_mas.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_c_mas.clicked.connect(lambda: self.spin_cols.setValue(self.spin_cols.value() + 1))

        style_mini_btn = f"""
            QPushButton {{
                background-color: #F0F4F8;
                color: {COLOR_AZUL_PRIMARIO};
                font-size: 15px;
                font-weight: 900;
                border-radius: 6px;
                border: 1px solid {COLOR_AZUL_CLARO};
            }}
            QPushButton:hover {{
                background-color: {COLOR_AZUL_CLARO};
                color: {COLOR_AZUL_PRIMARIO};
            }}
        """
        btn_f_menos.setStyleSheet(style_mini_btn)
        btn_f_mas.setStyleSheet(style_mini_btn)
        btn_c_menos.setStyleSheet(style_mini_btn)
        btn_c_mas.setStyleSheet(style_mini_btn)

        style_spin = f"""
            QSpinBox {{
                background-color: #F8FAFC;
                border: 1px solid {COLOR_AZUL_CLARO};
                border-radius: 6px;
                color: {COLOR_TEXTO_MAIN};
                font-size: 12px;
                font-weight: 800;
            }}
            QSpinBox::up-button, QSpinBox::down-button {{ width: 0px; }}
        """
        self.spin_filas.setStyleSheet(style_spin)
        self.spin_cols.setStyleSheet(style_spin)

        self.spin_filas.valueChanged.connect(self.actualizar_dimensiones)
        self.spin_cols.valueChanged.connect(self.actualizar_dimensiones)

        header.addWidget(self.lbl_titulo)
        header.addStretch()
        header.addWidget(lbl_f)
        header.addWidget(btn_f_menos)
        header.addWidget(self.spin_filas)
        header.addWidget(btn_f_mas)
        header.addSpacing(6)
        header.addWidget(lbl_c)
        header.addWidget(btn_c_menos)
        header.addWidget(self.spin_cols)
        header.addWidget(btn_c_mas)

        self.tabla.setStyleSheet(f"""
            QTableWidget {{
                background-color: #FAFCFE;
                border: 1px solid {COLOR_AZUL_CLARO};
                border-radius: 12px;
                gridline-color: #E2E8F0;
                color: {COLOR_TEXTO_MAIN};
                font-weight: 600;
            }}
            QTableWidget::item {{
                border-radius: 4px;
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
        """)

        layout.addLayout(header)
        layout.addWidget(self.tabla)

    def actualizar_dimensiones(self):
        f = self.spin_filas.value()
        c = self.spin_cols.value()
        self.tabla.setRowCount(f)
        self.tabla.setColumnCount(c)

    def actualizar_titulo(self, nuevo_numero):
        self.numero = nuevo_numero
        self.lbl_titulo.setText(f"Matriz {self.numero}")


class CalculadoraMatrices(QWidget):
    def __init__(self, ventana_principal=None):
        super().__init__()

        self.ventana_principal = ventana_principal
        self.setWindowTitle("BelugaCalc - Básica")
        self.resize(1100, 800)

        self.tablas = []
        self.operadores = []
        self.tarjetas = []
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(f"background-color: {COLOR_FONDO_APP};")

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(24, 20, 24, 20)
        layout_principal.setSpacing(16)

        titulo = QLabel("Calculadora Básica", self)
        titulo.setStyleSheet(f"""
            color: {COLOR_TEXTO_MAIN};
            font-size: 26px;
            font-weight: 900;
            font-family: 'Segoe UI', sans-serif;
        """)
        layout_principal.addWidget(titulo)

        controles = QHBoxLayout()

        lbl_cant = QLabel("Matrices:", self)
        lbl_cant.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 13px; font-weight: 700;")

        btn_menos = QPushButton("‹", self)
        btn_menos.setFixedSize(36, 36)
        btn_menos.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_menos.clicked.connect(self.quitar_matriz_stepper)

        self.spin_cant = QSpinBox(self)
        self.spin_cant.setRange(1, 10)
        self.spin_cant.setValue(2)
        self.spin_cant.setFixedHeight(36)
        self.spin_cant.valueChanged.connect(self.sincronizar_cantidad_matrices)

        btn_mas = QPushButton("›", self)
        btn_mas.setFixedSize(36, 36)
        btn_mas.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_mas.clicked.connect(self.agregar_matriz_stepper)

        style_btn_step = f"""
            QPushButton {{
                background-color: #FFFFFF;
                color: {COLOR_AZUL_PRIMARIO};
                font-size: 20px;
                font-weight: 900;
                border-radius: 10px;
                border: 1px solid {COLOR_AZUL_CLARO};
            }}
            QPushButton:hover {{
                background-color: {COLOR_AZUL_CLARO};
            }}
        """
        btn_menos.setStyleSheet(style_btn_step)
        btn_mas.setStyleSheet(style_btn_step)

        self.spin_cant.setStyleSheet(f"""
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

        btn_ejecutar = QPushButton("Ejecutar operación", self)
        btn_ejecutar.setFixedHeight(38)
        btn_ejecutar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_ejecutar.setStyleSheet(f"""
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
        btn_ejecutar.clicked.connect(self.ejecutar_expresion)

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
            QPushButton:hover {{
                background-color: #F0F9FF;
            }}
        """)
        btn_conversiones.clicked.connect(self.abrir_conversiones)

        btn_volver = QPushButton("Volver", self)
        btn_volver.setFixedHeight(38)
        btn_volver.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #64748B;
                font-size: 13px;
                font-weight: 700;
                border-radius: 12px;
                border: 1.5px solid #E2E8F0;
                padding: 0px 16px;
            }
            QPushButton:hover {
                color: #04335A;
                border-color: #C4D4E6;
            }
        """)
        btn_volver.clicked.connect(self.volver)

        controles.addWidget(lbl_cant)
        controles.addWidget(btn_menos)
        controles.addWidget(self.spin_cant)
        controles.addWidget(btn_mas)
        controles.addSpacing(16)
        controles.addWidget(btn_ejecutar)
        controles.addWidget(btn_limpiar)
        controles.addWidget(btn_conversiones)
        controles.addWidget(btn_volver)
        controles.addStretch()

        layout_principal.addLayout(controles)

        # Scroll Area moderno
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:horizontal {
                border: none;
                background: #E2E8F0;
                height: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:horizontal {
                background: #9ABCE0;
                border-radius: 5px;
                min-width: 30px;
            }
        """)

        self.contenedor_matrices = QWidget()
        self.matrices_layout = QHBoxLayout(self.contenedor_matrices)
        self.matrices_layout.setContentsMargins(0, 8, 0, 8)
        self.matrices_layout.setSpacing(16)
        self.matrices_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.scroll_area.setWidget(self.contenedor_matrices)
        layout_principal.addWidget(self.scroll_area, 3)

        # SECCIÓN DE RESULTADO Y PROCEDIMIENTO
        layout_resultados = QHBoxLayout()

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
        lay_r.setSpacing(10)

        lbl_r_title = QLabel("Resultado:", box_res)
        lbl_r_title.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 14px; font-weight: 800; border: none;")

        self.tabla_res = QTableWidget()
        self.tabla_res.setStyleSheet(f"""
            QTableWidget {{
                background-color: #FAFCFE;
                border: 1px solid {COLOR_AZUL_CLARO};
                border-radius: 10px;
                gridline-color: #E2E8F0;
                color: {COLOR_TEXTO_MAIN};
                font-weight: 600;
            }}
            QHeaderView::section {{
                background-color: {COLOR_AZUL_CLARO};
                color: {COLOR_AZUL_PRIMARIO};
                font-weight: 700;
                border: none;
            }}
        """)

        # NUEVA CAJITA DE EXPRESIÓN DE RESULTADO ABAJO DE LA TABLA
        self.lbl_expresion_res = QLabel("Expresión de Resultado:\n—", box_res)
        self.lbl_expresion_res.setStyleSheet(f"""
            QLabel {{
                background-color: #F8FAFC;
                color: {COLOR_TEXTO_MAIN};
                font-size: 13px;
                font-weight: 700;
                border: 1px solid {COLOR_AZUL_CLARO};
                border-radius: 10px;
                padding: 10px;
            }}
        """)

        lay_r.addWidget(lbl_r_title)
        lay_r.addWidget(self.tabla_res)
        lay_r.addWidget(self.lbl_expresion_res)

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

        self.txt_bitacora = QTextEdit()
        self.txt_bitacora.setReadOnly(True)
        self.txt_bitacora.setStyleSheet("""
            QTextEdit {
                border: none;
                background: transparent;
                font-size: 13px;
                color: #1E293B;
            }
        """)

        lay_p.addWidget(lbl_p_title)
        lay_p.addWidget(self.txt_bitacora)

        layout_resultados.addWidget(box_res, 1)
        layout_resultados.addWidget(box_proc, 1)

        layout_principal.addLayout(layout_resultados, 2)

        self.agregar_matriz()
        self.agregar_matriz()

    def agregar_matriz_stepper(self):
        val = self.spin_cant.value()
        if val < 10:
            self.spin_cant.setValue(val + 1)

    def quitar_matriz_stepper(self):
        val = self.spin_cant.value()
        if val > 1:
            self.spin_cant.setValue(val - 1)

    def sincronizar_cantidad_matrices(self, cantidad_deseada):
        mientras_suba = len(self.tablas)
        if cantidad_deseada > mientras_suba:
            for _ in range(cantidad_deseada - mientras_suba):
                self.agregar_matriz()
        elif cantidad_deseada < mientras_suba:
            for _ in range(mientras_suba - cantidad_deseada):
                self.eliminar_matriz(len(self.tablas) - 1)

    def agregar_matriz(self):
        numero = len(self.tablas) + 1
        filas, columnas = 3, 3

        if self.tablas:
            operador = QComboBox()
            operador.addItems(["+", "-", "*"])
            operador.setCurrentText("+")
            operador.setFixedSize(54, 36)
            operador.setCursor(Qt.CursorShape.PointingHandCursor)
            operador.setStyleSheet(f"""
                QComboBox {{
                    background-color: {COLOR_AZUL_CLARO};
                    color: {COLOR_AZUL_PRIMARIO};
                    font-weight: 900;
                    font-size: 16px;
                    border-radius: 10px;
                    padding-left: 12px;
                }}
                QComboBox::drop-down {{
                    border: none;
                }}
            """)
            self.matrices_layout.addWidget(operador)
            self.operadores.append(operador)

        tabla = QTableWidget(filas, columnas)
        tabla.setMinimumWidth(300)
        tabla.setMinimumHeight(180)

        self.tablas.append(tabla)

        tarjeta = TarjetaMatriz(numero, tabla, self.contenedor_matrices)
        tarjeta.setFixedWidth(340)

        self.tarjetas.append(tarjeta)
        self.matrices_layout.addWidget(tarjeta)
        
        if len(self.tablas) != self.spin_cant.value():
            self.spin_cant.blockSignals(True)
            self.spin_cant.setValue(len(self.tablas))
            self.spin_cant.blockSignals(False)

    def eliminar_matriz(self, indice):
        if indice < 0 or indice >= len(self.tablas):
            return

        if len(self.tablas) <= 1:
            return

        operador_indice = 0 if indice == 0 else indice - 1
        if self.operadores:
            operador = self.operadores.pop(operador_indice)
            self.matrices_layout.removeWidget(operador)
            operador.deleteLater()

        tabla = self.tablas.pop(indice)
        tarjeta = self.tarjetas.pop(indice)

        self.matrices_layout.removeWidget(tarjeta)
        tarjeta.deleteLater()
        tabla.deleteLater()

        for num, t_actual in enumerate(self.tarjetas, start=1):
            t_actual.actualizar_titulo(num)

        if len(self.tablas) != self.spin_cant.value():
            self.spin_cant.blockSignals(True)
            self.spin_cant.setValue(len(self.tablas))
            self.spin_cant.blockSignals(False)

        self.txt_bitacora.clear()
        self.lbl_expresion_res.setText("Expresión de Resultado:\n—")
        self.tabla_res.clearContents()
        self.tabla_res.setRowCount(0)
        self.tabla_res.setColumnCount(0)

    def limpiar_tablas(self):
        for tabla in self.tablas + [self.tabla_res]:
            tabla.clearContents()
        self.txt_bitacora.clear()
        self.lbl_expresion_res.setText("Expresión de Resultado:\n—")

    def leer_matriz(self, tabla):
        matriz = []
        for i in range(tabla.rowCount()):
            fila = []
            for j in range(tabla.columnCount()):
                item = tabla.item(i, j)
                texto = item.text().strip() if item else ""
                fila.append(float(texto) if texto else 0.0)
            matriz.append(fila)
        return matriz

    def mostrar_resultado(self, matriz_res):
        self.tabla_res.clear()

        if isinstance(matriz_res, str):
            self.tabla_res.setRowCount(1)
            self.tabla_res.setColumnCount(1)
            self.tabla_res.setItem(0, 0, QTableWidgetItem(matriz_res))
            return

        if not matriz_res:
            self.tabla_res.setRowCount(0)
            self.tabla_res.setColumnCount(0)
            return

        filas = len(matriz_res)
        columnas = len(matriz_res[0])
        self.tabla_res.setRowCount(filas)
        self.tabla_res.setColumnCount(columnas)

        for i in range(filas):
            for j in range(columnas):
                valor = matriz_res[i][j]
                if isinstance(valor, float) and valor.is_integer():
                    texto = str(int(valor))
                else:
                    texto = str(round(float(valor), 4))
                self.tabla_res.setItem(i, j, QTableWidgetItem(texto))

    def validar_dimensiones(self, izquierda, derecha, operador):
        filas_i, columnas_i = len(izquierda), len(izquierda[0])
        filas_d, columnas_d = len(derecha), len(derecha[0])

        if operador in ("+", "-"):
            if filas_i != filas_d or columnas_i != columnas_d:
                raise ValueError(
                    "Las matrices deben tener dimensiones idénticas "
                    f"para usar {operador}."
                )
        elif operador == "*" and columnas_i != filas_d:
            raise ValueError(
                "Dimensiones incompatibles para multiplicar: "
                f"({filas_i}x{columnas_i}) * ({filas_d}x{columnas_d})."
            )

    def realizar_operacion(self, izquierda, derecha, operador):
        self.validar_dimensiones(izquierda, derecha, operador)

        if operador == "+":
            return MatrizModel.sumar([izquierda, derecha])
        if operador == "-":
            return MatrizModel.restar([izquierda, derecha])
        return MatrizModel.multiplicar([izquierda, derecha])

    def matriz_a_html(self, matriz, titulo=""):
        html = []
        if titulo:
            html.append(f"<div style='color: #0284C7; font-weight: bold; margin-top: 8px; font-size: 13px;'>{titulo}:</div>")
        
        html.append("<pre style=\"font-family: 'Consolas', 'Courier New', monospace; font-size: 13px; color: #04335A; margin: 4px 0;\">")
        
        anchos = []
        for j in range(len(matriz[0])):
            max_len = 0
            for i in range(len(matriz)):
                val = matriz[i][j]
                txt = f"{int(val)}" if isinstance(val, float) and val.is_integer() else f"{val:.2f}"
                max_len = max(max_len, len(txt))
            anchos.append(max_len)

        for fila in matriz:
            elementos = []
            for j, val in enumerate(fila):
                txt = f"{int(val)}" if isinstance(val, float) and val.is_integer() else f"{val:.2f}"
                elementos.append(txt.rjust(anchos[j]))
            contenido = "   ".join(elementos)
            html.append(f"[  {contenido}  ]")
            
        html.append("</pre>")
        return "".join(html)

    def generar_pasos_operacion_html(self, izquierda, derecha, resultado, operador, texto_izq, texto_der):
        html = []
        html.append(f"<div style='background-color: #E0F2FE; color: #04335A; padding: 6px 12px; border-radius: 8px; font-weight: bold; margin-top: 10px;'>=== {texto_izq} {operador} {texto_der} ===</div>")

        if operador == "+":
            html.append("<p style='color: #64748B; margin: 4px 0;'>Se suman las entradas que ocupan la misma posición.</p>")
        elif operador == "-":
            html.append("<p style='color: #64748B; margin: 4px 0;'>Se restan las entradas que ocupan la misma posición.</p>")
        else:
            html.append("<p style='color: #64748B; margin: 4px 0;'>Cada entrada se obtiene mediante producto fila por columna:</p>")
            html.append("<pre style=\"font-family: 'Consolas', monospace; font-size: 12px; color: #334155;\">")
            for i in range(len(izquierda)):
                for j in range(len(derecha[0])):
                    terminos = []
                    for k in range(len(izquierda[0])):
                        terminos.append(f"({izquierda[i][k]})({derecha[k][j]})")
                    html.append(f"Resultado[{i + 1},{j + 1}] = " + " + ".join(terminos) + f" = {resultado[i][j]}")
            html.append("</pre>")

        html.append(self.matriz_a_html(izquierda, texto_izq))
        html.append(self.matriz_a_html(derecha, texto_der))
        html.append(self.matriz_a_html(resultado, "Resultado parcial"))
        return "".join(html)

    def ejecutar_expresion(self):
        try:
            matrices = [self.leer_matriz(tabla) for tabla in self.tablas]
            operadores = [combo.currentText() for combo in self.operadores]

            if len(matrices) < 2:
                raise ValueError("Se necesitan al menos dos matrices.")

            valores = list(matrices)
            ops = list(operadores)
            nombres = [f"Matriz {i + 1}" for i in range(len(matrices))]

            html_pasos = []
            html_pasos.append("<div style='background-color: #04335A; color: #FFFFFF; padding: 8px 12px; border-radius: 10px; font-weight: bold;'>EVALUACIÓN DE LA EXPRESIÓN</div>")
            
            expr_str = " ".join(item for par in zip(nombres, ops + [""]) for item in par if item)
            html_pasos.append(f"<p style='color: #031E36; font-weight: bold; margin: 8px 0 2px 0;'>Expresión: <span style='color: #0284C7;'>{expr_str}</span></p>")
            html_pasos.append("<p style='color: #64748B; font-size: 11px; margin-bottom: 10px;'><i>Nota: La multiplicación (*) tiene prioridad sobre (+) y (-).</i></p>")

            while "*" in ops:
                indice = ops.index("*")
                izq = valores[indice]
                der = valores[indice + 1]
                res = self.realizar_operacion(izq, der, "*")
                html_pasos.append(self.generar_pasos_operacion_html(izq, der, res, "*", nombres[indice], nombres[indice + 1]))
                valores[indice:indice + 2] = [res]
                nombre_res = f"({nombres[indice]} * {nombres[indice + 1]})"
                nombres[indice:indice + 2] = [nombre_res]
                ops.pop(indice)

            while ops:
                op = ops.pop(0)
                izq = valores.pop(0)
                der = valores.pop(0)
                nom_izq = nombres.pop(0)
                nom_der = nombres.pop(0)
                res = self.realizar_operacion(izq, der, op)
                html_pasos.append(self.generar_pasos_operacion_html(izq, der, res, op, nom_izq, nom_der))
                valores.insert(0, res)
                nombres.insert(0, f"({nom_izq} {op} {nom_der})")

            html_pasos.append("<div style='background-color: #0284C7; color: #FFFFFF; padding: 6px 12px; border-radius: 8px; font-weight: bold; margin-top: 14px;'>RESULTADO FINAL</div>")
            html_pasos.append(self.matriz_a_html(valores[0]))

            resultado_final = valores[0]
            self.mostrar_resultado(resultado_final)
            
            # ACTUALIZAR LA ETIQUETA DE EXPRESIÓN DE RESULTADO ABAJO DE LA TABLA
            self.lbl_expresion_res.setText(f"Expresión de Resultado:\n{expr_str}")

            self.txt_bitacora.setHtml("".join(html_pasos))
            self.txt_bitacora.verticalScrollBar().setValue(0)

        except ValueError as error:
            QMessageBox.warning(self, "Error", str(error))
        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"Ocurrió un error inesperado: {error}"
            )

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