from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QMessageBox, QTextEdit, QWidget, QScrollArea
import os
import json

def show_schedule_gui(parent):
    selected_date = parent.calendarWidget.selectedDate().toPyDate()
    y = f"{selected_date.year % 100:02d}"
    m = f"{selected_date.month:02d}"
    d = f"{selected_date.day:02d}"

    directory = "schedules"
    if not os.path.exists(directory):
        QMessageBox.warning(parent, "오류", "일정 디렉토리가 존재하지 않습니다.")
        return

    files = [f for f in os.listdir(directory) if f.endswith(".dat")]
    matched = []

    for fname in files:
        if fname.startswith(f"{y}{m}{d}"):
            filepath = os.path.join(directory, fname)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    matched.append(data)
            except Exception:
                continue

    if not matched:
        QMessageBox.information(parent, "일정 없음", f"{selected_date.year}년 {selected_date.month}월 {selected_date.day}일 일정이 없습니다.")
        return

    # 일정 목록 출력용 다이얼로그
    dialog = QDialog(parent)
    dialog.setWindowTitle("일정 조회")
    dialog.setFixedSize(400, 300)

    main_dialog_layout = QVBoxLayout(dialog)

    content_widget = QWidget()

    content_layout = QVBoxLayout(content_widget)
    content_layout.setSpacing(0)
    content_layout.setContentsMargins(0, 0, 0, 0)

    title_label = QLabel(f"{selected_date.year}년 {selected_date.month}월 {selected_date.day}일 일정 목록")
    content_layout.addWidget(title_label)

    for data in matched:
        uid = data['unique_id']
        hour = data['date']['hour']
        minute = data['date']['minute']
        content = data['schedule']
        label_text = f"[{hour}:{minute}] 일정 : {content} (ID : {uid})"
        schedule_label = QLabel(label_text)
        content_layout.addWidget(schedule_label)

    content_layout.addStretch()

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(content_widget)

    main_dialog_layout.addWidget(scroll_area)

    dialog.exec()