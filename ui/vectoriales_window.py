from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog

class VectorialesWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, CalcWindow):
        CalcWindow.setObjectName("CalcWindow")
        CalcWindow.resize(700, 500)

        # Layout principal
        self.verticalLayout = QtWidgets.QVBoxLayout(CalcWindow)

        # --- Vector U ---
        self.lblU = QtWidgets.QLabel("Vector U")
        self.verticalLayout.addWidget(self.lblU)

        self.tableA = QtWidgets.QTableWidget()
        self.tableA.setRowCount(1)       # Por defecto 1 fila
        self.tableA.setColumnCount(3)    # Por defecto 3 columnas
        self.verticalLayout.addWidget(self.tableA)

        # --- Vector V ---
        self.lblV = QtWidgets.QLabel("Vector V")
        self.verticalLayout.addWidget(self.lblV)

        self.tableB = QtWidgets.QTableWidget()
        self.tableB.setRowCount(1)
        self.tableB.setColumnCount(3)
        self.verticalLayout.addWidget(self.tableB)

        # --- Botones de operaciones ---
        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.btn_prod_punto = QtWidgets.QPushButton("Producto Punto")
        self.horizontalLayout.addWidget(self.btn_prod_punto)

        self.btn_prod_cruz = QtWidgets.QPushButton("Producto Cruz")
        self.horizontalLayout.addWidget(self.btn_prod_cruz)

        self.btn_norma = QtWidgets.QPushButton("Norma")
        self.horizontalLayout.addWidget(self.btn_norma)

        self.btn_angulo = QtWidgets.QPushButton("Ángulo")
        self.horizontalLayout.addWidget(self.btn_angulo)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # --- Resultado ---
        self.lblResultado = QtWidgets.QLabel("Resultado")
        self.verticalLayout.addWidget(self.lblResultado)

        self.tableResultado = QtWidgets.QTableWidget()
        self.verticalLayout.addWidget(self.tableResultado)

        # --- Bitácora ---
        self.lblBitacora = QtWidgets.QLabel("Bitácora")
        self.verticalLayout.addWidget(self.lblBitacora)

        self.txt_bitacora = QtWidgets.QTextEdit()
        self.verticalLayout.addWidget(self.txt_bitacora)

        # Configuración final
        self.retranslateUi(CalcWindow)
        QtCore.QMetaObject.connectSlotsByName(CalcWindow)

    def retranslateUi(self, CalcWindow):
        CalcWindow.setWindowTitle("Calculadora Vectorial")
