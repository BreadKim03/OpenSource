from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QMessageBox, QTextEdit, QWidget, QScrollArea, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
import os
import json


def delete_schedule_by_uid(directory, target_uid):
    files = [f for f in os.listdir(directory) if f.endswith(".dat")]

    target_file = None
    for filename in files:
        try:
            uid_part = filename.split('-')[1].split('.')[0]
        except IndexError:
            continue

        if uid_part == target_uid:
            target_file = filename
            break

    if not target_file:
        print(f"UID {target_uid} 일정이 없습니다.")
        return False

    file_path = os.path.join(directory, target_file)
    try:
        os.remove(file_path)
        print(f"UID {target_uid} 일정이 삭제되었습니다.")
        return True
    except Exception as e:
        print(f"삭제 중 오류 발생: {e}")
        return False

def delete_schedule_gui(parent):
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

    # 삭제 ID 입력란과 버튼 배치
    id_layout = QHBoxLayout()
    id_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
    id_label = QLabel("삭제할 일정 ID:")
    id_edit = QLineEdit()
    id_edit.setFixedWidth(60)
    id_layout.addWidget(id_label)
    id_layout.addWidget(id_edit)
    id_layout.addStretch()
    main_dialog_layout.addLayout(id_layout)

    btn_layout = QHBoxLayout()
    delete_btn = QPushButton("삭제")
    cancel_btn = QPushButton("취소")
    btn_layout.addWidget(delete_btn)
    btn_layout.addWidget(cancel_btn)
    main_dialog_layout.addLayout(btn_layout)

    def on_delete():
        del_id = id_edit.text().strip()
        if not del_id:
            QMessageBox.warning(dialog, "입력 오류", "삭제할 ID를 입력하세요.")
            return
        try:
            del_id = f"{int(del_id):03d}"  # 숫자형으로 변환 후 3자리 문자열로 포맷팅
        except ValueError:
            QMessageBox.warning(dialog, "입력 오류", "ID는 숫자여야 합니다.")

        success = delete_schedule_by_uid(directory, del_id)
        if success:
            QMessageBox.information(dialog, "삭제 완료", f"ID {del_id} 일정이 삭제되었습니다.")
            dialog.accept()  # 창 닫기
        else:
            QMessageBox.warning(dialog, "오류", f"ID {del_id} 일정이 없습니다.")

    delete_btn.clicked.connect(on_delete)
    cancel_btn.clicked.connect(dialog.reject)

    dialog.exec()