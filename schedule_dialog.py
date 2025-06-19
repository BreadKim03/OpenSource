from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton

class ScheduleDialog(QDialog):
    def __init__(self, date_str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("일정 추가")
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel(f"{date_str} 일정 내용 입력"))

        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)

        self.save_button = QPushButton("저장")
        self.save_button.clicked.connect(self.accept)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def get_text(self):
        return self.text_edit.toPlainText()