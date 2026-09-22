from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
    QGroupBox, QTextEdit, QComboBox, QScrollArea, QDialog,
    QFormLayout, QDialogButtonBox
)

from core.operaciones import MatrizModel
from ui.conversiones_window import ConversionesWindow


class DimensionesDialog(QDialog):
    def __init__(self, parent=None, filas=3, columnas=3, numero=1):
        super().__init__(parent)
        self.setWindowTitle(f"Dimensiones de Matriz {numero}")

        formulario = QFormLayout(self)

        self.spin_filas = QSpinBox()
        self.spin_filas.setRange(1, 20)
        self.spin_filas.setValue(filas)

        self.spin_columnas = QSpinBox()
        self.spin_columnas.setRange(1, 20)
        self.spin_columnas.setValue(columnas)

        formulario.addRow("Filas:", self.spin_filas)
        formulario.addRow("Columnas:", self.spin_columnas)

        botones = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        botones.accepted.connect(self.accept)
        botones.rejected.connect(self.reject)
        formulario.addRow(botones)

    def dimensiones(self):
        return self.spin_filas.value(), self.spin_columnas.value()


class CalculadoraMatrices(QWidget):
    def __init__(self, ventana_principal=None):
        super().__init__()

        self.ventana_principal = ventana_principal
        self.setWindowTitle("BelugaCalc - Básica")
        self.resize(1100, 800)

        self.tablas = []
        self.operadores = []
        self.grupos_matrices = []
        self.init_ui()

    def init_ui(self):
        layout_principal = QVBoxLayout()

        titulo = QLabel("<h2>Calculadora Básica</h2>")
        layout_principal.addWidget(titulo)

        controles = QHBoxLayout()

        btn_agregar = QPushButton("Agregar matriz")
        btn_agregar.clicked.connect(self.agregar_matriz)
        controles.addWidget(btn_agregar)

        btn_limpiar = QPushButton("Limpiar")
        btn_limpiar.clicked.connect(self.limpiar_tablas)
        controles.addWidget(btn_limpiar)

        btn_ejecutar = QPushButton("Ejecutar operación")
        btn_ejecutar.clicked.connect(self.ejecutar_expresion)
        controles.addWidget(btn_ejecutar)

        btn_conversiones = QPushButton("Conversiones")
        btn_conversiones.clicked.connect(self.abrir_conversiones)
        controles.addWidget(btn_conversiones)

        btn_volver = QPushButton("Volver")
        btn_volver.clicked.connect(self.volver)
        controles.addWidget(btn_volver)

        controles.addStretch()
        layout_principal.addLayout(controles)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.contenedor_matrices = QWidget()
        self.matrices_layout = QHBoxLayout(self.contenedor_matrices)
        self.scroll_area.setWidget(self.contenedor_matrices)
        layout_principal.addWidget(self.scroll_area, 3)

        layout_principal.addWidget(QLabel("<b>Resultado:</b>"))
        self.tabla_res = QTableWidget()
        self.tabla_res.setMaximumHeight(180)
        layout_principal.addWidget(self.tabla_res)

        layout_principal.addWidget(QLabel("<b>Procedimiento Paso a Paso:</b>"))
        self.txt_bitacora = QTextEdit()
        self.txt_bitacora.setReadOnly(True)
        layout_principal.addWidget(self.txt_bitacora, 2)

        self.setLayout(layout_principal)

        self.agregar_matriz(usar_dialogo=False)
        self.agregar_matriz(usar_dialogo=False)

    def crear_grupo_tabla(self, numero, tabla):
        grupo = QGroupBox(f"Matriz {numero}")
        layout = QVBoxLayout()

        dimensiones = QHBoxLayout()
        btn_dimensiones = QPushButton("Cambiar dimensiones")
        btn_dimensiones.clicked.connect(
            lambda: self.cambiar_dimensiones(numero - 1)
        )
        dimensiones.addWidget(btn_dimensiones)

        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(
            lambda: self.eliminar_matriz(numero - 1)
        )
        dimensiones.addWidget(btn_eliminar)
        dimensiones.addStretch()
        layout.addLayout(dimensiones)

        layout.addWidget(tabla)
        grupo.setLayout(layout)
        return grupo

    def agregar_matriz(self, usar_dialogo=True):
        numero = len(self.tablas) + 1
        filas, columnas = 3, 3

        if usar_dialogo:
            dialogo = DimensionesDialog(self, filas, columnas, numero)
            if dialogo.exec() != QDialog.DialogCode.Accepted:
                return
            filas, columnas = dialogo.dimensiones()

        if self.tablas:
            operador = QComboBox()
            operador.addItems(["+", "-", "*"])
            operador.setCurrentText("+")
            operador.setFixedWidth(70)
            self.matrices_layout.addWidget(operador)
            self.operadores.append(operador)

        tabla = QTableWidget(filas, columnas)
        tabla.setMinimumWidth(280)
        tabla.setMinimumHeight(180)

        self.tablas.append(tabla)
        grupo = self.crear_grupo_tabla(numero, tabla)
        self.grupos_matrices.append(grupo)
        self.matrices_layout.addWidget(grupo)

    def eliminar_matriz(self, indice):
        if indice < 0 or indice >= len(self.tablas):
            return

        if len(self.tablas) <= 1:
            QMessageBox.information(
                self,
                "Eliminar matriz",
                "Debe existir al menos una matriz en la calculadora."
            )
            return

        respuesta = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Deseas eliminar la Matriz {indice + 1}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if respuesta != QMessageBox.StandardButton.Yes:
            return

        # Cada operador está ubicado entre dos matrices.
        # Si eliminamos la primera matriz, quitamos el operador siguiente;
        # en otro caso, quitamos el operador que estaba antes de ella.
        operador_indice = 0 if indice == 0 else indice - 1
        if self.operadores:
            operador = self.operadores.pop(operador_indice)
            self.matrices_layout.removeWidget(operador)
            operador.deleteLater()

        tabla = self.tablas.pop(indice)
        grupo = self.grupos_matrices.pop(indice)
        self.matrices_layout.removeWidget(grupo)
        grupo.deleteLater()
        tabla.deleteLater()

        # Actualizar los títulos para que sigan una numeración consecutiva.
        for numero, grupo_actual in enumerate(self.grupos_matrices, start=1):
            grupo_actual.setTitle(f"Matriz {numero}")

        self.txt_bitacora.clear()
        self.tabla_res.clearContents()
        self.tabla_res.setRowCount(0)
        self.tabla_res.setColumnCount(0)

    def cambiar_dimensiones(self, indice):
        tabla = self.tablas[indice]
        dialogo = DimensionesDialog(
            self,
            tabla.rowCount(),
            tabla.columnCount(),
            indice + 1
        )

        if dialogo.exec() != QDialog.DialogCode.Accepted:
            return

        filas, columnas = dialogo.dimensiones()
        tabla.setRowCount(filas)
        tabla.setColumnCount(columnas)

    def limpiar_tablas(self):
        for tabla in self.tablas + [self.tabla_res]:
            tabla.clearContents()
        self.txt_bitacora.clear()

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

    def formato_operando(self, indice):
        return f"Matriz {indice + 1}"

    def generar_pasos_operacion(self, izquierda, derecha, resultado, operador, texto_izq, texto_der):
        pasos = []
        pasos.append(f"=== {texto_izq} {operador} {texto_der} ===")

        if operador == "+":
            pasos.append("Se suman las entradas que ocupan la misma posición.\n")
        elif operador == "-":
            pasos.append("Se restan las entradas que ocupan la misma posición.\n")
        else:
            pasos.append("Cada entrada se obtiene mediante producto fila por columna.\n")
            for i in range(len(izquierda)):
                for j in range(len(derecha[0])):
                    terminos = []
                    for k in range(len(izquierda[0])):
                        terminos.append(
                            f"({izquierda[i][k]})({derecha[k][j]})"
                        )
                    pasos.append(
                        f"Resultado[{i + 1},{j + 1}] = "
                        + " + ".join(terminos)
                        + f" = {resultado[i][j]}"
                    )

        pasos.append(MatrizModel.formato_matriz_str(izquierda, texto_izq))
        pasos.append(MatrizModel.formato_matriz_str(derecha, texto_der))
        pasos.append("Resultado parcial:\n")
        pasos.append(MatrizModel.formato_matriz_str(resultado))
        return "\n".join(pasos)

    def ejecutar_expresion(self):
        try:
            matrices = [self.leer_matriz(tabla) for tabla in self.tablas]
            operadores = [combo.currentText() for combo in self.operadores]

            if len(matrices) < 2:
                raise ValueError("Se necesitan al menos dos matrices.")

            resultado, pasos = self.evaluar_expresion(matrices, operadores)
            self.mostrar_resultado(resultado)
            self.txt_bitacora.setText(pasos)

        except ValueError as error:
            QMessageBox.warning(self, "Error", str(error))
        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"Ocurrió un error inesperado: {error}"
            )

    def evaluar_expresion(self, matrices, operadores):
        # Se aplica la precedencia usual: multiplicación antes que suma/resta.
        valores = list(matrices)
        ops = list(operadores)
        nombres = [f"Matriz {i + 1}" for i in range(len(matrices))]
        pasos = ["=== EVALUACIÓN DE LA EXPRESIÓN ===", ""]
        pasos.append(
            "Expresión: " + " ".join(
                item for par in zip(nombres, ops + [""]) for item in par if item
            )
        )
        pasos.append("La multiplicación (*) tiene prioridad sobre (+) y (-).\n")

        while "*" in ops:
            indice = ops.index("*")
            izquierda = valores[indice]
            derecha = valores[indice + 1]
            resultado = self.realizar_operacion(izquierda, derecha, "*")
            pasos.append(
                self.generar_pasos_operacion(
                    izquierda,
                    derecha,
                    resultado,
                    "*",
                    nombres[indice],
                    nombres[indice + 1]
                )
            )
            valores[indice:indice + 2] = [resultado]
            nombre_resultado = f"({nombres[indice]} * {nombres[indice + 1]})"
            nombres[indice:indice + 2] = [nombre_resultado]
            ops.pop(indice)

        while ops:
            operador = ops.pop(0)
            izquierda = valores.pop(0)
            derecha = valores.pop(0)
            nombre_izquierda = nombres.pop(0)
            nombre_derecha = nombres.pop(0)
            resultado = self.realizar_operacion(izquierda, derecha, operador)
            pasos.append(
                self.generar_pasos_operacion(
                    izquierda,
                    derecha,
                    resultado,
                    operador,
                    nombre_izquierda,
                    nombre_derecha
                )
            )
            valores.insert(0, resultado)
            nombres.insert(0, f"({nombre_izquierda} {operador} {nombre_derecha})")

        pasos.append("\n=== RESULTADO FINAL ===")
        pasos.append(MatrizModel.formato_matriz_str(valores[0]))
        return valores[0], "\n".join(pasos)

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
