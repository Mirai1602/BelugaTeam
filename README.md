# BelugaCalc

**BelugaCalc** es una aplicación de escritorio desarrollada en Python con una interfaz gráfica moderna utilizando PyQt6 y Fluent Widgets. Está diseñada para resolver operaciones matemáticas básicas, álgebra lineal avanzada, cálculos vectoriales, sistemas de ecuaciones y conversiones numéricas.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green?style=flat&logo=qt)](https://pypi.org/project/PyQt6/)
[![Fluent Widgets](https://img.shields.io/badge/UI-PyQt6--Fluent--Widgets-purple?style=flat)](https://pypi.org/project/PyQt6-Fluent-Widgets/)
[![Repo GitHub](https://img.shields.io/badge/GitHub-BelugaTeam-black?style=flat&logo=github)](https://github.com/Mirai1602/BelugaTeam)

---

##  Características Principales

* **Interfaz Moderna (Fluent Design):** Componentes visuales basados en Fluent UI para una navegación fluida e intuitiva.
* **Operaciones Básicas:** Suma, resta, multiplicación y funciones aritméticas esenciales.
* **Álgebra Lineal Avanzada:**
  * Eliminación de Gauss y Gauss-Jordan.
  * Reducción de pivotes.
* **Sistemas de Ecuaciones:** Resolución de sistemas lineales y ecuaciones.
* **Cálculo Vectorial:** Operaciones y análisis de vectores.
* **Conversiones Numéricas:** Conversión entre diferentes sistemas y bases de números.

---

## Requisitos e Instalación

### Requisitos Previos
* **Python 3.8** o superior instalado en el sistema.

### Instalación de Dependencias

Ejecuta los siguientes comandos en tu terminal para instalar las librerías necesarias:

```bash
pip install PyQt6
pip install "PyQt6-Fluent-Widgets"
```

### Estructura del proyecto

BelugaTeam/
├── assets/                     # Recursos visuales e imágenes
│   └── BelugaK1.png            # Logotipo / Icono de la aplicación
├── core/                       # Lógica interna y módulos matemáticos
│   ├── conversiones.py         # Algoritmos de conversión numérica
│   ├── matriz.py               # Clase Matriz y manipulación
│   ├── operaciones.py          # Operaciones aritméticas y matriciales
│   ├── utils.py                # Funciones auxiliares y de soporte
│   └── vectoriales.py          # Lógica para cálculo vectorial
├── ui/                         # Componentes de la interfaz gráfica (PyQt6 Fluent)
│   ├── avanzada_window.py      # Operaciones avanzadas (Gauss, pivotes, etc.)
│   ├── basica_window.py        # Interfaz de operaciones básicas
│   ├── conversion_widget.py    # Componentes reutilizables para conversiones
│   ├── conversiones_window.py  # Ventana de conversiones numéricas
│   ├── ecuaciones_window.py    # Ventana para resolución de ecuaciones
│   ├── home_window.py          # Pantalla principal de bienvenida
│   ├── main_window.py          # Contenedor principal y navegación
│   └── vectoriales_window.py   # Ventana para operaciones vectoriales
├── controllers/                # Controladores adicionales
├── main.py                     # Punto de entrada principal
├── requirements.txt            # Archivo de dependencias
└── README.md                   # Documentación del proyecto


Para ejecutar:

```bash
python main.py
```


