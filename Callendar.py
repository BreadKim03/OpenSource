import json
from datetime import datetime
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
from GUI import Ui_MainWindow
from Callendar_GUI_add import add_schedule_gui
from Callendar_GUI_show import show_schedule_gui
from Callendar_GUI_delete import delete_schedule_gui

class CalendarApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.add_schedule)
        self.pushButton_2.clicked.connect(self.show_schedule)
        self.pushButton_3.clicked.connect(self.delete_schedule)
        self.pushButton_4.clicked.connect(self.goto_today)

    def add_schedule(self):
        add_schedule_gui(self)

    def show_schedule(self):
        show_schedule_gui(self)

    def delete_schedule(self):
        delete_schedule_gui(self)

    def goto_today(self):
        today = datetime.today().date()
        self.calendarWidget.setSelectedDate(today)

#고유번호 생성(3자리)
def generate_id(y, m, d, h, mi):
    #schedules 디렉토리가 없을 시 생성
    directory = "schedules"
    if not os.path.exists(directory):
        os.makedirs(directory)
        return "001"
    
    # 마지막 파일 uid 불러오기
    files = os.listdir("schedules")
    if not files:return "001"
    elif sorted(files)[-1].split('-')[0] != f"{y}{m}{d}{h}{mi}":return "001"
    else:
        last_file = sorted(files)[-1]
        last_id = int(last_file.split('-')[1].split('.dat')[0])
        new_id = (last_id + 1) % 1000
        return f"{new_id:03d}"
    
#입력 데이터 파싱
def parsing_input():
    while True:
        try:
            s = input("일정을 입력하세요 (YYYY MM DD HH MM / Default=Now): ")
            if s:
                if datetime.strptime(s, "%Y %m %d %H %M"):
                    s = list(s.split())
                else:print("잘못된 날짜 형식입니다.")
            else:s = list(datetime.now().strftime("%Y %m %d %H %M").split())
            return s[0][2:], s[1], s[2], s[3], s[4]
        except:
            print("잘못된 입력 형식입니다.")  

#파일 저장 
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

#저장된 파일 불러오기
def load_file(filename):
    filepath = os.path.join("schedules", filename)
    if not os.path.exists(filepath):
        return "오류 : 해당 일정이 존재하지 않습니다."
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CalendarApp()
    main_window.show()
    sys.exit(app.exec()) 
