from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("分数统计软件")
        self.resize(360, 500)

        # 设置窗口图标
        self.setWindowIcon(QIcon("icon.ico"))

        # 设置字体样式
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)

        self.name_label = QLabel("姓名:")
        self.name_label.setFont(font)
        self.name_input = QLineEdit()
        self.score_label = QLabel("分数:")
        self.score_label.setFont(font)
        self.score_input = QLineEdit()
        self.add_button = QPushButton("添加")
        self.sort_button = QPushButton("排序")
        self.table_widget = QTableWidget()

        # 设置按钮样式
        self.add_button.setStyleSheet("QPushButton { background-color: #2196F3; color: white; }"
                                       "QPushButton:hover { background-color: #1976D2; }"
                                       "QPushButton:pressed { background-color: #0D47A1; }")
        self.sort_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }"
                                        "QPushButton:hover { background-color: #388E3C; }"
                                        "QPushButton:pressed { background-color: #1B5E20; }")

        # 设置表格属性
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["姓名", "分数"])
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)  # 禁止编辑表格内容
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)  # 选择整行

        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.score_label)
        layout.addWidget(self.score_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.sort_button)
        layout.addWidget(self.table_widget)

        # 创建主窗口部件
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 存储学生信息
        self.students = []

        # 绑定按钮点击事件
        self.add_button.clicked.connect(self.add_student)
        self.sort_button.clicked.connect(self.sort_scores)

    def add_student(self):
        name = self.name_input.text()
        score = self.score_input.text()

        # 输入验证，如果姓名或分数为空则不执行添加操作
        if name.strip() == "" or score.strip() == "":
            return

        try:
            score = float(score)
        except ValueError:
            # 如果输入的成绩无法转换为浮点数，则给出提示并清空输入框
            self.score_input.clear()
            QMessageBox.warning(self, "错误", "请输入有效的分数！", QMessageBox.Ok)
            return

        # 验证姓名是否已经存在
        for student in self.students:
            if student[0] == name:
                QMessageBox.warning(self, "错误", "该姓名已存在！", QMessageBox.Ok)
                return

        self.students.append((name, score))

        row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(row_count)
        self.table_widget.setItem(row_count, 0, QTableWidgetItem(name))
        self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(score)))

        self.name_input.clear()
        self.score_input.clear()

    def sort_scores(self):
        sorted_students = sorted(self.students, key=lambda s: s[1], reverse=True)

        self.table_widget.clearContents()
        self.table_widget.setRowCount(len(sorted_students))

        for row, student in enumerate(sorted_students):
            name_item = QTableWidgetItem(student[0])
            score_item = QTableWidgetItem(str(student[1]))

            self.table_widget.setItem(row, 0, name_item)
            self.table_widget.setItem(row, 1, score_item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
