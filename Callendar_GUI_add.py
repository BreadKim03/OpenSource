from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QHBoxLayout, QComboBox
)
from PyQt6.QtCore import Qt
from datetime import datetime
import os
import json

def add_schedule_gui(parent):
    dialog = QDialog(parent)
    dialog.setWindowTitle("일정 추가")
    dialog.setFixedSize(300, 120)

    layout = QVBoxLayout(dialog)
    layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

    # 선택된 날짜 출력
    date = parent.calendarWidget.selectedDate().toPyDate()
    date_str = f"{date.year}년 {date.month}월 {date.day}일"
    layout.addWidget(QLabel(f"선택한 날짜: {date_str}"))

    # 시간 및 분 선택 (ComboBox)
    hour_combo = QComboBox()
    for i in range(24):
        hour_combo.addItem(f"{i:02d}")
    hour_combo.setCurrentIndex(datetime.now().hour)

    minute_combo = QComboBox()
    for i in range(0, 60, 5):
        minute_combo.addItem(f"{i:02d}")
    minute_combo.setCurrentIndex(datetime.now().minute // 5)

    time_layout = QHBoxLayout()
    time_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
    time_layout.addWidget(QLabel("시:"))
    time_layout.addWidget(hour_combo)
    time_layout.addWidget(QLabel("분:"))
    time_layout.addWidget(minute_combo)
    layout.addLayout(time_layout)

    # 일정 내용 입력 (한 줄에 "일정 내용:" 레이블 + 입력란)
    content_layout = QHBoxLayout()
    content_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
    content_layout.addWidget(QLabel("일정 내용:"))
    content_edit = QLineEdit()
    content_layout.addWidget(content_edit)
    layout.addLayout(content_layout)

    # 등록 / 취소 버튼
    button_layout = QHBoxLayout()
    save_btn = QPushButton("등록")
    cancel_btn = QPushButton("취소")

    def on_save():
        content = content_edit.text()
        if not content.strip():
            QMessageBox.warning(parent, "입력 오류", "일정 내용을 입력해주세요.")
            return
        y, m, d = f"{date.year % 100:02d}", f"{date.month:02d}", f"{date.day:02d}"
        h = hour_combo.currentText()
        mi = minute_combo.currentText()
        uid = generate_global_uid()
        filepath = save_file(y, m, d, h, mi, uid, content)
        QMessageBox.information(parent, "저장 완료", f"일정이 저장되었습니다:\n{filepath}")
        save_btn.setEnabled(False)  # 중복 저장 방지
        dialog.accept()

    save_btn.clicked.connect(on_save)
    cancel_btn.clicked.connect(dialog.reject)

    button_layout.addWidget(save_btn)
    button_layout.addWidget(cancel_btn)
    layout.addLayout(button_layout)

    dialog.exec()

# def generate_id(y, m, d, h, mi):
#     directory = "schedules"
#     os.makedirs(directory, exist_ok=True)
#     files = os.listdir(directory)
#     prefix = f"{y}{m}{d}{h}{mi}"
#     uids = [
#         int(f.split('-')[1].split('.dat')[0])
#         for f in files
#         if f.startswith(prefix) and f.endswith(".dat")
#     ]
#     new_id = (max(uids) + 1 if uids else 1) % 1000
#     if new_id == 0:
#         new_id = 1
#     return f"{new_id:03d}"

def generate_global_uid():
    counter_file = "schedules/uid_counter.txt"
    os.makedirs("schedules", exist_ok=True)

    if not os.path.exists(counter_file):
        with open(counter_file, 'w') as f:
            f.write("1")
        return "001"

    with open(counter_file, 'r+') as f:
        uid = int(f.read().strip())
        new_uid = uid + 1
        if new_uid == 0:
            new_uid = 1
        f.seek(0)
        f.write(str(new_uid))
        f.truncate()
        return f"{new_uid:03d}"

def save_file(year, month, day, h, m, uid, content):
    directory = "schedules"
    os.makedirs(directory, exist_ok=True)

    filename = f"{year}{month}{day}{h}{m}-{uid}.dat"
    filepath = os.path.join(directory, filename)

    data = {
        "unique_id": uid,
        "date": {
            "year": year,
            "month": month,
            "day": day,
            "hour": h,
            "minute": m
        },
        "schedule": content
    }
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return filepath