import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class BillingProgram(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("电信计费程序")
        self.setGeometry(300, 300, 300, 200)

        self.generate_button = QPushButton("生成费用文件", self)
        self.generate_button.clicked.connect(self.generate_billing_file)
        self.generate_button.setGeometry(50, 50, 200, 50)

    def generate_billing_file(self):
        hd_file_path = "hd.txt"
        fl_file_path = "fl.txt"
        fy_file_path = "fy.txt"

        try:
            hd_file = open(hd_file_path, "r")
            fl_file = open(fl_file_path, "r")
            fy_file = open(fy_file_path, "w")


            rate_dict = {}
            for line in fl_file:
                area_code, rate = line.strip().split()
                rate_dict[area_code] = float(rate)

            for line in hd_file:
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BillingProgram()
    window.show()
    sys.exit(app.exec_())
