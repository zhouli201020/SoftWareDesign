from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton
import sys
import random


class TypingGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('打字程序')
        self.setWindowIcon(QIcon("Icon-A2.ico"))

        self.textLabel = QLabel()
        self.inputLineEdit = QLineEdit()
        self.accuracyLabel = QLabel()
        self.startButton = QPushButton('开始')

        # 设置字体和颜色
        font = QFont('Arial', 18)
        self.textLabel.setFont(font)
        self.accuracyLabel.setFont(font)

        font = QFont('Arial', 14)
        self.inputLineEdit.setFont(font)

        self.textLabel.setStyleSheet("QLabel { color: #333333; }")
        self.accuracyLabel.setStyleSheet("QLabel { color: #333333; }")
        self.startButton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: #FFFFFF;
                font-size: 14px;
                padding: 8px 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(QLabel('系统生成字符串:'))
        layout.addWidget(self.textLabel)
        layout.addWidget(QLabel('用户输入:'))
        layout.addWidget(self.inputLineEdit)
        layout.addWidget(QLabel('准确率:'))
        layout.addWidget(self.accuracyLabel)
        layout.addWidget(self.startButton)

        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)
        self.setLayout(layout)

        # 设置背景颜色和边框样式
        self.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
                border: 2px solid #CCCCCC;
                border-radius: 10px;
            }
        """)

        # 设置窗口大小
        self.resize(400, 300)

        self.startButton.clicked.connect(self.startGame)

    def startGame(self):
        random_string = self.generateRandomString()
        self.textLabel.setText(random_string)
        self.inputLineEdit.textChanged.connect(lambda: self.checkInput(random_string))

    def generateRandomString(self):
        length = random.randint(5, 10)
        letters = 'abcdefghijklmnopqrstuvwxyz'
        random_string = ''.join(random.choice(letters) for _ in range(length))
        return random_string

    def checkInput(self, random_string):
        input_text = self.inputLineEdit.text()
        input_length = len(input_text)
        random_length = len(random_string)
        common_length = min(input_length, random_length)
        correct_chars = sum(1 for i in range(common_length) if input_text[i] == random_string[i])
        accuracy = (correct_chars / max(input_length, random_length)) * 100
        self.accuracyLabel.setText(f'Accuracy: {accuracy:.2f} %')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = TypingGame()
    game.show()
    sys.exit(app.exec_())
