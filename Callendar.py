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
    directory = "schedules"
    os.makedirs(directory, exist_ok=True)

    filename = f"{year}-{month}-{day}-{uid}.dat"
    filepath = os.path.join(directory, filename)

    data = {
        "unique_id": uid,
        "date": {
            "year": year,
            "month": month,
            "day": day
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
    uid = generate_id()
    y, m, d = parsing_date()
    filename = save_file(y, m, d, uid)
    print(f"일정이 저장되었습니다: {filename}")

def check_schedule():
    directory = "schedules"
    if not os.path.exists(directory):
        print("오류 : 일정이 존재하지 않습니다.")
        return
    
    files = os.listdir(directory)
    if not files:
        print("오류 : 일정이 존재하지 않습니다.")
        return
    
    print ("조회할 일정 단위를 선택하세요.")
    print("1. 년도별 2. 월별 3. 일별")
    ch = input("")
    year = month = day = None
    
    if ch == "1":
        year = input("조회할 년도를 입력해주세요.")
        
    elif ch == "2":
        year = input("조회할 년도를 입력해주세요.")
        month = input("해당 년도의 조회할 월을 입력해주세요.")
        
    elif ch == "3":
        year = input("조회할 년도를 입력해주세요.")
        month = input("해당 년도의 조회할 월을 입력해주세요.")
        day = input("조회할 일자를 입력해주세요.")
        
    else:
        print("다시 입력해주세요.")
        return
    
    #파일 찾기
    search = []
    for fname in files:
        if not fname.endswith('.dat'):
            continue
        parts = fname[:-4].split('-')
        if len(parts) != 4:
            continue
        y, m, d, uid = parts

        if year and y != year:
            continue
        if month and m != month:
            continue
        if day and d != day:
            continue
        search.append(fname)
        
    if not search:
        print("조건에 맞는 일정이 없습니다.")
        return
    
    print("\n-----일정 목록-----")
    for idx, fname in enumerate(search, 1):
        data = load_file(fname)
        print(f"   날짜 : {data['date']['year']}-{data['date']['month']}-{data['date']['day']}")
        print(f"   고유 ID : {data['unique_id']}")
        print("\n")
    
    #조회 창에서 삭제는 일정 삭제 함수 구현 후 이곳에 분기처리해 추가할 예정
