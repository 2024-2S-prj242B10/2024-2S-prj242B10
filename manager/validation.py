import re
import os
import sys
from src.book import BookManager
from datetime import datetime
'''
정규표현식
startdate.txt
-1줄만 허용

-날짜문자열: ^(?:(?:20[0-2]\d)-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01]))$ //

booklist.txt
-1줄 이상 40줄 이하

-도서ID : 1000~9999 //
-도서제목 : ^[a-zA-Z가-힣0-9](?:[a-zA-Z가-힣0-9\s]{0,48}[a-zA-Z가-힣0-9])?$ /?
-대출 여부: True, False //

userlist.txt
-1줄 이상 11줄 이하
-0줄일 경우 초기화 해야함

-사용자이름 : [A-Za-z]{1, 20} //
-사용자 ID : [A-Za-z0-9]{3, 7} //
-사용자 비밀번호 : [A-Za-z0-9]{5, 10} //
-대출 권수 : 0~3 //
-대출 가능 날짜 == 날짜 문자열
-사용자 접근 등급 True, False

loglist.txt
- 0줄 이상 도서 정보행 개수 이하

-도서ID == boolist거와 동일
-사용자ID == userlist와 동일
-대출 여부 == True, False
-대출 및 반납일 == 날짜문자열
'''

def validate_date_compare(user_input: str, available_date: str) -> bool:
    # 문자열을 날짜로 변환
    user_date = datetime.strptime(user_input, '%Y-%m-%d')
    available_date_obj = datetime.strptime(available_date, '%Y-%m-%d')
    
    # 날짜 비교
    return user_date >= available_date_obj

def validate_user_name(user_name):
    if re.fullmatch(r'^[A-Za-z]{1,20}$', user_name):
        return True
    return False

def validate_user_id(user_id):
    if re.fullmatch(r'^[A-Za-z0-9]{3, 7}', user_id):
        return True
    return False

def validate_user_pw(user_pw):
    if re.fullmatch(r'^[A-Za-z0-9]{5, 10}', user_pw):
        return True
    return False

def validate_loan_count(loan_count):
    if re.fullmatch(r'^[0-3]$', loan_count):
        return True
    return False

def validate_date(date):
    if re.fullmatch(r'^(?:(?:20[0-2]\d)-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01]))$', date):
        return True
    return False

def validate_t_f(insert) -> bool:
    arrow = ['True','False']
    if insert in arrow:
        return True
    else:
        return False

def validate_book_title(title): #도서 제목 정규표현식 변경
    if re.fullmatch(r'^[a-zA-Z가-힣\s]{1,50}$', title):
        return True
    return False

def validate_book_id(book_id):
    return book_id.isdigit() and len(book_id) == 4

def validate_book_exist(book_id):
    return any(book.book_id == book_id for book in BookManager().books)

def validate_book_can_borrow(book_id):
    for book in BookManager().books:
        if book.book_id == book_id:
            return not book.is_loaned
    return False

