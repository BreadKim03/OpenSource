from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QMessageBox, QTextEdit, QWidget, QScrollArea, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
import os
import json


def get_uid(parent, dir, files, content):
    for fname in files:
        path = os.path.join(dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if data['schedule'] == content:break
    return data['unique_id']

def delete_schedule_gui(parent):
    date = parent.calendarWidget.selectedDate().toPyDate()
    directory = "schedules"
    if not os.path.exists(directory):
        QMessageBox.warning(parent, "오류", "일정 디렉토리가 존재하지 않습니다.")
        return
    files = [f for f in os.listdir(directory) if f.endswith(".dat") and f.startswith(f"{date.year % 100:02d}{date.month:02d}{date.day:02d}")]
    delete = []
    for row in range(parent.tableWidget.rowCount()):
        chk_item = parent.tableWidget.item(row, 0)
        if chk_item and chk_item.checkState() == Qt.CheckState.Checked:
            for fname in files:
                path = os.path.join(directory, fname)
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if data['schedule'] == parent.tableWidget.item(row, 1).text():
                    delete.append(data['unique_id'])
    if not delete:
        QMessageBox.information(parent, "선택 항목 없음", "삭제 대상이 없습니다.")
        return
    del_count = 0
    for uid in delete:
        for fname in files:
            if uid==fname.split('-')[1].split('.')[0]:
                try:os.remove(directory + '/' + fname)
                except Exception as e:
                    QMessageBox.warning(parent, "삭제 오류", f"{fname} 삭제에 실패했습니다\n{e}")
                    return
        del_count += 1
    if del_count > 0:QMessageBox.information(parent, "삭제 완료", f"총 {del_count}개의 일정이 삭제되었습니다.")
    else:QMessageBox.information(parent, "삭제 실패", "일정 삭제에 실패하였습니다.")
