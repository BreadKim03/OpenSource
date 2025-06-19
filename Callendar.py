import json
from datetime import datetime
import os

#고유번호 생성(3자리)
def generate_id(y, m, d, h, mi):
    # 마지막 파일 uid 불러오기
    files = os.listdir("schedules")
    if not files:return "001"
    elif sorted(files)[-1].split('-')[0] != f"{y[2:]}{m:0>2}{d:0>2}{h:0>2}{mi:0>2}":return "001"
    else:
        print(sorted(files)[-1].split('-')[0], f"{y[2:]}{m:0>2}{d:0>2}{h:0>2}{mi:0>2}")
        last_file = sorted(files)[-1]
        last_id = int(last_file.split('-')[1].split('.')[0])
        new_id = (last_id + 1) % 1000
        return f"{new_id:03d}"
    
#연-월-일 파싱
def parsing_date():
    now = datetime.now()
    return str(now.year), str(now.month), str(now.day), str(now.hour), str(now.minute)

#파일 저장 
def save_file(year, month, day, h, m, uid):
    directory = "schedules"
    os.makedirs(directory, exist_ok=True)

    filename = f"{year[2:]}{month:0>2}{day:0>2}{h:0>2}{m:0>2}-{uid}.dat"
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

#실행
if __name__ == "__main__":
    y, m, d, h, mi = parsing_date()
    uid = generate_id(y, m, d, h, mi)
    filename = save_file(y, m, d, h, mi, uid)
    print(f"일정이 저장되었습니다: {filename}")
