import json
from datetime import datetime
import os

#고유번호 생성(3자리)
def generate_id(y, m, d, h, mi):

    directory = "schedules"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 마지막 파일 uid 불러오기
    files = os.listdir(directory)
    if not files:
        return "001"
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

#일정 추가
def add_schedule():
    content = input("일정 내용을 입력하세요 :")
    y,m,d,h,mi = parsing_input()
    uid = generate_id(y, m, d, h, mi)
    filename = save_file(y, m, d, h, mi, uid, content)
    print(f"일정이 저장되었습니다: {filename}") 

#일정 조회
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
        year = input("조회할 년도를 입력해주세요. (YYYY) :")[2:]
        
    elif ch == "2":
        year = input("조회할 년도를 입력해주세요. (YYYY) :")[2:]
        month = input("해당 년도의 조회할 월을 입력해주세요. (MM) :")
        
    elif ch == "3":
        year = input("조회할 년도를 입력해주세요.  (YYYY) :")[2:]
        month = input("해당 년도의 조회할 월을 입력해주세요. (MM) :")
        day = input("조회할 일자를 입력해주세요. (DD) :")
        
    else:
        print("다시 입력해주세요.")
        return
    
    #파일 찾기
    search = []
    for fname in files:
        if not fname.endswith('.dat'):
            continue
        parts = [fname[:2],fname[2:4],fname[4:6],fname.split('-')[1]]
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


#일정 삭제
def delete_schedule():
    directory = "schedules"
    if not os.path.exists(directory):
        print("오류 : 일정이 존재하지 않습니다.")
        return
    
    files = os.listdir(directory)
    if not files:
        print("오류 : 일정이 존재하지 않습니다.")
        return
    
    year = input("삭제할 일정의 년도를 입력하세요 (YYYY) :")[2:]
    month = input("해당 년도의 조회할 월을 입력해주세요. (MM) :")
    day = input("조회할 일자를 입력해주세요. (DD) :")

    search = []
    for fname in files:
        if not fname.endswith(".dat"):
            continue
        parts = [fname[:2],fname[2:4],fname[4:6],fname.split('-')[1].split('.dat')[0]]
        if len(parts) != 4:
            continue
        y,m,d,uid = parts
        if y == year and m == month and d == day:
            search.append((fname, uid))
        
    if not search:
        print("해당 날짜에 일정이 없습니다.")
        return
        
    print(f"\n{year}-{month}-{day} 일정목록")
    for i, (fname, uid) in enumerate(search, 1):
        filepath = os.path.join(directory, fname)
        with open(filepath, 'r', encoding = 'UTF-8') as f:
            data = json.load(f)
            print(f"{i}. 고유번호: {uid} - 내용: {data['schedule']}\n")

    uid = input("삭제할 일정의 고유번호를 입력하세요: ")

    target = None
    for fname, file_uid in search:
        if file_uid == uid:
            target = fname
            break

    if not target:
        print("해당 고유번호의 일정이 없습니다.")
        return
    
    confirm = input(f"정말로 '{target}' 일정을 삭제하시겠습니까? (y/n) :")
    if confirm.lower() != 'y':
        print("삭제가 취소되었습니다.")
        return
    
    filepath = os.path.join(directory, target)
    os.remove(filepath)
    print(f"'{target}' 일정이 삭제되었습니다.")
    
#일정 수정
def edit_schedule(uid):
    directory = "schedules"
    
    if not os.path.exists(directory):
        print("오류 : 일정이 존재하지 않습니다.")
        return
    
    files = os.listdir(directory)
    if not files:
        print("오류 : 일정이 존재하지 않습니다.")
        return
    
    file = None
    
    for fname in files:
        if not fname.endswith('.dat'):
            continue
        parts = [fname[:2],fname[2:4],fname[4:6],fname.split('-')[1].split('.dat')[0]]
        if len(parts) != 4:
            continue
        _, _, _, fuid = parts

        if fuid == uid:
            file = fname
            break
        
    if not file:
        print("조건에 맞는 일정이 없습니다.")
        return
    
    data = load_file(file)
    print("\n선택된 일정 정보")
    print(f"\n날짜: {data['date']['year']}-{data['date']['month']}-{data['date']['day']}")
    print(f"\n내용: {data['schedule']}\n")
    
    content = input("수정할 내용을 입력하세요 : ")
    data['schedule'] = content
    filepath = os.path.join(directory, file)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print("해당 일정의 내용이 수정되었습니다.")
    
if __name__ == "__main__":
    while (1):
        print("\n-----일정 관리 프로그램----")
        print("1. 일정 추가")
        print("2. 일정 조회")
        print("3. 일정 수정")
        print("4. 일정 삭제")
        print("5. 종료")
        choice = input("작업 선택: ")
    
        if choice == "1":
            add_schedule()
        elif choice == "2":
            check_schedule()
        elif choice == "3":
            uid = input("수정할 일정의 고유번호를 입력하세요: ")
            edit_schedule(uid)
        elif choice == "4":
            delete_schedule()
        elif choice == "5":
            print("프로그램을 종료합니다.")
            break
        else:
            print("올바른 선택지를 입력해주세요.")