from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys


class ConverterWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("进制转换器")
        self.setWindowIcon(QIcon("Icon-A1.ico"))
        self.setGeometry(100, 100, 320, 210)

        self.decimal_label = QLabel("十进制:", self)
        self.decimal_label.move(20, 20)

        self.decimal_line = QLineEdit(self)
        self.decimal_line.move(120, 20)
        self.decimal_line.textChanged.connect(self.convert_decimal)

        self.binary_label = QLabel("二进制:", self)
        self.binary_label.move(20, 60)

        self.binary_line = QLineEdit(self)
        self.binary_line.move(120, 60)
        self.binary_line.textChanged.connect(self.convert_binary)

        self.octal_label = QLabel("八进制:", self)
        self.octal_label.move(20, 100)

        self.octal_line = QLineEdit(self)
        self.octal_line.move(120, 100)
        self.octal_line.textChanged.connect(self.convert_octal)

        self.hex_label = QLabel("十六进制:", self)
        self.hex_label.move(20, 140)

        self.hex_line = QLineEdit(self)
        self.hex_line.move(120, 140)
        self.hex_line.textChanged.connect(self.convert_hexadecimal)

    def convert_decimal(self):
        decimal_num = self.decimal_line.text()

        try:
            decimal_num = int(decimal_num)

            binary_num = bin(decimal_num)[2:]
            self.binary_line.setText(binary_num)

            octal_num = oct(decimal_num)[2:]
            self.octal_line.setText(octal_num)

            hexadecimal_num = hex(decimal_num)[2:]
            self.hex_line.setText(hexadecimal_num)

        except ValueError:
            self.binary_line.setText("")
            self.octal_line.setText("")
            self.hex_line.setText("")

    def convert_binary(self):
        binary_num = self.binary_line.text()

        try:
            decimal_num = int(binary_num, 2)
            self.decimal_line.setText(str(decimal_num))

            octal_num = oct(decimal_num)[2:]
            self.octal_line.setText(octal_num)

            hexadecimal_num = hex(decimal_num)[2:]
            self.hex_line.setText(hexadecimal_num)

        except ValueError:
            self.decimal_line.setText("")
            self.octal_line.setText("")
            self.hex_line.setText("")

    def convert_octal(self):
        octal_num = self.octal_line.text()

        try:
            decimal_num = int(octal_num, 8)
            self.decimal_line.setText(str(decimal_num))

            binary_num = bin(decimal_num)[2:]
            self.binary_line.setText(binary_num)

            hexadecimal_num = hex(decimal_num)[2:]
            self.hex_line.setText(hexadecimal_num)

        except ValueError:
            self.decimal_line.setText("")
            self.binary_line.setText("")
            self.hex_line.setText("")

    def convert_hexadecimal(self):
        hexadecimal_num = self.hex_line.text()

        try:
            decimal_num = int(hexadecimal_num, 16)
            self.decimal_line.setText(str(decimal_num))

            binary_num = bin(decimal_num)[2:]
            self.binary_line.setText(binary_num)

            octal_num = oct(decimal_num)[2:]
            self.octal_line.setText(octal_num)

        except ValueError:
            self.decimal_line.setText("")
            self.binary_line.setText("")
            self.octal_line.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ConverterWindow()
    window.show()
    sys.exit(app.exec_())
