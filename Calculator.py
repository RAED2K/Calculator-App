import sys

from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
                             QPushButton, QMainWindow, QGridLayout, QLineEdit)
from PyQt6.QtCore import Qt, QSize
from pycares import symbol


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Calculator")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        self.result_display = QLineEdit(self)
        self.result_display.setReadOnly(True)
        self.result_display.setFixedHeight(50)
        self.result_display.setText("0")
        self.result_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(self.result_display)
        grid = QGridLayout()
        main_layout.addLayout(grid)
        sym = ['Cls', 'Back', '(', ')',
               '7', '8', '9', '/',
               '4', '5', '6', '*',
               '1', '2', '3', '-',
               '0', '.', '=', '+']

        position = [(i,j) for i in range(5) for j in range(4)]
        for position, sym in zip(position, sym):

            button = QPushButton(sym)
            grid.addWidget(button, *position)
            button.clicked.connect(self.on_button_clicked)


    def on_button_clicked(self):
        sender = self.sender()
        symbol = sender.text()

        current_text = self.result_display.text()

        if symbol == 'Cls':
            self.result_display.setText('0')
        elif symbol == 'Back':
            self.result_display.setText(current_text[:-1] or '0')
        elif symbol == '=':
            try:
                result = str(eval(current_text))
                self.result_display.setText(result)
            except Exception:
                self.result_display.setText("Error")
        else:
            if current_text == '0':
                self.result_display.setText(symbol)
            else:
                self.result_display.setText(current_text + symbol)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())

    