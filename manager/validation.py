import re
import os
import sys
import time
from src.book import BookManager
from datetime import datetime
from manager.var import Var as var

class Validate():
    
    def validate_user_name(self,user_name):
        if re.fullmatch(r'^[A-Za-z]{1,20}$', user_name):
            return True
        return False
    

    def validate_user_id(self,user_id):
        if re.fullmatch(r'^[A-Za-z0-9]{3,7}', user_id):
            return True
        return False

    def validate_user_id_duplicate(self,user_id):
        from src.user import UserManager
        user_manager = UserManager()
        for user in user_manager.users:
            if user.user_id == user_id:
                return False 
        return True

    def validate_user_pw(self,user_pw):
        if re.fullmatch(r'^[A-Za-z0-9]{5,10}', user_pw):
            return True
        return False

    def validate_loan_count(self,loan_count):
        if re.fullmatch(r'^[0-3]$', loan_count):
            return True
        return False

    def validate_date(self,date):
        if re.fullmatch(r'^(?:(?:20[0-2]\d)-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01]))$', date):
            return True
        return False

    def validate_t_f(self,insert) -> bool:
        arrow = ['True','False']
        if insert in arrow:
            return True
        else:
            return False

    def validate_book_title(self,title): #도서 제목 정규표현식 변경
        if re.fullmatch(r'^[a-zA-Z가-힣0-9](?:[a-zA-Z가-힣0-9\s]{0,48}[a-zA-Z가-힣0-9])?$', title):
            return True
        return False

    def validate_book_id(self,book_id):
        if book_id.isdigit():
            book_id = int(book_id)
            if 1000 <= book_id <= 9999:
                return True
        return False

    def validate_book_exist(self,book_id):
        return any(book.book_id == book_id for book in BookManager().books)

    def validate_book_can_borrow(self,book_id):
        for book in BookManager().books:
            if book.book_id == book_id:
                return not book.is_loaned
        return False
    
    def validate_loan_date(self,loan_date):
        if re.fullmatch(r'^(100|[1-9][0-9]?)$', loan_date):
            return True
        return False
    
    def validate_over_due(self,over_due):
        if re.fullmatch(r'^(100|[1-9][0-9]?)$', over_due):
            return True
        return False
    
    def validate_book_delimiter(self,book_delimiter):
        if re.fullmatch(r'^(100|[1-9][0-9]{2})$',book_delimiter):
            return True
        return False
    
    def validate_book_publisher(self,publisher):
        if re.fullmatch(r'^[a-zA-Z가-힣0-9](?:[a-zA-Z가-힣0-9\s]{0,8}[a-zA-Z가-힣0-9])?$',publisher):
            return True
        return False
    
    
    def validate_book_writer(self,writer):
        if re.fullmatch(r'^[a-zA-Z가-힣0-9](?:[a-zA-Z가-힣0-9\s]{0,18}[a-zA-Z가-힣0-9])?$',writer):
            return True
        return False
    
    def validate_name_delimiter(self,name_delimiter):
        if re.fullmatch(r'^(100|[1-9][0-9]{2})$',name_delimiter):
            return True
        return False
    
    # def validate_writer_element(self, writer_element):
    #     """Validate the entire file element."""
    #     # Combined regex for the whole file element
    #     element_regex = (
    #         r'^\['
    #         r'('
    #         r'[a-zA-Z가-힣0-9](?:[a-zA-Z가-힣0-9\s]{0,18}[a-zA-Z가-힣0-9])?'  # Author name
    #         r'),'
    #         r'(100|[1-9][0-9]{2})'  # Book delimiter
    #         r'\]$|^\[,]$'  # Or just [,]
    #     )
    #     return bool(re.fullmatch(element_regex, writer_element))


    def validate_writer_element(self, writer_element):
        """Validate the entire file element."""
        # 정규 표현식 수정: [저자코드,저자명]
        element_regex = (
            r'^\['
            r'(100|[1-9][0-9]{2})'  # 저자 코드: 100~999의 숫자
            r','  # 쉼표 구분자
            r'('
            r'[a-zA-Z가-힣0-9](?:[a-zA-Z가-힣0-9\s]{0,18}[a-zA-Z가-힣0-9])?'  # 저자명
            r')'
            r'\]$|^\[-,-]$'  # 또는 단순히 [,] 만 입력된 경우
        )
        return bool(re.fullmatch(element_regex, writer_element))


