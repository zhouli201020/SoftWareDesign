import sys
import os

from PyQt5 import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QMessageBox, QTextEdit, \
    QScrollArea


class TelecomBillingProgram(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("电信计费程序")
        self.setGeometry(100, 100, 400, 350)

        self.label = QLabel("电话号码:", self)
        self.label.setGeometry(20, 20, 100, 20)

        self.line_edit = QLineEdit(self)
        self.line_edit.setGeometry(120, 20, 200, 20)

        self.generate_button = QPushButton("生成费用文件", self)
        self.generate_button.setGeometry(120, 60, 120, 30)
        self.generate_button.clicked.connect(self.generate_billing_file)

        self.query_button = QPushButton("查询费用", self)
        self.query_button.setGeometry(250, 60, 70, 30)
        self.query_button.clicked.connect(self.calculate_billing)

        self.query_records_button = QPushButton("查询话单", self)
        self.query_records_button.setGeometry(120, 100, 200, 30)
        self.query_records_button.clicked.connect(self.query_call_records)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(20, 140, 360, 180)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.scroll_area.setWidget(self.text_edit)

        self.default_path = os.getcwd()  # 获取当前工作目录

    def generate_billing_file(self):
        billing_file = 'fy.txt'

        if os.path.exists(billing_file):
            QMessageBox.warning(self, "警告", "费用文件已存在")
            return

        rate_data = {}
        try:
            with open('fl.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    area_code, rate = line.strip().split()
                    rate_data[area_code] = float(rate)
        except FileNotFoundError:
            QMessageBox.warning(self, "警告", "找不到费率文件")
            return
        except UnicodeDecodeError as e:
            QMessageBox.warning(self, "警告", "无法打开费率文件: " + str(e))
            return
        except Exception as e:
            QMessageBox.warning(self, "警告", "打开费率文件时发生错误: " + str(e))
            return

        call_records = []
        with open('hd.txt', 'r', encoding='utf-8') as file:
            for line in file:
                record = line.strip().split()
                if len(record) != 5:
                    QMessageBox.warning(self, "警告", "通话记录格式不正确")
                    return

                caller_area, caller_number, receiver_area, receiver_number, duration = record
                call_type = "本地" if caller_area == receiver_area else "长途"
                local_cost = self.calculate_local_cost(int(duration))
                long_distance_cost = self.calculate_long_distance_cost(int(duration), rate_data.get(receiver_area, 0))
                total_cost = local_cost + long_distance_cost
                call_record = f"{caller_number} {call_type} {total_cost:.2f}"
                call_records.append(call_record)

        if not call_records:
            QMessageBox.warning(self, "警告", "没有可计费的通话记录")
            return

        try:
            with open(billing_file, 'w', encoding='utf-8') as file:
                file.write("\n".join(call_records))
        except Exception as e:
            QMessageBox.warning(self, "警告", "保存费用文件时发生错误: " + str(e))
            return

        QMessageBox.information(self, "提示", "费用文件生成成功")

    def calculate_local_cost(self, duration):
        if duration <= 180:
            return 0.5
        else:
            minutes = duration // 60
            additional_minutes = minutes - 3
            return 0.5 + additional_minutes * 0.2

    def calculate_long_distance_cost(self, duration, rate):
        minutes = (duration + 59) // 60
        return rate * minutes

    def calculate_billing(self):
        phone_number = self.line_edit.text().strip()
        if not phone_number:
            QMessageBox.warning(self, "警告", "请输入电话号码")
            return

        billing_file = 'fy.txt'
        if not os.path.exists(billing_file):
            QMessageBox.warning(self, "警告", "费用文件不存在，请先生成费用文件")
            return

        user_data = {}
        try:
            with open('yh.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    number, username = line.strip().split()
                    user_data[number] = username
        except FileNotFoundError:
            QMessageBox.warning(self, "警告", "找不到用户文件")
            return
        except UnicodeDecodeError as e:
            QMessageBox.warning(self, "警告", "无法打开用户文件: " + str(e))
            return
        except Exception as e:
            QMessageBox.warning(self, "警告", "打开用户文件时发生错误: " + str(e))
            return

        total_local_cost = 0
        total_long_distance_cost = 0

        with open(billing_file, 'r', encoding='utf-8') as file:
            for line in file:
                record = line.strip().split()
                if len(record) != 3:
                    QMessageBox.warning(self, "警告", "费用记录格式不正确")
                    return

                current_phone_number, call_type, cost = record
                if current_phone_number == phone_number:
                    if call_type == "本地":
                        total_local_cost += float(cost)
                    elif call_type == "长途":
                        total_long_distance_cost += float(cost)

        username = user_data.get(phone_number, "未知用户")
        total_cost = total_local_cost + total_long_distance_cost
        result_text = f"用户名: {username}\n电话号码: {phone_number}\n本地话费: {total_local_cost:.2f}\n长途话费: {total_long_distance_cost:.2f}\n话费总计: {total_cost:.2f}"
        QMessageBox.information(self, "费用查询结果", result_text)

    def query_call_records(self):
        phone_number = self.line_edit.text().strip()
        if not phone_number:
            QMessageBox.warning(self, "警告", "请输入电话号码")
            return

        user_data = {}
        try:
            with open('yh.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    number, username = line.strip().split()
                    user_data[number] = username
        except FileNotFoundError:
            QMessageBox.warning(self, "警告", "找不到用户文件")
            return
        except UnicodeDecodeError as e:
            QMessageBox.warning(self, "警告", "无法打开用户文件: " + str(e))
            return
        except Exception as e:
            QMessageBox.warning(self, "警告", "打开用户文件时发生错误: " + str(e))
            return

        call_records = []
        with open('hd.txt', 'r', encoding='utf-8') as file:
            for line in file:
                record = line.strip().split()
                if len(record) != 5:
                    QMessageBox.warning(self, "警告", "通话记录格式不正确")
                    return

                caller_area, caller_number, receiver_area, receiver_number, duration = record
                username = user_data.get(caller_number, "未知用户")
                call_record = f"用户名: {username}\n主叫电话: {caller_number}\n被叫电话: {receiver_number}\n通话时长: {duration}"
                if caller_number == phone_number or receiver_number == phone_number:
                    call_records.append(call_record)

        if not call_records:
            QMessageBox.warning(self, "警告", "未找到该电话号码的通话记录")
            return

        result_text = "\n\n".join(call_records)
        self.text_edit.setPlainText(result_text)

        self.scroll_area.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TelecomBillingProgram()
    window.show()
    sys.exit(app.exec_())
