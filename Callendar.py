import json
from datetime import datetime
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
from GUI import Ui_MainWindow

class CalendarApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

#고유번호 생성(3자리)
def generate_id(y, m, d, h, mi):
    # 마지막 파일 uid 불러오기
    files = os.listdir("schedules")
    if not files:return "001"
    elif sorted(files)[-1].split('-')[0] != f"{y}{m}{d}{h}{mi}":return "001"
    else:
        last_file = sorted(files)[-1]
        last_id = int(last_file.split('-')[1].split('.')[0])
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
def save_file(year, month, day, h, m, uid):
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
        }
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
