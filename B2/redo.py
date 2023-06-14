import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QLabel, QLineEdit, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

class BillingProgram(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("电信计费程序")
        self.setGeometry(300, 300, 800, 600)

        self.generate_button = QPushButton("生成费用文件", self)
        self.generate_button.clicked.connect(self.generate_billing_file)
        self.generate_button.setGeometry(50, 50, 200, 50)

        self.query_button = QPushButton("话单查询", self)
        self.query_button.clicked.connect(self.query_call_records)
        self.query_button.setGeometry(50, 120, 200, 50)

        self.bill_query_button = QPushButton("话费查询", self)
        self.bill_query_button.clicked.connect(self.query_bill)
        self.bill_query_button.setGeometry(50, 190, 200, 50)

        self.number_label = QLabel("电话号码:", self)
        self.number_label.setGeometry(50, 260, 100, 30)

        self.number_input = QLineEdit(self)
        self.number_input.setGeometry(150, 260, 150, 30)

        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(50, 300, 700, 250)
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["用户名", "主叫电话号码", "被叫电话号码", "通话时长", "话费总计"])
        self.table_widget.setColumnHidden(4, True)

    def generate_billing_file(self):
        hd_file_path = "hd.txt"
        fl_file_path = "fl.txt"
        fy_file_path = "fy.txt"

        try:
            hd_file = open(hd_file_path, "r")
            fl_file = open(fl_file_path, "r")
            fy_file = open(fy_file_path, "w", encoding="utf-8")

            #fy_file.write("主叫电话号码 通话类型 话费金额\n")

            rate_dict = {}
            for line in fl_file:
                area_code, rate = line.strip().split()
                rate_dict[area_code] = float(rate)

            line_count = sum(1 for _ in hd_file)
            hd_file.seek(0)

            for i, line in enumerate(hd_file):
                call_info = line.strip().split()
                caller_area_code = call_info[0]
                caller_number = call_info[1]
                callee_area_code = call_info[2]
                callee_number = call_info[3]
                duration = int(call_info[4])

                if caller_area_code == callee_area_code:
                    call_type = "本地"
                    local_cost = self.calculate_local_cost(duration)
                    total_cost = local_cost
                else:
                    call_type = "长途"
                    long_distance_cost = self.calculate_long_distance_cost(duration, rate_dict[callee_area_code])
                    total_cost = long_distance_cost

                if i == line_count - 1:
                    fy_file.write(f"{caller_number} {call_type} {total_cost:.2f}")
                else:
                    fy_file.write(f"{caller_number} {call_type} {total_cost:.2f}\n")

            fy_file.close()
            hd_file.close()
            fl_file.close()

            QMessageBox.information(self, "成功", "费用文件生成成功")
        except FileNotFoundError:
            QMessageBox.warning(self, "错误", "源数据文件或费率文件不存在")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"生成费用文件时发生错误: {str(e)}")

    def calculate_local_cost(self, duration):
        if duration <= 180:
            return 0.5
        else:
            additional_minutes = (duration - 180) // 180
            return 0.5 + additional_minutes * 0.2

    def calculate_long_distance_cost(self, duration, rate):
        minutes = (duration + 59) // 60
        return rate * minutes

    def query_call_records(self):
        number = self.number_input.text()

        try:
            hd_file_path = "hd.txt"
            fy_file_path = "fy.txt"
            yh_file_path = "yh.txt"

            hd_file = open(hd_file_path, "r", encoding="utf-8")
            fy_file = open(fy_file_path, "r", encoding="utf-8")
            yh_file = open(yh_file_path, "r", encoding="utf-8")

            call_records = []
            user_dict = {}

            for line in yh_file:
                phone_number, user_name = line.strip().split()
                user_dict[phone_number] = user_name

            for line in hd_file:
                call_info = line.strip().split()
                caller_number = call_info[1]
                callee_number = call_info[3]
                duration = call_info[4]

                if caller_number == number or callee_number == number:
                    user_name = user_dict.get(number, "")
                    call_records.append((user_name, caller_number, callee_number, duration))

            self.display_call_records(call_records)

            hd_file.close()
            fy_file.close()
            yh_file.close()
        except FileNotFoundError:
            QMessageBox.warning(self, "错误", "源数据文件或用户文件不存在")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"查询话单时发生错误: {str(e)}")

    def query_bill(self):
        number = self.number_input.text()

        try:
            fy_file_path = "fy.txt"
            yh_file_path = "yh.txt"

            fy_file = open(fy_file_path, "r", encoding="utf-8")
            yh_file = open(yh_file_path, "r", encoding="utf-8")

            user_dict = {}
            local_cost = 0
            long_distance_cost = 0

            for line in yh_file:
                phone_number, user_name = line.strip().split()
                user_dict[phone_number] = user_name

            for line in fy_file:
                call_info = line.strip().split()
                caller_number = call_info[0]
                call_type = call_info[1]
                cost = float(call_info[2])

                if caller_number == number:
                    if call_type == "本地":
                        local_cost += cost
                    elif call_type == "长途":
                        long_distance_cost += cost

            total_cost = local_cost + long_distance_cost
            user_name = user_dict.get(number, "")

            QMessageBox.information(self, "话费查询结果", f"用户名: {user_name}\n电话号码: {number}\n本地话费: {local_cost:.2f}\n长途话费: {long_distance_cost:.2f}\n话费总计: {total_cost:.2f}")

            fy_file.close()
            yh_file.close()
        except FileNotFoundError:
            QMessageBox.warning(self, "错误", "费用文件或用户文件不存在")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"话费查询时发生错误: {str(e)}")

    def display_call_records(self, call_records):
        self.table_widget.setRowCount(0)

        for row, record in enumerate(call_records):
            self.table_widget.insertRow(row)
            for col, data in enumerate(record):
                self.table_widget.setItem(row, col, QTableWidgetItem(str(data)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BillingProgram()
    window.show()
    sys.exit(app.exec_())