class File_util:
    def __init__(self):
        self.book_count
        self.recent_date ='2000-01-01'
        self.user_count
        self.loan_count #loglist 행의 개수

    #startdate.txt 무결성
    def validate_startdate_file(self):
        if os.path.exists('data/startdate.txt'):
            with open('data/startdate.txt','r',encoding='utf-8') as file:
                lines = file.read().rstrip().split('\n')
                if len(lines)==1:
                    if lines =='': # 빈 파일일 경우
                        print("startdate.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.")
                        os.system('pause')
                        sys.exit()
                    else:
                        startdate_check = validate_date(lines) #시작 가능 날짜 유효성 검사
                        if startdate_check:
                            self.recent_date = lines
                        else:
                            print("startdate.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.")
                else:
                    print("startdate.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.")
                    os.system('pause')
                    sys.exit()
        else:
            try:
                with open('data/startdate.txt','w',encoding='utf-8') as file_w:
                    file_w.write('2000-01-01')
                print('data 디렉토리에 startdate.txt파일 생성을 완료했습니다.')
            except:
                print('data 디렉토리에 startdate.txt파일 생성에 실패했습니다. 프로그램을 종료합니다.')
                os.system('pause')
                sys.exit()

    #booklist.txt 무결성    
    def validate_booklist_file(self):
        if os.path.exists('data/booklist.txt'):
            with open('data/booklist.txt','r',encoding='utf-8') as file:
                lines = file.read().rstrip().split('\n')
                if len(lines) > 40:
                    print('booklist.txt파일의 내용이 제한을 초과하였습니다. 프로그램을 종료합니다.')
                    os.system('pause')
                    sys.exit()
                elif len(lines)==1:
                    if lines == '': #빈 파일일 경우
                        self.book_count = 0
                        return
                    else:
                        parts = lines.split(',')
                        if not len(parts)==3:
                            print('booklist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                            os.system('pause')
                            sys.exit()
                        else:
                            book_id,book_title,book_loan_check = parts[0],parts[1],parts[2]
                            id_check = validate_book_id(book_id)
                            title_check = validate_book_title(book_title)
                            loan_check = validate_t_f(book_loan_check)
                            if not (id_check and title_check and loan_check):
                                print('booklist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                                os.system('pause')
                                sys.exit()
                            self.book_count = 1
                else:
                    line_count =0
                    for line in lines:
                        parts = line.split(',')
                        if not len(parts)==3:
                            print('booklist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                            os.system('pause')
                            sys.exit()
                        else:
                            book_id,book_title,book_loan_check = parts[0],parts[1],parts[2]
                            id_check = validate_book_id(book_id)
                            title_check = validate_book_title(book_title)
                            loan_check = validate_t_f(book_loan_check)
                            if not (id_check and title_check and loan_check):
                                print('booklist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                                os.system('pause')
                                sys.exit()
                        line_count +=1
                    self.book_count= line_count #booklist.txt 행 개수
        else:
            try:
                with open('data/booklist.txt','w',encoding='utf-8'):
                    pass
                print('data 디렉토리에 booklist.txt파일 생성을 완료했습니다.')
            except:
                print('data 디렉토리에 booklist.txt파일 생성에 실패했습니다. 프로그램을 종료합니다.')
                os.system('pause')
                sys.exit()
    
    #userlist.txt 무결성
    def validate_userlist_file(self):
        if os.path.exists('data/userlist.txt'):
            with open('data/userlist.txt','r',encoding='utf-8') as file:
                lines = file.read().rstrip().split('\n')
                if len(lines) > 11:
                    print('userlist.txt파일의 내용이 제한을 초과하였습니다. 프로그램을 종료합니다.')
                    os.system('pause')
                    sys.exit()
                elif len(lines)==1:
                    if lines == '': #빈 파일일 경우
                        with open('data/userlist.txt','w',encoding='utf-8') as file_w:
                            file_w.write('ADMIN,admin,a1234,0,2000-01-01,False')
                        self.user_count = 1
                    else:
                        parts = lines.split(',')
                        if not len(parts)==6:
                            print('userlist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                            os.system('pause')
                            sys.exit()
                        else:
                            use_name,user_id,user_pw = parts[0],parts[1],parts[2]
                            loan_count,loan_avail_date,access_level=parts[3],parts[4],parts[5]
                            use_name_check = validate_user_name(use_name)
                            user_id_check = validate_user_id(user_id)
                            user_pw_check = validate_user_pw(user_pw)
                            loan_count_check = validate_loan_count(loan_count)
                            loan_avail_date_check = validate_date(loan_avail_date)
                            if loan_avail_date_check:
                                loan_avail_date_check = validate_date_compare(loan_avail_date,self.recent_date)
                            access_level_check = validate_t_f(access_level)
                            if not (use_name_check and user_id_check and user_pw_check and loan_count_check and loan_avail_date_check and access_level_check):
                                print('userlist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                                os.system('pause')
                                sys.exit()
                            self.user_count = 2
                else:
                    line_count =0
                    for line in lines:
                        parts = line.split(',')
                        if not len(parts)==6:
                            print('userlist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                            os.system('pause')
                            sys.exit()
                        else:
                            use_name,user_id,user_pw = parts[0],parts[1],parts[2]
                            loan_count,loan_avail_date,access_level=parts[3],parts[4],parts[5]
                            use_name_check = validate_user_name(use_name)
                            user_id_check = validate_user_id(user_id)
                            user_pw_check = validate_user_pw(user_pw)
                            loan_count_check = validate_loan_count(loan_count)
                            loan_avail_date_check = validate_date(loan_avail_date)
                            if loan_avail_date_check:
                                loan_avail_date_check = validate_date_compare(loan_avail_date,self.recent_date)
                            access_level_check = validate_t_f(access_level)
                            if not (use_name_check and user_id_check and user_pw_check and loan_count_check and loan_avail_date_check and access_level_check):
                                print('userlist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                                os.system('pause')
                                sys.exit()
                        line_count +=1
                    self.user_count= line_count #userlist.txt 행 개수
        else:
            try:
                with open('data/userlist.txt','w',encoding='utf-8') as file_w:
                    file_w.write('ADMIN,admin,a1234,0,2000-01-01,False')
                print('data 디렉토리에 userlist.txt파일 생성을 완료했습니다.')
            except:
                print('data 디렉토리에 userlist.txt파일 생성에 실패했습니다. 프로그램을 종료합니다.')
                os.system('pause')
                sys.exit()
    
     #userlist.txt 무결성
    
    #loglist.txt 무결성
    def validate_loglist_file(self):
        if os.path.exists('data/loglist.txt'):
            with open('data/loglist.txt','r',encoding='utf-8') as file:
                lines = file.read().rstrip().split('\n')
                if len(lines) > self.book_count:
                    print('loglist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                    os.system('pause')
                    sys.exit()
                elif len(lines)==1:
                    if lines == '': #빈 파일일 경우
                        self.loan_count = 0
                    else:
                        parts = lines.split(',')
                        if not len(parts)==4:
                            print('loglist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                            os.system('pause')
                            sys.exit()
                        else:
                            book_id,user_id,is_loan,loan_date= parts[0],parts[1],parts[2],parts[3]
                            book_id_check = validate_book_id(book_id)
                            user_id_check = validate_user_id(user_id)
                            is_loan_check = validate_t_f(is_loan)
                            loan_date_check = validate_date(loan_date) # 정규 표현식 검사
                            if loan_date_check: # 최근 날짜와 비교
                                loan_date_check = validate_date_compare(loan_date,self.recent_date)
                           
                            if not (book_id_check and user_id_check and is_loan_check and loan_date_check):
                                print('loglist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                                os.system('pause')
                                sys.exit()
                            self.loan_count = 1
                else:
                    line_count =0
                    for line in lines:
                        parts = line.split(',')
                        if not len(parts)==4:
                            print('loglist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                            os.system('pause')
                            sys.exit()
                        else:
                            book_id,user_id,is_loan,loan_date= parts[0],parts[1],parts[2],parts[3]
                            book_id_check = validate_book_id(book_id)
                            user_id_check = validate_user_id(user_id)
                            is_loan_check = validate_t_f(is_loan)
                            loan_date_check = validate_date(loan_date) # 정규 표현식 검사
                            if loan_date_check: # 최근 날짜와 비교
                                loan_date_check = validate_date_compare(loan_date,self.recent_date)
                            if not (book_id_check and user_id_check and is_loan_check and loan_date_check):
                                print('loglist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                                os.system('pause')
                                sys.exit()
                            
                        line_count +=1
                    self.loan_count= line_count #loglist.txt 행 개수
        else:
            try:
                with open('data/loglist.txt','w',encoding='utf-8'):
                    pass
                    print('data 디렉토리에 loglist.txt파일 생성을 완료했습니다.')
            except:
                print('data 디렉토리에 loglist.txt파일 생성에 실패했습니다. 프로그램을 종료합니다.')
                os.system('pause')
                sys.exit()
