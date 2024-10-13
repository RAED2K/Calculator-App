import sys
import math

from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGridLayout,
                             QPushButton, QMainWindow, QLineEdit )
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_degree_mode = True  # Default to degree mode
        self.is_second_mode = False  # Track "2nd" mode
        self.error_occurred = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Calculator")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        self.result_display = QLineEdit(self)
        self.result_display.setFixedHeight(80)
        self.result_display.setText("0")
        self.result_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(self.result_display)
        grid = QGridLayout()
        main_layout.addLayout(grid)
        self.setFixedSize(460, 600)
        self.setMaximumSize(460, 600)
        self.setWindowIcon(QIcon("calculator.ico"))

        grid.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        self.setStyleSheet("""
            QLineEdit {
                font-size: 30px;
                padding: 10px;
                border: 5px solid #2a755a;
                border-radius: 10px;
            }
            QPushButton {
                font-size: 25px;
                background-color: #2a755a;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
            }
             QPushButton:hover {
                background-color: #45a049; 
            }
            QMainWindow {
                background-color: #020a17;
            }
        """)


        self.sym = ['2nd', 'deg', 'sin', 'cos', 'tan',
                    'lg', 'ln', 'e', '[', ']',
                    '^', 'AC', '⌫', '(', ')',
                    '√', '7', '8', '9', '÷',
                    '!', '4', '5', '6', '×',
                    '⁽⁻¹⁾', '1', '2', '3', '-',
                    'π',  '0', '.', '=', '+']

        position = [(i, j) for i in range(7) for j in range(5)]
        for pos, symbol in zip(position, self.sym):
            button = QPushButton(symbol)
            button.setFixedSize(80, 60)
            grid.addWidget(button, *pos)
            button.clicked.connect(self.on_button_clicked)
            if symbol == '⌫':
                button.setStyleSheet("""
                                QPushButton {
                                    padding-top: 20px;
                                }""")
            if symbol == '⁽⁻¹⁾':
                button.setStyleSheet("""
                                QPushButton {
                                    padding-top: 24px;
                                }""")

            if (symbol in ['AC', '⌫', '(', ')', '÷', '×', '-', '+', '=', '.',
                           '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
                button.setStyleSheet("""
                                QPushButton {
                                    background-color: #3e9c7a;
                                }
                                QPushButton:hover {
                                    background-color: #45a049;
                                }""")

    def on_button_clicked(self):
        sender = self.sender()
        symbol = sender.text()

        self.animate_button(sender)

        current_text = self.result_display.text()
        operators_with_brackets = ['√', 'sin', 'cos', 'tan', 'sin⁻¹', 'cos⁻¹', 'tan⁻¹', 'ln', 'lg']

        if self.error_occurred:
            current_text = ''
            self.error_occurred = False


        if symbol == '2nd':
            self.toggle_second_mode()
        elif symbol == 'deg' or symbol == 'rad':
            self.toggle_deg_rad(sender)
        elif symbol == 'AC':
            self.result_display.setText('0')
        elif symbol == '⌫':
            self.result_display.setText(current_text[:-1] or '0')
        elif symbol == '=':
            try:
                result = self.evaluate_expression(current_text)
                self.result_display.setText(str(result))
            except Exception as e:
                self.result_display.setText("Error")
                self.error_occurred = True
        else:
            if symbol in operators_with_brackets:
                if current_text == '0':
                    self.result_display.setText(f'{symbol}(')
                    self.result_display.setCursorPosition(len(symbol)+1)
                else:
                    self.result_display.setText(current_text + f'{symbol}()')
                    self.result_display.setCursorPosition(len(current_text) + len(symbol) + 1)
            else:
                if current_text == '0' or current_text == "Error":
                    self.result_display.setText(symbol)
                else:
                    self.result_display.setText(current_text + symbol)

    def animate_button(self, button):
        original_color = button.palette().color(button.backgroundRole()).name()
        pressed_color = '#45a049'

        button.setStyleSheet(f"QPushButton {{ background-color: {pressed_color}; color: white; }}")
        QTimer.singleShot(100, lambda: button.setStyleSheet(
            f"QPushButton {{ background-color: {original_color}; color: white; }}"))

    def toggle_deg_rad(self, sender):
        if self.is_degree_mode:
            self.is_degree_mode = False
            sender.setText('rad')
        else:
            self.is_degree_mode = True
            sender.setText('deg')
            self.is_second_mode = False
            self.update_trig_buttons("normal")


    def toggle_second_mode(self):
        if self.is_degree_mode:
            self.is_second_mode = not self.is_second_mode
            self.update_trig_buttons("2nd" if self.is_second_mode else "normal")


    def update_trig_buttons(self, mode):
        if mode == "2nd":
            self.sym[2] = 'sin⁻¹'
            self.sym[3] = 'cos⁻¹'
            self.sym[4] = 'tan⁻¹'
        else:
            self.sym[2] = 'sin'
            self.sym[3] = 'cos'
            self.sym[4] = 'tan'

        for i, button in enumerate(self.findChildren(QPushButton)):
            button.setText(self.sym[i])

    def evaluate_expression(self, expression):
        try:
            while '!' in expression:
                index = expression.index('!')
                num_str = ''
                i = index - 1
                while i >= 0 and (expression[i].isdigit() or expression[i] == '.'):
                    num_str = expression[i] + num_str
                    i -= 1
                if num_str:
                    number = int(num_str)
                    factorial_result = math.factorial(number)
                    expression = expression[:i + 1] + str(factorial_result) + expression[index + 1:]
                else:
                    raise ValueError("Invalid factorial expression.")

            while '⁽⁻¹⁾' in expression:
                num_str = ''
                i = expression.index('⁽⁻¹⁾') - 1
                while i >= 0 and (expression[i].isdigit() or expression[i] == '.'):
                    num_str = expression[i] + num_str
                    i -= 1

                if num_str:
                    number = float(num_str)
                    if number != 0:
                        reciprocal_result = 1 / number
                        expression = expression[:i + 1] + str(reciprocal_result) + expression[
                                                                                   expression.index('⁽⁻¹⁾') + 4:]
                    else:
                        raise ValueError("Cannot divide by zero.")
                else:
                    raise ValueError("Invalid '1 / x' expression.")

            expression = expression.replace('[', '(').replace(']', ')')
            expression = expression.replace('×', '*').replace('÷', '/').replace('^', '**')
            expression = expression.replace('ln', 'math.log')
            expression = expression.replace('lg', 'math.log10')
            expression = expression.replace('π', 'math.pi')
            expression = expression.replace('e', 'math.e')
            expression = expression.replace('√', 'math.sqrt')

            expression = self.convert_trig_to_radians(expression)

            result = eval(expression)

            return result
        except Exception as e:
            return "Error"


    def convert_trig_to_radians(self, expression):
        """
        Converts the arguments of trigonometric functions (sin, cos, tan) to radians
        if the calculator is in degree mode.
        """
        if self.is_degree_mode:
            if self.is_second_mode:
                expression = expression.replace('sin⁻¹', 'math.degrees(math.asin(')
                expression = expression.replace('cos⁻¹', 'math.degrees(math.acos(')
                expression = expression.replace('tan⁻¹', 'math.degrees(math.atan(')
            else:
                expression = expression.replace('sin', 'math.sin(math.radians(')
                expression = expression.replace('cos', 'math.cos(math.radians(')
                expression = expression.replace('tan', 'math.tan(math.radians(')
        else:
            expression = expression.replace('sin', 'math.sin')
            expression = expression.replace('cos', 'math.cos')
            expression = expression.replace('tan', 'math.tan')


        open_count = expression.count('(')
        close_count = expression.count(')')
        if open_count > close_count:
            expression += ')' * (open_count - close_count)

        return expression


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())