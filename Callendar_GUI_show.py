from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6 import QtCore
import os
import json

def show_schedule_gui(parent):
    todo = parent.tableWidget
    selected_date = parent.calendarWidget.selectedDate().toPyDate()
    y = f"{selected_date.year % 100:02d}"
    m = f"{selected_date.month:02d}"
    d = f"{selected_date.day:02d}"
    item = QTableWidgetItem("")
    directory = "schedules"
    if not os.path.exists(directory):
        os.makedirs("schedules", exist_ok=True)
        todo.setRowCount(1)
        todo.setItem(0, 0, item)
        todo.setItem(0, 1, QTableWidgetItem(""))

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
        todo.setRowCount(1)
        todo.setItem(0, 0, item)
        todo.setItem(0, 1, QTableWidgetItem(""))

    for i, data in enumerate(matched):
        hour = data['date']['hour']
        minute = data['date']['minute']
        content = data['schedule']
        todo.setRowCount(i + 1)
        item = QTableWidgetItem(f"{hour}:{minute}")
        preset(item)
        todo.setItem(i, 0, QTableWidgetItem(item))
        todo.setItem(i, 1, QTableWidgetItem(content))
    
def preset(item):
    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    item.setCheckState(QtCore.Qt.CheckState.Unchecked)