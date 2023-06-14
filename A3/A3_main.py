from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QFont, QIcon
import sys


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文本编辑器")
        self.setGeometry(100, 100, 800, 600)

        self.text_edit = QTextEdit(self)
        self.text_edit.setFont(QFont("Arial", 16))  # 设置字体大小为16
        self.setCentralWidget(self.text_edit)

        self.create_menu()

        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F0F0;
            }

            QTextEdit {
                background-color: white;
                color: #333333;
                font-family: Arial;
            }
        """)

        self.current_file_path = ""

    def create_menu(self):
        menubar = self.menuBar()

        # 创建文件菜单
        file_menu = menubar.addMenu("文件")

        # 新建菜单项
        new_action = QAction("新建", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        # 打开菜单项
        open_action = QAction("打开", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # 保存菜单项
        save_action = QAction("保存", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

    def new_file(self):
        self.text_edit.clear()
        self.current_file_path = ""

    def open_file(self):
        if self.check_save_changes():
            file_path, _ = QFileDialog.getOpenFileName(self, "打开文件")
            if file_path:
                try:
                    with open(file_path, "r") as file:
                        content = file.read()
                        self.text_edit.setText(content)
                        self.current_file_path = file_path
                except Exception as e:
                    QMessageBox.critical(self, "错误", "无法打开文件：{}".format(e))

    def save_file(self):
        if not self.current_file_path:
            file_path, _ = QFileDialog.getSaveFileName(self, "保存文件", filter="Text Files (*.txt)")
            if file_path:
                self.current_file_path = file_path
            else:
                return

        try:
            with open(self.current_file_path, "w") as file:
                file.write(self.text_edit.toPlainText())
                self.text_edit.document().setModified(False)  # 保存后将编辑状态设为未修改
                QMessageBox.information(self, "提示", "文件保存成功")
        except Exception as e:
            QMessageBox.critical(self, "错误", "无法保存文件：{}".format(e))

    def closeEvent(self, event):
        if self.text_edit.document().isModified():
            reply = QMessageBox.question(self, "保存文件", "是否保存文件？",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.save_file()
            elif reply == QMessageBox.Cancel:
                event.ignore()
                return

        event.accept()

    def check_save_changes(self):
        if self.text_edit.document().isModified():
            reply = QMessageBox.question(self, "保存文件", "是否保存文件？",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.save_file()
                return True
            elif reply == QMessageBox.No:
                return True
            elif reply == QMessageBox.Cancel:
                return False
        else:
            return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = TextEditor()
    window.show()
    sys.exit(app.exec_())
