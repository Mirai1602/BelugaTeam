# ui/inversa_window.py

import os
from fractions import Fraction
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
    QTextEdit, QComboBox, QFrame, QGraphicsDropShadowEffect, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from core.inversa import MatrizInversa


# PALETA DE COLORES AZUL GLACIAL / ÁRTICO
COLOR_FONDO_APP = "#F4F8FB"
COLOR_TARJETA_BG = "#FFFFFF"
COLOR_TEXTO_MAIN = "#031E36"
COLOR_AZUL_PRIMARIO = "#04335A"
COLOR_AZUL_MEDIO = "#4474A3"
COLOR_CELESTE_HIELO = "#9ABCE0"
COLOR_AZUL_CLARO = "#C4D4E6"


class InversaWindow(QWidget):
    """Interfaz Dashboard para el módulo de matrices inversas."""

    def __init__(self, ventana_principal=None):
        super().__init__(ventana_principal)
        self.ventana_principal = ventana_principal
        self.setWindowTitle("BelugaCalc - Matrices Inversas")
        self.resize(1100, 800)
        self.init_ui()
        self.generar_matriz()

    def init_ui(self):
        self.setStyleSheet(f"background-color: {COLOR_FONDO_APP};")

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(24, 20, 24, 20)
        layout_principal.setSpacing(16)

        # 1. TÍTULO DE CABECERA
        titulo = QLabel("Matrices Inversas", self)
        titulo.setStyleSheet(f"""
            color: {COLOR_TEXTO_MAIN};
            font-size: 26px;
            font-weight: 900;
            font-family: 'Segoe UI', sans-serif;
        """)
        layout_principal.addWidget(titulo)

        # 2. BARRA DE CONTROLES SUPERIORES (STEPPERS + / -)
        controles = QHBoxLayout()

        # Filas Stepper
        lbl_f = QLabel("Filas:", self)
        lbl_f.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 13px; font-weight: 700;")

        btn_f_menos = QPushButton("−", self)
        btn_f_menos.setFixedSize(36, 36)
        btn_f_menos.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_f_menos.clicked.connect(lambda: self.spin_filas.setValue(self.spin_filas.value() - 1))

        self.spin_filas = QSpinBox(self)
        self.spin_filas.setRange(1, 15)
        self.spin_filas.setValue(3)
        self.spin_filas.setFixedHeight(36)
        self.spin_filas.valueChanged.connect(self.generar_matriz)

        btn_f_mas = QPushButton("+", self)
        btn_f_mas.setFixedSize(36, 36)
        btn_f_mas.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_f_mas.clicked.connect(lambda: self.spin_filas.setValue(self.spin_filas.value() + 1))

        # Columnas Stepper
        lbl_c = QLabel("Columnas:", self)
        lbl_c.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 13px; font-weight: 700;")

        btn_c_menos = QPushButton("−", self)
        btn_c_menos.setFixedSize(36, 36)
        btn_c_menos.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_c_menos.clicked.connect(lambda: self.spin_columnas.setValue(self.spin_columnas.value() - 1))

        self.spin_columnas = QSpinBox(self)
        self.spin_columnas.setRange(1, 15)
        self.spin_columnas.setValue(3)
        self.spin_columnas.setFixedHeight(36)
        self.spin_columnas.valueChanged.connect(self.generar_matriz)

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

        # Operación
        lbl_op = QLabel("Operación:", self)
        lbl_op.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 13px; font-weight: 700;")

        self.combo_operacion = QComboBox(self)
        self.combo_operacion.addItems([
            "Matriz inversa",
            "Matriz inversa de una matriz inversa",
        ])
        self.combo_operacion.setFixedHeight(36)
        self.combo_operacion.setStyleSheet(f"""
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

        # Botón Calcular
        btn_calcular = QPushButton("Calcular inversa", self)
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
        btn_calcular.clicked.connect(self.calcular)

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
        btn_limpiar.clicked.connect(self.limpiar)

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
        controles.addWidget(lbl_op)
        controles.addWidget(self.combo_operacion)
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
                padding: 4px;
            }}
        """

        # 3. TARJETA ELEVADA MATRIZ A
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

        lbl_m_title = QLabel("Matriz A", card_matriz)
        lbl_m_title.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 15px; font-weight: 800; border: none;")

        self.tabla_matriz = QTableWidget(card_matriz)
        self.tabla_matriz.setStyleSheet(style_tabla)

        card_layout.addWidget(lbl_m_title)
        card_layout.addWidget(self.tabla_matriz)

        layout_principal.addWidget(card_matriz, 3)

        # 4. RESULTADO Y PROCEDIMIENTO EN DOS TARJETAS PARALELAS
        layout_resultados = QHBoxLayout()

        # Cuadro Resultado
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

        lbl_r_title = QLabel("Matriz Inversa Resultante (A⁻¹):", box_res)
        lbl_r_title.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 14px; font-weight: 800; border: none;")

        self.tabla_resultado = QTableWidget(box_res)
        self.tabla_resultado.setStyleSheet(style_tabla)

        # ETIQUETA INFERIOR CON LA SOLUCIÓN EXPLÍCITA COMO ECUACIÓN Y VECTOR
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

        # Cuadro Procedimiento
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

        lbl_p_title = QLabel("Validaciones y procedimiento:", box_proc)
        lbl_p_title.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 14px; font-weight: 800; border: none;")

        self.txt_bitacora = QTextEdit(box_proc)
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

    def generar_matriz(self):
        filas = self.spin_filas.value()
        columnas = self.spin_columnas.value()
        self.tabla_matriz.setRowCount(filas)
        self.tabla_matriz.setColumnCount(columnas)

        for i in range(filas):
            for j in range(columnas):
                if self.tabla_matriz.item(i, j) is None:
                    item = QTableWidgetItem("0")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.tabla_matriz.setItem(i, j, item)

        self.limpiar_resultados()

    def limpiar_resultados(self):
        self.tabla_resultado.clear()
        self.tabla_resultado.setRowCount(0)
        self.tabla_resultado.setColumnCount(0)
        self.lbl_res_texto.setText("")
        self.txt_bitacora.clear()

    def limpiar(self):
        for i in range(self.tabla_matriz.rowCount()):
            for j in range(self.tabla_matriz.columnCount()):
                item = self.tabla_matriz.item(i, j)
                if item:
                    item.setText("0")
        self.limpiar_resultados()

    def leer_matriz(self):
        matriz = []
        for i in range(self.tabla_matriz.rowCount()):
            fila = []
            for j in range(self.tabla_matriz.columnCount()):
                item = self.tabla_matriz.item(i, j)
                texto = item.text().strip() if item else "0"
                if texto == "":
                    texto = "0"
                try:
                    fila.append(MatrizInversa.a_fraction(texto))
                except (ValueError, ZeroDivisionError):
                    raise ValueError(f"El valor de la posición ({i + 1}, {j + 1}) no es válido: {texto}")
            matriz.append(fila)
        return matriz

    def mostrar_resultado_doble(self, matriz, operacion=""):
        """Renderiza el resultado en la tabla Y muestra la ecuación explícita por elementos."""
        filas = len(matriz)
        columnas = len(matriz[0]) if matriz else 0
        self.tabla_resultado.setRowCount(filas)
        self.tabla_resultado.setColumnCount(columnas)

        headers = [f"c{j+1}" for j in range(columnas)]
        self.tabla_resultado.setHorizontalHeaderLabels(headers)

        elementos_ecuaciones = []
        filas_representacion = []

        for i in range(filas):
            self.tabla_resultado.setVerticalHeaderItem(i, QTableWidgetItem(f"f{i+1}"))
            elementos_fila = []
            for j in range(columnas):
                val_txt = MatrizInversa.formato_valor(matriz[i][j])
                item = QTableWidgetItem(val_txt)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_resultado.setItem(i, j, item)

                elementos_ecuaciones.append(f"a⁻¹({i+1},{j+1}) = {val_txt}")
                elementos_fila.append(val_txt)

            filas_representacion.append("[" + "  ".join(elementos_fila) + "]")

        self.tabla_resultado.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # GENERACIÓN DEL TEXTO DE SOLUCIÓN EXPLÍCITA COMO ECUACIÓN Y MATRIZ
        str_ecuaciones = ", ".join(elementos_ecuaciones[:6])  # Mostrar primeros elementos si es grande
        if len(elementos_ecuaciones) > 6:
            str_ecuaciones += ", ..."

        str_matriz = " | ".join(filas_representacion)

        self.lbl_res_texto.setText(
            f"<b>Ecuación de Elementos:</b><br>{str_ecuaciones}<br><br>"
            f"<b>Expresión Matricial (A⁻¹):</b><br>{str_matriz}"
        )

    def formatear_reporte_html(self, operacion, respuesta):
        """Genera una salida ordenada verticalmente en HTML."""
        html = []
        html.append(f"<div style='background-color: #04335A; color: #FFFFFF; padding: 6px 12px; border-radius: 8px; font-weight: bold;'>MÓDULO DE MATRICES INVERSAS</div>")
        html.append(f"<p style='color: #031E36; font-weight: bold; margin: 8px 0 2px 0;'>Operación: <span style='color: #0284C7;'>{operacion}</span></p>")
        html.append(f"<p style='color: #475569; font-size: 12px; margin-bottom: 8px;'><b>Método utilizado:</b> {respuesta['metodo']}</p>")

        html.append("<div style='background-color: #E0F2FE; color: #04335A; padding: 6px 12px; border-radius: 8px; font-weight: bold; margin-top: 8px; margin-bottom: 6px;'>VALIDACIONES</div>")
        html.append(f"<p style='color: #334155; margin: 4px 0;'>{respuesta['validaciones']}</p>")

        html.append("<div style='background-color: #0284C7; color: #FFFFFF; padding: 6px 12px; border-radius: 8px; font-weight: bold; margin-top: 10px; margin-bottom: 6px;'>PROCEDIMIENTO PASO A PASO</div>")
        
        # Bloque preformateado en fuente monospaced para matrices aumentadas
        html.append("<pre style=\"font-family: 'Consolas', 'Courier New', monospace; font-size: 12.5px; color: #04335A; margin: 4px 0; white-space: pre-wrap;\">")
        html.append(str(respuesta['pasos']))
        html.append("</pre>")

        return "".join(html)

    def calcular(self):
        try:
            matriz = self.leer_matriz()
            operacion = self.combo_operacion.currentText()
            respuesta = MatrizInversa.inversa(matriz, operacion)

            # Mostrar resultado doble (tabla + etiqueta inferior)
            self.mostrar_resultado_doble(respuesta["resultado"], operacion)
            
            # Formatear el procedimiento a HTML ordenado
            html_reporte = self.formatear_reporte_html(operacion, respuesta)
            self.txt_bitacora.setHtml(html_reporte)

        except Exception as e:
            self.limpiar_resultados()
            self.txt_bitacora.setHtml(f"<div style='color: #EF4444; font-weight: bold; padding: 8px;'>ERROR DE VALIDACIÓN:</div><p style='color: #B91C1C;'>{e}</p>")
            QMessageBox.warning(self, "Matriz inversa", str(e))