# Author Isai Rangel Turned in  05/12/2023
# This program was based off of Lab 2 with improvements and changes
# It was used with the help of some StackOverflow articles and Pyqt5 documentation for formatting
# https://doc.qt.io/qtforpython-5/PySide2/QtGui/QFont.html
# https://stackoverflow.com/questions/6784084/how-to-pass-arguments-to-functions-by-the-click-of-button-in-pyqt
# https://pythonprogramminglanguage.com/pyqt5-button/
# https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QMessageBox.html
# I also used the lectures and notes for references  .
import sys
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSpinBox, QMessageBox, \
    QInputDialog, QHBoxLayout, QTextEdit, QScrollArea
# ------------------
# Purpose:
# This program will allow a professor calculate students grades as well as the class as a whole.
# User will enter subject of the class.
# User will enter how many students and their grades
# Output will be the letter grade of each student andthe average of the class
# -------------------

# Grade Calculator Widget
class GradeCalculator(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('UNO Class Calculator')
        self.setFixedSize(300,500)
        self.GradeCalc_layout = QVBoxLayout()
        # Heading label and formatting
        self.heading_label = QLabel("This will calculate up to 30 individual student's grades "  
                    "\nand the average of your class.\n")   # HeadingLabel
        self.heading_label.setFont(QFont("Helvetica Neue", 11, QFont.Light, italic=True))
        self.GradeCalc_layout.addWidget(self.heading_label)
        # Subject label and input formatting
        self.subject_label = QLabel('Subject:')     # Subject Label
        self.subject_label.setStyleSheet("QLabel { border: 2px solid darkred; background-color:"
                    "darkred; color: white; }")
        self.subject_label.setFont(QFont('Optima', 20, QFont.Bold))
        self.subject_input = QLineEdit(self)
        self.subject_input.setFixedWidth(200)
        self.GradeCalc_layout.addWidget(self.subject_label)
        self.GradeCalc_layout.addWidget(self.subject_input)
        # Number of students label and input formatting
        self.studentCount_label = QLabel('Number of Students:')     # Student count label
        self.studentCount_label.setFont(QFont('Optima', 20, QFont.Bold))
        self.studentCount_label.setStyleSheet("QLabel { border: 2px solid darkred; background-color: "
            "darkred; color: white; }")
        self.studentCount_input = QSpinBox()       # Student count input SpinBox
        self.studentCount_input.setFixedWidth(40)
        self.studentCount_input.setMinimum(0)
        self.studentCount_input.setMaximum(30)
        self.GradeCalc_layout.addWidget(self.studentCount_label)
        self.GradeCalc_layout.addWidget(self.studentCount_input)
        # Calculate button and formatting
        self.calculate_button = QPushButton('Calculate')
        self.calculate_button.setFixedSize(90, 30)
        self.calculate_button.clicked.connect(self.calculate_grades) # Calculate button-clicked
        self.calculate_button_layout = QHBoxLayout()
        self.calculate_button_layout.addStretch(1)
        self.calculate_button_layout.addStretch(1)
        self.GradeCalc_layout.addWidget(self.calculate_button, alignment=Qt.AlignCenter)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        # Insert results
        print_results = QScrollArea()
        print_results.setWidget(self.result_text)
        print_results.setWidgetResizable(True)
        # Results label and formatting
        self.result_heading_label = QLabel('Results:')
        self.result_heading_label.setStyleSheet("QLabel { border: 2px solid darkRED; background-color: "
                "darkRED; color: white; }")
        self.result_heading_label.setFont(QFont('Optima', 20, QFont.Bold))
        self.GradeCalc_layout.addWidget(self.result_heading_label)
        self.GradeCalc_layout.addWidget(print_results)
        # Clear button formatting
        self.clear_button = QPushButton('Clear')
        self.clear_button.setFixedSize(90, 30)
        self.clear_button.clicked.connect(self.clear_results)
        self.clear_button_layout = QHBoxLayout()
        self.GradeCalc_layout.addWidget(self.clear_button, alignment=Qt.AlignRight)

        self.setLayout(self.GradeCalc_layout)

    # Calculate letter grade based on numerical grade
    def calculate_grades(self) -> None:
        subject: str = self.subject_input.text()
        if not subject.replace(" ", "").isalpha():  # Ensure valid subject
            QMessageBox.warning(self, 'Invalid Input', 'Subject must only contain letters and spaces.')
            return
        student_count = self.studentCount_input.value()

        if student_count == 0:
            QMessageBox.warning(self, 'Invalid Input', 'Number of students must be greater than zero.')
            return
        grade_inputs = []

        for i in range(1, student_count + 1):   # Get student numerical points
            grade, ok = QInputDialog.getInt(self, f'Student {i}', f'Enter the grade for Student {i}:'
            f'\nvalue(s) must be between 0-100', 0, 0, 100)
            if not ok:
                return
            grade_inputs.append(grade)

        grade_labels = []
        total_grades = 0
        for i, grade in enumerate(grade_inputs):
            letter_grade = self.calculate_letter_grade(grade)
            grade_labels.append(f'Student {i + 1} score is {grade} and grade is {letter_grade}')
            total_grades += grade

        class_average = total_grades / student_count
        grade_labels.append(f'Class Average: {class_average:.2f}')
        self.result_text.setText('\n'.join(grade_labels))
        self.result_text.setFont(QFont('Optima', 15))

    # Convert numerical points to letter grade
    def calculate_letter_grade(self, numeric_grade: int) -> str:
        if numeric_grade >= 90:
            return 'A'
        elif numeric_grade >= 80:
            return 'B'
        elif numeric_grade >= 70:
            return 'C'
        elif numeric_grade >= 60:
            return 'D'
        else:
            return 'F'
    # clear all inputs
    def clear_results(self) -> None:
        self.result_text.clear()
        self.subject_input.clear()
        self.studentCount_input.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = GradeCalculator()
    calculator.show()
    sys.exit(app.exec_())
