import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.main_window import Ui_MainWindow
from controllers.main_controller import MainController

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.controller = MainController(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
