import json
import random
from datetime import datetime
import os

#고유번호 생성(3자리)
def generate_id():
    return f"{random.randint(0, 999):03d}"

#연-월-일 파싱
def parsing_date():
    now = datetime.now()
    return str(now.year), str(now.month), str(now.day)

#파일 저장
def save_file(year, month, day, uid):
    filename = f"{year}-{month}-{day}-{uid}.dat"
    data = {
        "unique_id": uid,
        "date": {
            "year": year,
            "month": month,
            "day": day
        }
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return filename

#저장된 파일 불러오기
def load_file(filename):
    if not os.path.exists(filename):
        return "오류 : 해당 일정이 존재하지 않습니다."
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

#실행
if __name__ == "__main__":
    uid = generate_id()
    y, m, d = parsing_date()
    filename = save_file(y, m, d, uid)
    print(f"일정이 저장되었습니다.")
