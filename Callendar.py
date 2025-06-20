import json
from datetime import datetime
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import QTimer
import sys
from GUI import Ui_MainWindow
from Callendar_GUI_add import add_schedule_gui
from Callendar_GUI_show import show_schedule_gui
from Callendar_GUI_delete import delete_schedule_gui

class CalendarApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        show_schedule_gui(self)
        self.calendarWidget.clicked.connect(self.show_schedule)
        self.pushButton.clicked.connect(self.add_schedule)
        self.pushButton_2.clicked.connect(self.delete_schedule)
        self.pushButton_3.clicked.connect(self.goto_today)

    def add_schedule(self):
        add_schedule_gui(self)
        show_schedule_gui(self)

    def show_schedule(self, date):
        show_schedule_gui(self)

    def delete_schedule(self):
        delete_schedule_gui(self)
        show_schedule_gui(self)

    def goto_today(self):
        today = datetime.today().date()
        self.calendarWidget.setSelectedDate(today)
        show_schedule_gui(self)
    
def check_upcoming_schedules(parent_widget):
    if not os.path.exists("schedules"):
        return
    
    today = datetime.today().date()
    alerted = set()

    for fname in os.listdir("schedules"):
        if not fname.endswith(".dat"):
            continue
        try:
            with open(os.path.join("schedules", fname), "r", encoding="utf-8") as f:
                data = json.load(f)
                y = int("20" + data["date"]["year"])
                m = int(data["date"]["month"])
                d = int(data["date"]["day"])
                schedule_date = datetime(y, m, d).date()

                delta = (schedule_date - today).days
                if 0 < delta <= 3 and schedule_date not in alerted:
                    alerted.add(schedule_date)
                    msg = QMessageBox(parent_widget)
                    msg.setWindowTitle("일정 알림")
                    msg.setIcon(QMessageBox.Icon.Information)
                    msg.setText(f"{m}월 {d}일 일정이 {delta}일 남았습니다!")
                    msg.exec()
        except Exception as e:
            print("오류 발생 : 알림 표시 실패", e)
            continue

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CalendarApp()
    main_window.show()
    QTimer.singleShot(100, lambda: check_upcoming_schedules(main_window))
    sys.exit(app.exec()) 
