import os
import sys
from manager.validation import Validate,File_util
from manager.ui import Prompt
from src.date_manager import DateManager
from src.user import *
from src.book import BookManager
# from src.user import UserManager
  
def main():
    #무결성 검사
    file_util = File_util()
    file_util.validate_startdate_file()
    file_util.validate_booklist_file()
    file_util.validate_userlist_file()
    file_util.validate_loglist_file()
    file_util.validate_startinfo_file()

    date_manager = DateManager()
    date_manager.read_file()

    #가상날짜 입력 프롬프트
    while True:  # 잘못된 입력이면 모드 선택 프롬프트 반복
            print("-------------------------------------------")
            print("프로그램을 종료하려면 숫자 0을 입력해주세요.")
           
            command = input("프로그램에서 사용할 날짜를 입력해주세요 (yyyy-mm-dd):")
            
            is_valid, insert = date_manager.parse_insert(command)
            
            if is_valid:
                if insert=='0': # 0을 입력해 종료하려는 경우
                    os.system('pause')
                    sys.exit()
                else:
                    break
    
    #loan_manager = LoanManaer()
    user_manager = UserManager()
    book_manager = BookManager()

    prompt = Prompt()
    # 초기 화면 프롬프트
    
    arrow = [0,1,2] # 허용 명령어
    while True:  # 잘못된 입력이면 모드 선택 프롬프트 반복
        print("-------------------------------------------")
        print("[도서 대출 관리 프로그램]")
        print("0. 종료")
        print("1. 로그인")
        print("2. 회원가입")

        command = input("원하는 메뉴의 번호를 입력해 주세요:")

        if command.isdigit():  # 입력값이 숫자로만 이루어졌는지 확인
            command = int(command)
        else:
            print('올바르지 않은 입력형식입니다. 다시 입력해주세요.')
            continue
        
        if command in arrow:
            if command == 0:
                print("프로그램을 종료합니다")
                break
            elif command == 1:
                is_valid,is_manager,user_id=prompt.login_prompt(user_manager) # 파라미터로 manager 객체 넣어야 함
                if is_valid:
                    if is_manager:
                        prompt.manager_menu_prompt(book_manager) # 관리자 프롬프트로 넘어가기
                    else:
                        prompt.user_menu_prompt(book_manager, user_id) # 사용자 프롬프트로 넘어가기
                else:
                    continue
            elif command == 2:
                prompt.register(user_manager) # 회원 가입

        #mod에 오류 메시지를 반환하도록 설계
        else:   
            print('올바르지 않은 입력형식입니다. 다시 입력해주세요.')  # 오류 메시지 출력

if __name__ == "__main__":
    main()
