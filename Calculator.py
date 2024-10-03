import sys

from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
                             QPushButton, QMainWindow, QGridLayout)
from PyQt6.QtCore import Qt, QSize

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Calculator")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        grid = QGridLayout(central_widget)


        sym = ['Cls', 'Back', '', 'Close',
               '7', '8', '9', '/',
               '4', '5', '6', '*',
               '1', '2', '3', '-',
               '0', '.', '=', '+']

        position = [(i,j) for i in range(5) for j in range(4)]
        for position, sym in zip(position, sym):

            button = QPushButton(sym)
            grid.addWidget(button, *position)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())

    