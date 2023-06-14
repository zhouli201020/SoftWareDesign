from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys


class EncryptionProgram(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("加密程序")
        self.setWindowIcon(QIcon("icon.ico"))

        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)

        self.plain_text_label = QLabel("明文：")
        self.plain_text_label.setFont(title_font)
        self.plain_text_input = QLineEdit()

        self.key_label = QLabel("密钥：")
        self.key_label.setFont(title_font)
        self.key_input = QLineEdit()

        self.encrypt_button = QPushButton("加密")
        self.encrypt_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.encrypt_button.clicked.connect(self.encrypt)

        self.result_label = QLabel("密文：")
        self.result_label.setFont(title_font)
        self.result_output = QLabel()
        self.result_output.setStyleSheet("background-color: white; border: 1px solid #ccc; padding: 5px;")

        layout = QVBoxLayout()
        layout.addWidget(self.plain_text_label)
        layout.addWidget(self.plain_text_input)
        layout.addWidget(self.key_label)
        layout.addWidget(self.key_input)
        layout.addWidget(self.encrypt_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_output)

        self.setLayout(layout)

    def encrypt(self):
        plain_text = self.plain_text_input.text()
        key = self.key_input.text()

        # 输入验证
        if not plain_text:
            self.show_error_message("请输入明文")
            return

        if not key:
            self.show_error_message("请输入密钥")
            return

        try:
            key = int(key)
        except ValueError:
            self.show_error_message("密钥必须为整数")
            return

        # 加密
        encrypted_text = ""
        for char in plain_text:
            encrypted_char = chr(ord(char) + key)
            encrypted_text += encrypted_char

        self.result_output.setText(encrypted_text)

    def show_error_message(self, message):
        error_message = QMessageBox()
        error_message.setIcon(QMessageBox.Critical)
        error_message.setText("错误")
        error_message.setInformativeText(message)
        error_message.setWindowTitle("错误")
        error_message.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    program = EncryptionProgram()
    program.show()
    sys.exit(app.exec_())
