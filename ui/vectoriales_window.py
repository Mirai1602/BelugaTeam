from fractions import Fraction

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem, QComboBox, QTextEdit, QMessageBox,
    QGroupBox, QLineEdit, QScrollArea, QWidget, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from core.vectoriales import VectorModel

COLOR_FONDO_APP = "#F4F8FB"
COLOR_TARJETA_BG = "#FFFFFF"
COLOR_TEXTO_MAIN = "#031E36"
COLOR_AZUL_PRIMARIO = "#04335A"
COLOR_AZUL_MEDIO = "#4474A3"
COLOR_CELESTE_HIELO = "#9ABCE0"
COLOR_AZUL_CLARO = "#C4D4E6"


class VectorialesWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.tablas_vectores = []
        self.setWindowTitle("BelugaCalc - Módulo de Vectores")
        self.resize(1150, 820)
        self.setup_ui()
        self.generar_vectores()

    def setup_ui(self):
        self.setStyleSheet(f"background-color: {COLOR_FONDO_APP};")
        principal = QVBoxLayout(self)
        principal.setContentsMargins(28, 24, 28, 24)
        principal.setSpacing(16)

        titulo = QLabel("Módulo de Vectores", self)
        titulo.setStyleSheet(f"""
            color: {COLOR_TEXTO_MAIN};
            font-size: 26px;
            font-weight: 900;
            font-family: 'Segoe UI', sans-serif;
        """)
        principal.addWidget(titulo)

        # Controles superiores
        controles = QHBoxLayout()
        controles.setSpacing(10)

        lbl_dim = QLabel("Dimensión:", self)
        lbl_dim.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 13px; font-weight: 700;")
        
        btn_dim_menos = QPushButton("‹", self)
        btn_dim_menos.setFixedSize(30, 30)
        btn_dim_menos.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_dim_menos.clicked.connect(lambda: self.spin_dimension.setValue(self.spin_dimension.value() - 1))

        self.spin_dimension = QSpinBox(self)
        self.spin_dimension.setRange(1, 20)
        self.spin_dimension.setValue(3)
        self.spin_dimension.setFixedHeight(30)
        self.spin_dimension.setFixedWidth(45)

        btn_dim_mas = QPushButton("›", self)
        btn_dim_mas.setFixedSize(30, 30)
        btn_dim_mas.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_dim_mas.clicked.connect(lambda: self.spin_dimension.setValue(self.spin_dimension.value() + 1))

        lbl_gen = QLabel("Vectores generadores:", self)
        lbl_gen.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 13px; font-weight: 700;")

        btn_gen_menos = QPushButton("‹", self)
        btn_gen_menos.setFixedSize(30, 30)
        btn_gen_menos.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_gen_menos.clicked.connect(lambda: self.spin_generadores.setValue(self.spin_generadores.value() - 1))

        self.spin_generadores = QSpinBox(self)
        self.spin_generadores.setRange(1, 10)
        self.spin_generadores.setValue(2)
        self.spin_generadores.setFixedHeight(30)
        self.spin_generadores.setFixedWidth(45)

        btn_gen_mas = QPushButton("›", self)
        btn_gen_mas.setFixedSize(30, 30)
        btn_gen_mas.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_gen_mas.clicked.connect(lambda: self.spin_generadores.setValue(self.spin_generadores.value() + 1))

        style_btn_step = f"""
            QPushButton {{
                background-color: #FFFFFF;
                color: {COLOR_AZUL_PRIMARIO};
                font-size: 16px;
                font-weight: 900;
                border-radius: 8px;
                border: 1px solid {COLOR_AZUL_CLARO};
            }}
            QPushButton:hover {{
                background-color: {COLOR_AZUL_CLARO};
            }}
        """
        btn_dim_menos.setStyleSheet(style_btn_step)
        btn_dim_mas.setStyleSheet(style_btn_step)
        btn_gen_menos.setStyleSheet(style_btn_step)
        btn_gen_mas.setStyleSheet(style_btn_step)

        style_spin = f"""
            QSpinBox {{
                background-color: #FFFFFF;
                border: 1px solid {COLOR_AZUL_CLARO};
                border-radius: 8px;
                color: {COLOR_TEXTO_MAIN};
                font-size: 13px;
                font-weight: 800;
                alignment: center;
            }}
            QSpinBox::up-button, QSpinBox::down-button {{ width: 0px; }}
        """
        self.spin_dimension.setStyleSheet(style_spin)
        self.spin_generadores.setStyleSheet(style_spin)

        btn_generar = QPushButton("Generar", self)
        btn_generar.setFixedHeight(36)
        btn_generar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_generar.clicked.connect(self.generar_vectores)
        btn_generar.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_AZUL_PRIMARIO};
                color: #FFFFFF;
                font-size: 13px;
                font-weight: 700;
                border-radius: 10px;
                padding: 0px 16px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {COLOR_AZUL_MEDIO};
            }}
        """)

        btn_limpiar = QPushButton("Limpiar", self)
        btn_limpiar.setFixedHeight(36)
        btn_limpiar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_limpiar.clicked.connect(self.limpiar)
        btn_limpiar.setStyleSheet(f"""
            QPushButton {{
                background-color: #FFFFFF;
                color: {COLOR_AZUL_MEDIO};
                font-size: 13px;
                font-weight: 700;
                border-radius: 10px;
                border: 1.5px solid {COLOR_AZUL_CLARO};
                padding: 0px 14px;
            }}
            QPushButton:hover {{
                background-color: #F0F9FF;
            }}
        """)

        btn_volver = QPushButton("Volver", self)
        btn_volver.setFixedHeight(36)
        btn_volver.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_volver.clicked.connect(self.close)
        btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #64748B;
                font-size: 13px;
                font-weight: 700;
                border-radius: 10px;
                border: 1.5px solid #E2E8F0;
                padding: 0px 14px;
            }
            QPushButton:hover {
                color: #04335A;
                border-color: #C4D4E6;
            }
        """)

        controles.addWidget(lbl_dim)
        controles.addWidget(btn_dim_menos)
        controles.addWidget(self.spin_dimension)
        controles.addWidget(btn_dim_mas)
        controles.addSpacing(12)
        controles.addWidget(lbl_gen)
        controles.addWidget(btn_gen_menos)
        controles.addWidget(self.spin_generadores)
        controles.addWidget(btn_gen_mas)
        controles.addSpacing(16)
        controles.addWidget(btn_generar)
        controles.addWidget(btn_limpiar)
        controles.addWidget(btn_volver)
        controles.addStretch()
        principal.addLayout(controles)

        # Área de desplazamiento para los vectores
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical {
                border: none;
                background: #E2E8F0;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #9ABCE0;
                border-radius: 4px;
                min-height: 20px;
            }
        """)
        self.contenedor = QWidget()
        self.vectores_layout = QVBoxLayout(self.contenedor)
        self.vectores_layout.setContentsMargins(0, 4, 0, 4)
        self.vectores_layout.setSpacing(12)
        self.scroll.setWidget(self.contenedor)
        principal.addWidget(self.scroll, 3)

        # Fila inferior de ejecución de operaciones
        fila_operacion = QHBoxLayout()
        fila_operacion.setSpacing(12)
        
        lbl_op = QLabel("Operación:", self)
        lbl_op.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 13px; font-weight: 700;")
        fila_operacion.addWidget(lbl_op)

        self.combo_operacion = QComboBox()
        self.combo_operacion.addItems([
            "Suma", "Resta", "Multiplicación por escalar", "Combinación lineal"
        ])
        self.combo_operacion.setFixedHeight(36)
        self.combo_operacion.setStyleSheet(f"""
            QComboBox {{
                background-color: #FFFFFF;
                color: {COLOR_AZUL_PRIMARIO};
                font-weight: 700;
                font-size: 13px;
                border-radius: 10px;
                border: 1px solid {COLOR_AZUL_CLARO};
                padding-left: 10px;
            }}
        """)
        fila_operacion.addWidget(self.combo_operacion)

        lbl_esc = QLabel("Escalar:", self)
        lbl_esc.setStyleSheet(f"color: {COLOR_TEXTO_MAIN}; font-size: 13px; font-weight: 700;")
        fila_operacion.addWidget(lbl_esc)

        self.txt_escalar = QLineEdit("2")
        self.txt_escalar.setFixedHeight(36)
        self.txt_escalar.setMaximumWidth(100)
        self.txt_escalar.setStyleSheet(f"""
            QLineEdit {{
                background-color: #FFFFFF;
                border: 1px solid {COLOR_AZUL_CLARO};
                border-radius: 10px;
                padding: 0px 8px;
                color: {COLOR_TEXTO_MAIN};
                font-weight: 700;
            }}
        """)
        fila_operacion.addWidget(self.txt_escalar)

        btn_ejecutar = QPushButton("Ejecutar", self)
        btn_ejecutar.setFixedHeight(36)
        btn_ejecutar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_ejecutar.clicked.connect(self.ejecutar)
        btn_ejecutar.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_AZUL_PRIMARIO};
                color: #FFFFFF;
                font-size: 13px;
                font-weight: 700;
                border-radius: 10px;
                padding: 0px 20px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {COLOR_AZUL_MEDIO};
            }}
        """)
        fila_operacion.addWidget(btn_ejecutar)
        fila_operacion.addStretch()
        principal.addLayout(fila_operacion)

        # Paneles inferiores de Resultados y Bitácora Estilizados
        layout_resultados = QHBoxLayout()
        layout_resultados.setSpacing(16)

        # Panel Resultado
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

        self.lbl_resultado = QLabel("Sin resultados", box_res)
        self.lbl_resultado.setWordWrap(True)
        self.lbl_resultado.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 700;
                color: #04335A;
                border: none;
                background: transparent;
            }
        """)

        # Cajita de Expresión de Resultado en Ecuación
        self.lbl_expresion_res = QLabel("Expresión de Resultado:\n—", box_res)
        self.lbl_expresion_res.setWordWrap(True)
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
        lay_r.addWidget(self.lbl_resultado)
        lay_r.addWidget(self.lbl_expresion_res)

        # Panel Procedimiento / Bitácora
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
        lay_p.setSpacing(10)

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
        principal.addLayout(layout_resultados, 2)

    def generar_vectores(self):
        while self.vectores_layout.count():
            item = self.vectores_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.tablas_vectores.clear()
        dimension = self.spin_dimension.value()
        cantidad = self.spin_generadores.value()

        for indice in range(cantidad):
            grupo = QGroupBox(f"Vector generador v{indice + 1}")
            grupo.setStyleSheet(f"""
                QGroupBox {{
                    background-color: {COLOR_TARJETA_BG};
                    border-radius: 16px;
                    border: 1px solid {COLOR_AZUL_CLARO};
                    margin-top: 10px;
                    font-weight: bold;
                    color: {COLOR_AZUL_PRIMARIO};
                    padding: 12px;
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 16px;
                    padding: 0 6px;
                }}
            """)
            
            sombra = QGraphicsDropShadowEffect(grupo)
            sombra.setBlurRadius(20)
            sombra.setColor(QColor(3, 30, 54, 15))
            sombra.setYOffset(4)
            grupo.setGraphicsEffect(sombra)

            layout = QVBoxLayout(grupo)
            tabla = QTableWidget(1, dimension)
            tabla.setMinimumHeight(65)
            tabla.setStyleSheet(f"""
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
                    padding: 4px;
                }}
            """)
            for columna in range(dimension):
                tabla.setHorizontalHeaderItem(columna, QTableWidgetItem(str(columna + 1)))
                tabla.setItem(0, columna, QTableWidgetItem("0"))
            
            layout.addWidget(tabla)
            self.vectores_layout.addWidget(grupo)
            self.tablas_vectores.append(tabla)

        # Grupo objetivo b
        grupo_objetivo = QGroupBox("Vector objetivo b (para combinación lineal)")
        grupo_objetivo.setStyleSheet(f"""
            QGroupBox {{
                background-color: {COLOR_TARJETA_BG};
                border-radius: 16px;
                border: 1px solid {COLOR_AZUL_CLARO};
                margin-top: 10px;
                font-weight: bold;
                color: {COLOR_AZUL_PRIMARIO};
                padding: 12px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 6px;
            }}
        """)
        
        sombra_obj = QGraphicsDropShadowEffect(grupo_objetivo)
        sombra_obj.setBlurRadius(20)
        sombra_obj.setColor(QColor(3, 30, 54, 15))
        sombra_obj.setYOffset(4)
        grupo_objetivo.setGraphicsEffect(sombra_obj)

        layout_objetivo = QVBoxLayout(grupo_objetivo)
        self.tabla_objetivo = QTableWidget(1, dimension)
        self.tabla_objetivo.setMinimumHeight(65)
        self.tabla_objetivo.setStyleSheet(f"""
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
                padding: 4px;
            }}
        """)
        for columna in range(dimension):
            self.tabla_objetivo.setHorizontalHeaderItem(columna, QTableWidgetItem(str(columna + 1)))
            self.tabla_objetivo.setItem(0, columna, QTableWidgetItem("0"))
        
        layout_objetivo.addWidget(self.tabla_objetivo)
        self.vectores_layout.addWidget(grupo_objetivo)
        self.vectores_layout.addStretch()

        self.lbl_resultado.setText("Sin resultados")
        self.lbl_expresion_res.setText("Expresión de Resultado:\n—")
        self.txt_bitacora.clear()

    def leer_vector(self, tabla):
        vector = []
        for columna in range(tabla.columnCount()):
            item = tabla.item(0, columna)
            texto = item.text().strip() if item else "0"
            vector.append(VectorModel.a_fraction(texto))
        return vector

    def ejecutar(self):
        try:
            vectores = [self.leer_vector(tabla) for tabla in self.tablas_vectores]
            operacion = self.combo_operacion.currentText()

            if operacion in ("Suma", "Resta"):
                if len(vectores) < 2:
                    raise ValueError("Se necesitan al menos dos vectores para esta operación.")
                
                vector_acumulado = vectores[0]
                bitacora_total = []
                nombres = [f"v{i+1}" for i in range(len(vectores))]
                expr_str = f" {(' + ' if operacion == 'Suma' else ' - ')}.join(nombres)"

                for idx, siguiente_vector in enumerate(vectores[1:], start=2):
                    if operacion == "Suma":
                        res = VectorModel.suma(vector_acumulado, siguiente_vector)
                    else:
                        res = VectorModel.resta(vector_acumulado, siguiente_vector)
                    
                    vector_acumulado = res["resultado"]
                    bitacora_total.append(f"<div style='background-color: #E0F2FE; color: #04335A; padding: 6px 12px; border-radius: 8px; font-weight: bold; margin-top: 10px;'>=== Operación con v{idx} ===</div>")
                    bitacora_total.append(f"<pre style='font-family: Consolas; font-size: 12px; color: #334155;'>{res['pasos']}</pre>")

                vector_fmt = VectorModel.formato_vector(vector_acumulado)
                texto_resultado = f"Vector Resultado: {vector_fmt}"
                
                simbolo = "+" if operacion == "Suma" else "-"
                expr_ecuacion = f" v1 {simbolo} " + f" {simbolo} ".join([f"v{i}" for i in range(2, len(vectores)+1)]) + f" = {vector_fmt}"
                
                self.lbl_expresion_res.setText(f"Expresión de Resultado:\n{expr_ecuacion}")
                texto_bitacora = "".join(bitacora_total)

            elif operacion == "Multiplicación por escalar":
                if not vectores:
                    raise ValueError("Debe existir al menos un vector.")
                
                escalar = VectorModel.a_fraction(self.txt_escalar.text())
                res = VectorModel.escalar(vectores[0], escalar)
                vector_fmt = VectorModel.formato_vector(res['resultado'])
                
                texto_resultado = f"Vector Resultado: {vector_fmt}"
                expr_ecuacion = f"{escalar} · v1 = {vector_fmt}"
                self.lbl_expresion_res.setText(f"Expresión de Resultado:\n{expr_ecuacion}")
                texto_bitacora = f"<pre style='font-family: Consolas; font-size: 12px; color: #334155;'>{res['pasos']}</pre>"

            else:  # Combinación lineal
                objetivo = self.leer_vector(self.tabla_objetivo)
                respuesta = VectorModel.combinacion_lineal(vectores, objetivo)
                
                texto_resultado = respuesta["clasificacion"]
                coefs_str = ""
                if isinstance(respuesta["coeficientes"], list):
                    coefs_str = VectorModel.formato_vector(respuesta["coeficientes"])
                    texto_resultado += f"\nCoeficientes: {coefs_str}"
                
                expr_ecuacion = f"Combinación Lineal (b): {respuesta['clasificacion']}"
                self.lbl_expresion_res.setText(f"Expresión de Resultado:\n{expr_ecuacion}")
                texto_bitacora = f"<pre style='font-family: Consolas; font-size: 12px; color: #334155;'>{respuesta['pasos']}</pre>"

            self.lbl_resultado.setText(texto_resultado)
            self.txt_bitacora.setHtml(texto_bitacora)

        except Exception as error:
            QMessageBox.warning(self, "Error", str(error))

    def limpiar(self):
        tablas = self.tablas_vectores + ([self.tabla_objetivo] if hasattr(self, "tabla_objetivo") else [])
        for tabla in tablas:
            if tabla:
                for fila in range(tabla.rowCount()):
                    for columna in range(tabla.columnCount()):
                        tabla.setItem(fila, columna, QTableWidgetItem("0"))
        self.txt_escalar.setText("2")
        self.lbl_resultado.setText("Sin resultados")
        self.lbl_expresion_res.setText("Expresión de Resultado:\n—")
        self.txt_bitacora.clear()

    def closeEvent(self, event):
        if self.parent_window is not None:
            self.parent_window.show()
        event.accept()