class File_util:
    def __init__(self):
        self.validate = Validate()
        self.book_count = 0
        self.recent_date ='2000-01-01'
        self.user_count = 0
        self.loan_count = 0 #loglist 행의 개수
       


    #startinfo.txt 무결성
    def validate_startinfo_file(self):
        if os.path.exists('data/startinfo.txt'):
            with open('data/startinfo.txt', 'r', encoding='utf-8') as file:
                lines = file.read().rstrip().split('\n')
                if not lines or (len(lines) == 1 and lines[0] == ''):
                    print("startinfo.txt 파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.")
                    time.sleep(0.1)
                    sys.exit()
            
                parts = lines[0].split(',')
                if not len(parts)==2:
                    print("startinfo.txt 파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.")
                    time.sleep(0.1)
                    sys.exit()
                else:
                    loan_date,over_due = parts[0],parts[1]
                    if not (self.validate.validate_loan_date(loan_date) and self.validate.validate_over_due(over_due)) :
                        print("startinfo.txt 파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.")
                        time.sleep(0.1)
                        sys.exit()
                    else:
                        var.LOAN_DATE = loan_date
                        var.OVERDUE_DATE = over_due
        
        else:
            try:
                os.makedirs(os.path.dirname('data/startinfo.txt'), exist_ok=True)
                with open('data/startinfo.txt', 'w', encoding='utf-8') as file:
                    file.write('10,5')
                print('data 디렉토리에 startinfo.txt파일 생성을 완료했습니다.')
            except Exception as e:  
                print('data 디렉토리에 startinfo.txt파일 생성에 실패했습니다. 프로그램을 종료합니다.')
                time.sleep(0.1)
                sys.exit()

   

    #startdate.txt 무결성
    def validate_startdate_file(self):
        if os.path.exists('data/startdate.txt'):
            with open('data/startdate.txt', 'r', encoding='utf-8') as file:
                lines = file.read().rstrip().split('\n')

                if not lines or (len(lines) == 1 and lines[0] == ''):
                    print("startdate.txt 파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.")
                    time.sleep(0.1)
                    sys.exit()

                valid_dates = [line for line in lines if self.validate.validate_date(line)]

                if len(valid_dates) == 1:
                    self.recent_date = valid_dates[0]
                else:
                    print("startdate.txt 파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.")
                    time.sleep(0.1)
                    sys.exit()
        else:
            try:
                os.makedirs(os.path.dirname('data/startdate.txt'), exist_ok=True)
                with open('data/startdate.txt', 'w', encoding='utf-8') as file:
                    file.write('2000-01-01')
                print('data 디렉토리에 startdate.txt파일 생성을 완료했습니다.')
            except Exception as e:  
                print('data 디렉토리에 startdate.txt파일 생성에 실패했습니다. 프로그램을 종료합니다.')
                time.sleep(0.1)
                sys.exit()

    #booklist.txt 무결성    
    def validate_booklist_file(self):
        if os.path.exists('data/booklist.txt'):
            with open('data/booklist.txt','r',encoding='utf-8') as file:
                lines = file.read().rstrip().split('\n')
                if len(lines) > var.MAX_BOOK_CNT:
                    print('booklist.txt파일의 내용이 제한을 초과하였습니다. 프로그램을 종료합니다.')
                    time.sleep(0.1)
                    sys.exit()
                elif len(lines)==1:
                    if lines[0] == '': #빈 파일일 경우
                        self.book_count = 0
                        return
                    else:
                        parts = lines[0].split(',')
                        if not len(parts) ==17:
                            print('booklist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                            time.sleep(0.1)
                            sys.exit()
                        else:
                            book_delim,book_id,book_title,book_loan_check = parts[0],parts[1],parts[2],parts[3]
                            book_publisher = parts[4]
                            '''
                            book_writer = []
                            name_delim = []
                            '''
                            writer_element = []
                            for i in range(5,15):
                                writer_element.append(parts[i])
                            
                            writer_str = []
                            for i in range(5):
                                writer_str.append(writer_element[i*2] + "," + writer_element[i*2 +1])

                            stored_date = parts[15] # 입고일
                            deleted_date = parts[16]# 삭제일

                            if not len(writer_str)==var.MAX_WRITER_CNT:  #저자 수가 
                                print('booklist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                                time.sleep(0.1)
                                sys.exit()


                            
                            book_delim_check = self.validate.validate_book_delimiter(book_delim) #작가가 1명 이상인 경우
                            id_check = self.validate.validate_book_id(book_id)
                            title_check = self.validate.validate_book_title(book_title)
                            loan_check = self.validate.validate_t_f(book_loan_check)
                            book_publisher_check = self.validate.validate_book_publisher(book_publisher)
                            stored_date_check =self.validate.validate_date(stored_date)
                            deleted_date_check = (self.validate.validate_date(deleted_date) or (deleted_date == ""))
                            for i in range(len(writer_str)):
                                writer_str_check = self.validate.validate_writer_element(writer_str[i])

                                if not writer_str_check:
                                    break
                            
                            if not (book_delim_check and id_check and title_check
                                     and loan_check and book_publisher_check and writer_str_check
                                         and stored_date_check and deleted_date_check): 
                                print('booklist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                                time.sleep(0.1)
                                sys.exit()
                            self.book_count = 1
                else:
                    line_count =0
                    for line in lines:
                        if line=='':
                            print('booklist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                            time.sleep(0.1)
                            sys.exit()
                        parts = line.split(',')
                        if not len(parts) ==17:
                            print('booklist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                            time.sleep(0.1)
                            sys.exit()
                        else:
                            book_delim,book_id,book_title,book_loan_check = parts[0],parts[1],parts[2],parts[3]
                            book_publisher = parts[4]
                            '''
                            book_writer = []
                            name_delim = []
                            '''
                            writer_element = []
                            for i in range(5,15):
                                writer_element.append(parts[i])
                            
                            writer_str = []
                            for i in range(5):
                                 writer_str.append(writer_element[i*2] + "," + writer_element[i*2 +1])

                            stored_date = parts[15] # 입고일
                            deleted_date = parts[16] # 삭제일

                            if not len(writer_str)==var.MAX_WRITER_CNT:  #저자 수가 
                                print('booklist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                                time.sleep(0.1)
                                sys.exit()


                            
                            book_delim_check = self.validate.validate_book_delimiter(book_delim) #작가가 1명 이상인 경우
                            id_check = self.validate.validate_book_id(book_id)
                            title_check = self.validate.validate_book_title(book_title)
                            loan_check = self.validate.validate_t_f(book_loan_check)
                            book_publisher_check = self.validate.validate_book_publisher(book_publisher)
                            stored_date_check =self.validate.validate_date(stored_date)
                            deleted_date_check = (self.validate.validate_date(deleted_date) or deleted_date == "")
                            for i in range(len(writer_str)):
                                writer_str_check = self.validate.validate_writer_element(writer_str[i])
                                if not writer_str_check:
                                    break
                               

                            if not (book_delim_check and id_check and title_check
                                     and loan_check and book_publisher_check and writer_str_check
                                         and stored_date_check and deleted_date_check): # and deleted_date_check
                                print('booklist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                                time.sleep(0.1)
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
                time.sleep(0.1)
                sys.exit()

    #userlist.txt 무결성
    def validate_userlist_file(self):
        if os.path.exists('data/userlist.txt'):
            with open('data/userlist.txt','r',encoding='utf-8') as file:
                lines = file.read().rstrip().split('\n')
                if len(lines) > var.MAX_USER_CNT+1:
                    print('userlist.txt파일의 내용이 제한을 초과하였습니다. 프로그램을 종료합니다.')
                    time.sleep(0.1)
                    sys.exit()
                elif len(lines)==1:
                    if lines[0]== '': #빈 파일일 경우
                        with open('data/userlist.txt','w',encoding='utf-8') as file_w:
                            file_w.write('ADMIN,admin,a1234,0,2000-01-01,Ture')
                        self.user_count = 1
                    else:
                        parts = lines[0].split(',')
                        if not len(parts)==6:
                            print('userlist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                            time.sleep(0.1)
                            sys.exit()
                        else:
                            use_name,user_id,user_pw = parts[0],parts[1],parts[2]
                            loan_count,loan_avail_date,access_level=parts[3],parts[4],parts[5]
                            use_name_check = self.validate.validate_user_name(use_name)
                            user_id_check = self.validate.validate_user_id(user_id) #파일쪽 무결성
                            user_pw_check = self.validate.validate_user_pw(user_pw)
                            loan_count_check = self.validate.validate_loan_count(loan_count)
                            loan_avail_date_check = self.validate.validate_date(loan_avail_date)
                            access_level_check = self.validate.validate_t_f(access_level)
                            if not (use_name_check and user_id_check and user_pw_check and loan_count_check and loan_avail_date_check and access_level_check):
                                print('userlist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                                time.sleep(0.1)
                                sys.exit()
                            self.user_count = 2
                else:
                    line_count =0
                    for line in lines:
                        parts = line.split(',')
                        if not len(parts)==6:
                            print('userlist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                            time.sleep(0.1)
                            sys.exit()
                        else:
                            #데이터 요소 문법 규칙 확인
                            use_name,user_id,user_pw = parts[0],parts[1],parts[2]
                            loan_count,loan_avail_date,access_level=parts[3],parts[4],parts[5]
                            use_name_check = self.validate.validate_user_name(use_name)
                            user_id_check = self.validate.validate_user_id(user_id)
                            user_pw_check = self.validate.validate_user_pw(user_pw)
                            loan_count_check = self.validate.validate_loan_count(loan_count)
                            loan_avail_date_check = self.validate.validate_date(loan_avail_date)
                            access_level_check = self.validate.validate_t_f(access_level)
                            if not (use_name_check and user_id_check and user_pw_check and loan_count_check and loan_avail_date_check and access_level_check):
                                print('userlist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                                time.sleep(0.1)
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
                time.sleep(0.1)
                sys.exit()
    
    #loglist.txt 무결성
    def validate_loglist_file(self):
        if os.path.exists('data/loglist.txt'):
            with open('data/loglist.txt','r',encoding='utf-8') as file:
                lines = file.read().rstrip().split('\n')
                if len(lines)==1:
                    if lines[0]== '': #빈 파일일 경우
                        self.loan_count = 0
                    else:
                        parts = lines[0].split(',')
                        if not len(parts)==4:
                            print('loglist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                            time.sleep(0.1)
                            sys.exit()
                        else:
                            book_id,user_id,is_loan,loan_date= parts[0],parts[1],parts[2],parts[3]
                            book_id_check = self.validate.validate_book_id(book_id)
                            user_id_check = self.validate.validate_user_id(user_id)
                            is_loan_check = self.validate.validate_t_f(is_loan)
                            loan_date_check = self.validate.validate_date(loan_date) # 정규 표현식 검사
                            if not (book_id_check and user_id_check and is_loan_check and loan_date_check):
                                print('loglist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                                time.sleep(0.1)
                                sys.exit()
                            self.loan_count = 1
                else:
                    if len(lines) > self.book_count:
                        print('loglist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                        time.sleep(0.1)
                        sys.exit()
                    line_count =0
                    for line in lines:
                        parts = line.split(',')
                        if not len(parts)==4:
                            print('loglist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                            time.sleep(0.1)
                            sys.exit()
                        else:
                            book_id,user_id,is_loan,loan_date= parts[0],parts[1],parts[2],parts[3]
                            book_id_check = self.validate.validate_book_id(book_id)
                            user_id_check = self.validate.validate_user_id(user_id)
                            is_loan_check = self.validate.validate_t_f(is_loan)
                            loan_date_check = self.validate.validate_date(loan_date) # 정규 표현식 검사
                            if not (book_id_check and user_id_check and is_loan_check and loan_date_check):
                                print('loglist.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                                time.sleep(0.1)
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
                time.sleep(0.1)
                sys.exit()


    #totallog.txt 무결성    
    def validate_totallog_file(self):
        if os.path.exists('data/totallog.txt'):
            with open('data/totallog.txt','r',encoding='utf-8') as file:
                lines = file.read().rstrip().split('\n')
                if len(lines)==1:
                    if lines[0] == '': #빈 파일일 경우
                        return
                    else:
                        parts = lines[0].split(',')
                        if not len(parts) ==5:
                            print('totallog.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                            time.sleep(0.1)
                            sys.exit()
                        else:
                            book_id,user_id,book_loan_check,loan_date = parts[0],parts[1],parts[2],parts[3]
                            expected_return_date= parts[4]
    
                            
            
                            book_id_check = self.validate.validate_book_id(book_id)
                            user_id_check = self.validate.validate_user_id(user_id)
                            loan_check = self.validate.validate_t_f(book_loan_check)
                            loan_date_check =self.validate.validate_date(loan_date)
                            expected_return_date_check = self.validate.validate_date(expected_return_date)

                            if not (book_id_check and user_id_check and loan_check
                                     and loan_date_check and expected_return_date_check):
                                print('totallog.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                                time.sleep(0.1)
                                sys.exit()
                else: 
                    for line in lines:
                        if line=='':
                            print('totallog.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                            time.sleep(0.1)
                            sys.exit()
                        parts = line.split(',')
                        if not len(parts)==5:
                            print('totallog.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                            time.sleep(0.1)
                            sys.exit()
                        else:
                            book_id,user_id,book_loan_check,loan_date = parts[0],parts[1],parts[2],parts[3]
                            expected_return_date= parts[4]
    
                            
            
                            book_id_check = self.validate.validate_book_id(book_id)
                            user_id_check = self.validate.validate_user_id(user_id)
                            loan_check = self.validate.validate_t_f(book_loan_check)
                            loan_date_check =self.validate.validate_date(loan_date)
                            expected_return_date_check = self.validate.validate_date(expected_return_date)

                            if not (book_id_check and user_id_check and loan_check
                                     and loan_date_check and expected_return_date_check):
                                print('totallog.txt파일의 내용에 오류가 있습니다. 프로그램을 종료합니다.')
                                time.sleep(0.1)
                                sys.exit()
        else:
            try:
                with open('data/totallog.txt','w',encoding='utf-8'):
                    pass
                print('data 디렉토리에 totallog.txt파일 생성을 완료했습니다.')
            except:
                print('data 디렉토리에 totallog.txt파일 생성에 실패했습니다. 프로그램을 종료합니다.')
                time.sleep(0.1)
                sys.exit()
