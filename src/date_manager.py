import csv
import os
import re
from datetime import datetime


class DateManager():
    def __init__(self):
         self.virtual_date = "2000-01-01"
    
    #startdate 파일 읽기
    def read_file(self):
            with open('data/startdate.txt', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                self.virtual_date = reader    

    
    #시작 가능 날짜 정규표현식 확인
    def is_valid_date(self,date_string) -> bool:
        # 정규 표현식 정의
        pattern = r'^(?:(?:20[0-2]\d)-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01]))$'
        # 정규 표현식과 일치하는지 검사
        return bool(re.match(pattern, date_string))

    #시작 날짜 저장
    def save_startdate(self,save_date) -> None:
        self.virtual_date = save_date
        with open('data/startdate.txt', 'w') as file:
            file.write(save_date)
    
    #사용 가능한 날짜 여부 (현재 가상날짜 이전인지)
    def is_available_date(user_input: str, available_date: str) -> bool:
        # 문자열을 날짜로 변환
        user_date = datetime.strptime(user_input, '%Y-%m-%d')
        available_date_obj = datetime.strptime(available_date, '%Y-%m-%d')
        #날짜 비교
        return user_date >= available_date_obj
    
    def parse_insert(self,insert)->tuple[bool,any]:
        insert_s = insert.strip() # 입력 선후 공백 제거
        if insert_s == '': # 빈 문자열
            print("올바르지 않은 입력형식입니다. 다시 입력해주세요.")
            return False ,None
        elif insert_s.lstrip('0')=='': #선행 0 포함 0입력 여부 확인
            print('프로그램을 종료합니다.')
            return True,'0' #이거 프롬프트에서 종료 판단하고 프로그램 종료해야함
        
        check = self.is_valid_date(insert_s) #정규 표현식 확인
        if check:
            check = self.is_available_date(insert_s,self.virtual_date)
            if check:#정상 입력
                self.save_startdate(insert_s)
                return True ,None
            else: #사용 불가능한 날짜
                print(f"최근 대출일({self.virtual_date})보다 앞선날짜는 접근할 수 없습니다. 다시 입력해주세요.")
                return False,None
        else:
            print("올바르지 않은 입력형식입니다. 다시 입력해주세요.")
            return False, None
        