import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("学生成绩核算系统")
        self.setGeometry(100, 100, 1000, 400)
        self.setWindowIcon(QIcon("icon.ico"))

        self.table = QTableWidget(self)
        self.table.setGeometry(20, 20, 960, 300)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['学号', '平时成绩', '期中成绩', '期末成绩', '总评成绩', '等级', ''])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnHidden(6, True)

        self.file_imported = False
        self.grades_calculated = False

        import_button = QPushButton("导入成绩文件", self)
        import_button.setGeometry(20, 330, 120, 30)
        import_button.clicked.connect(self.import_grades)

        calculate_button = QPushButton("计算总评成绩", self)
        calculate_button.setGeometry(150, 330, 120, 30)
        calculate_button.clicked.connect(self.calculate_grades)

        class_average_button = QPushButton("计算班级总平均成绩", self)
        class_average_button.setGeometry(280, 330, 180, 30)
        class_average_button.clicked.connect(self.calculate_class_average)

        output_button = QPushButton("输出成绩信息", self)
        output_button.setGeometry(470, 330, 120, 30)
        output_button.clicked.connect(self.output_summary)

        grade_counts_button = QPushButton("统计各等级人数和占比", self)
        grade_counts_button.setGeometry(600, 330, 200, 30)
        grade_counts_button.clicked.connect(self.calculate_grade_counts)

    def import_grades(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "文本文件 (*.txt)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                lines = file.readlines()[1:]  # 跳过第一行，获取成绩信息
                self.table.setRowCount(len(lines))
                for i, line in enumerate(lines):
                    student_info = line.split()
                    student_id = student_info[0]
                    regular_score = student_info[1]
                    midterm_score = student_info[2]
                    final_score = student_info[3]
                    self.table.setItem(i, 0, QTableWidgetItem(student_id))
                    self.table.setItem(i, 1, QTableWidgetItem(regular_score))
                    self.table.setItem(i, 2, QTableWidgetItem(midterm_score))
                    self.table.setItem(i, 3, QTableWidgetItem(final_score))

            self.file_imported = True

    def calculate_grades(self):
        if not self.file_imported:
            QMessageBox.warning(self, "提示", "请先导入成绩文件！")
            return

        for i in range(self.table.rowCount()):
            regular_score = float(self.table.item(i, 1).text())
            midterm_score = float(self.table.item(i, 2).text())
            final_score = float(self.table.item(i, 3).text())
            total_score = 0.3 * regular_score + 0.3 * midterm_score + 0.4 * final_score
            grade = self.get_grade(total_score)
            total_score_item = QTableWidgetItem("{:.2f}".format(total_score))
            grade_item = QTableWidgetItem(grade)
            self.table.setItem(i, 4, total_score_item)
            self.table.setItem(i, 5, grade_item)

        self.grades_calculated = True

    def calculate_class_average(self):
        if not self.grades_calculated:
            QMessageBox.warning(self, "提示", "请先计算总评成绩！")
            return

        total_scores = []
        for i in range(self.table.rowCount()):
            total_score_item = self.table.item(i, 4)
            if total_score_item:
                total_scores.append(float(total_score_item.text()))

        if total_scores:
            class_average = sum(total_scores) / len(total_scores)
            QMessageBox.information(self, "班级总平均成绩", f"班级总平均成绩为：{class_average:.2f}")
        else:
            QMessageBox.warning(self, "提示", "没有可计算的成绩！")

    def calculate_grade_counts(self):
        if not self.grades_calculated:
            QMessageBox.warning(self, "提示", "请先计算总评成绩！")
            return

        grade_counts = {'优': 0, '良': 0, '中': 0, '及格': 0, '不及格': 0}
        total_students = self.table.rowCount()

        for i in range(self.table.rowCount()):
            grade = self.table.item(i, 5).text()
            grade_counts[grade] += 1

        percentages = {grade: count / total_students * 100 for grade, count in grade_counts.items()}

        message = "各等级人数和占比：\n\n"
        for grade, count in grade_counts.items():
            percentage = percentages[grade]
            message += f"{grade}：{count}人，占比：{percentage:.2f}%\n"

        QMessageBox.information(self, "统计结果", message)

    def get_grade(self, score):
        if score >= 90:
            return "优"
        elif score >= 80:
            return "良"
        elif score >= 70:
            return "中"
        elif score >= 60:
            return "及格"
        else:
            return "不及格"

    def output_summary(self):
        if not self.grades_calculated:
            QMessageBox.warning(self, "提示", "请先计算总评成绩！")
            return

        summary = {'优': [], '良': [], '中': [], '及格': [], '不及格': []}
        for i in range(self.table.rowCount()):
            student_id = self.table.item(i, 0).text()
            total_score = float(self.table.item(i, 4).text())
            grade = self.table.item(i, 5).text()
            summary[grade].append((student_id, total_score))

        with open('summary.txt', 'w', encoding='utf-8') as file:
            file.write("优秀学生：\n")
            for student in summary['优']:
                file.write(f"学号：{student[0]}，总评成绩：{student[1]}\n")

            file.write("\n良好学生：\n")
            for student in summary['良']:
                file.write(f"学号：{student[0]}，总评成绩：{student[1]}\n")

            file.write("\n中等学生：\n")
            for student in summary['中']:
                file.write(f"学号：{student[0]}，总评成绩：{student[1]}\n")

            file.write("\n及格学生：\n")
            for student in summary['及格']:
                file.write(f"学号：{student[0]}，总评成绩：{student[1]}\n")

            file.write("\n不及格学生：\n")
            for student in summary['不及格']:
                file.write(f"学号：{student[0]}，总评成绩：{student[1]}\n")

        QMessageBox.information(self, "提示", "成绩信息已成功输出到 summary.txt 文件中。")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
