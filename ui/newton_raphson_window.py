import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget,QVBoxLayout,QHBoxLayout,QLabel,QLineEdit,QPushButton,
    QDoubleSpinBox,QSpinBox,QFrame,QTableWidget,QTableWidgetItem,QTextEdit,QMessageBox,QHeaderView,QSplitter)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from core.biseccion import preparar_funcion
from core.newton_raphson import resolver_newton_raphson

class NewtonRaphsonWindow(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setStyleSheet('background-color:#F4F8FB;')
        self._crear_interfaz()

    def _crear_interfaz(self):
        principal=QVBoxLayout(self)
        principal.setContentsMargins(20,16,20,16)
        titulo=QLabel('Método Newton-Raphson')
        titulo.setStyleSheet('color:#031E36;font-size:24px;font-weight:900;')
        principal.addWidget(titulo)
        subtitulo=QLabel('Escribe f(x), el valor inicial X0 y la tolerancia. La derivada se calcula automáticamente.')
        subtitulo.setStyleSheet('color:#64748B;')
        principal.addWidget(subtitulo)
        tarjeta=QFrame()
        tarjeta.setStyleSheet('QFrame{background:white;border:1px solid #C4D4E6;border-radius:12px;}')
        campos=QHBoxLayout(tarjeta)
        self.txt_funcion=QLineEdit('x^3 - x - 2')
        self.txt_x0=QLineEdit('1.5')
        self.spin_tolerancia=QDoubleSpinBox()
        self.spin_tolerancia.setDecimals(10)
        self.spin_tolerancia.setRange(0.0000000001,1e6)
        self.spin_tolerancia.setValue(0.000001)
        self.spin_n=QSpinBox()
        self.spin_n.setRange(1,10000)
        self.spin_n.setValue(100)
        for nombre,widget,ancho in [('f(x):',self.txt_funcion,4),('X0:',self.txt_x0,1),('Tolerancia:',self.spin_tolerancia,2),('Iteraciones:',self.spin_n,1)]:
            grupo=QVBoxLayout()
            etiqueta=QLabel(nombre)
            etiqueta.setStyleSheet('color:#04335A;font-weight:700;')
            grupo.addWidget(etiqueta)
            widget.setMinimumHeight(34)
            widget.setStyleSheet('background:#FAFCFE;color:#031E36;border:1px solid #C4D4E6;border-radius:7px;padding:5px;')
            grupo.addWidget(widget)
            campos.addLayout(grupo,ancho)
        principal.addWidget(tarjeta)
        acciones=QHBoxLayout()
        for nombre,accion in [('Graficar función',self.graficar),('Calcular Newton-Raphson',self.calcular),('Limpiar',self.limpiar)]:
            boton=QPushButton(nombre)
            boton.setCursor(Qt.CursorShape.PointingHandCursor)
            boton.setStyleSheet('QPushButton{background:#04335A;color:white;font-weight:700;border:0;border-radius:9px;padding:9px 13px;} QPushButton:hover{background:#4474A3;}')
            boton.clicked.connect(accion)
            acciones.addWidget(boton)
        acciones.addStretch()
        principal.addLayout(acciones)
        self.lbl_estado=QLabel('Lista para graficar o calcular.')
        self.lbl_estado.setStyleSheet('background:#EAF5FC;color:#04335A;border:1px solid #C4D4E6;border-radius:8px;padding:9px;font-weight:700;')
        principal.addWidget(self.lbl_estado)
        splitter=QSplitter(Qt.Orientation.Vertical)
        frame_tabla=QFrame()
        lt=QVBoxLayout(frame_tabla)
        lt.addWidget(QLabel('Tabla de iteraciones'))
        self.tabla=QTableWidget(0,8)
        self.tabla.setHorizontalHeaderLabels(['i','X anterior','f(X)','f\'(X)','X nuevo','f(X nuevo)','Cambio','Residuo'])
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setStyleSheet('QTableWidget{background:#FAFCFE;color:#031E36;} QHeaderView::section{background:#C4D4E6;color:#04335A;font-weight:700;}')
        lt.addWidget(self.tabla)
        splitter.addWidget(frame_tabla)
        inferior=QSplitter(Qt.Orientation.Horizontal)
        proc=QFrame()
        lp=QVBoxLayout(proc)
        lp.addWidget(QLabel('Procedimiento / Bitácora'))
        self.bitacora=QTextEdit()
        self.bitacora.setReadOnly(True)
        self.bitacora.setStyleSheet('background:white;color:#1E293B;font-family:Consolas;')
        lp.addWidget(self.bitacora)
        inferior.addWidget(proc)
        graf=QFrame()
        lg=QVBoxLayout(graf)
        lg.addWidget(QLabel('Gráfica de f(x) y aproximaciones'))
        self.figura=Figure(figsize=(5,3),tight_layout=True)
        self.canvas=FigureCanvas(self.figura)
        self.ax=self.figura.add_subplot(111)
        lg.addWidget(self.canvas)
        inferior.addWidget(graf)
        inferior.setSizes([500,500])
        splitter.addWidget(inferior)
        splitter.setSizes([260,360])
        principal.addWidget(splitter,1)

    def _dibujar(self,filas=None):
        simbolica,f=preparar_funcion(self.txt_funcion.text().strip())
        x0=float(self.txt_x0.text())
        valores=[x0]+([fila['x_nuevo'] for fila in filas] if filas else [])
        centro=valores[-1]
        margen=max(1.5,abs(centro-x0)*2)
        xs=np.linspace(min(valores)-margen,max(valores)+margen,500)
        ys=[]
        for x in xs:
            try: ys.append(f(float(x)))
            except (ValueError,ZeroDivisionError,OverflowError): ys.append(np.nan)
        self.ax.clear()
        self.ax.plot(xs,ys,label='f(x)',color='#2563EB')
        self.ax.axhline(0,color='#64748B',linewidth=1)
        if filas:
            for fila in filas:
                self.ax.scatter([fila['x_nuevo']],[fila['fx_nuevo']],color='#E68A25',s=22,zorder=4)
        self.ax.set_ylim(np.nanpercentile(ys,5)-1,np.nanpercentile(ys,95)+1) if np.isfinite(ys).any() else None
        self.ax.grid(True,alpha=.25)
        self.ax.legend()
        self.canvas.draw()

    def graficar(self):
        try:
            self._dibujar()
            self.lbl_estado.setText('Función graficada. Puedes calcular Newton-Raphson.')
        except Exception as exc:
            QMessageBox.warning(self,'Error al graficar',str(exc))

    def calcular(self):
        try:
            funcion,derivada,filas,raiz,residuo,resumen=resolver_newton_raphson(
                self.txt_funcion.text().strip(),self.txt_x0.text().strip(),
                self.spin_tolerancia.value(),self.spin_n.value())
            self.tabla.setRowCount(len(filas))
            claves=['it','x_anterior','fx','dfx','x_nuevo','fx_nuevo','cambio','residuo']
            for i,fila in enumerate(filas):
                for j,clave in enumerate(claves):
                    valor=fila[clave]
                    self.tabla.setItem(i,j,QTableWidgetItem(str(valor) if clave=='it' else f'{valor:.10g}'))
            self.bitacora.setPlainText(resumen)
            self.lbl_estado.setText(f'Raíz aproximada: {raiz:.10f} | Residuo: {residuo:.3g}')
            self._dibujar(filas)
        except Exception as exc:
            QMessageBox.warning(self,'No se pudo calcular',str(exc))

    def limpiar(self):
        self.txt_funcion.clear()
        self.txt_x0.clear()
        self.tabla.setRowCount(0)
        self.bitacora.clear()
        self.ax.clear()
        self.canvas.draw()
        self.lbl_estado.setText('Lista para graficar o calcular.')