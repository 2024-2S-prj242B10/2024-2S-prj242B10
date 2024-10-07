from manager.validation import *
from src.user import *
def admin_menu():
    """관리자 메뉴"""
    print("[관리자 메뉴]")
    print("0. 로그아웃")
    print("1. 도서 등록")
    print("2. 도서 삭제")
    print("3. 도서 검색")
    print("4. 도서 조회")


class Prompt:

    # 로그인 프롬프트
    def login_prompt(self)-> tuple[bool,any]:

        while True:  # 잘못된 입력이면 모드 선택 프롬프트 반복
            print("-------------------------------------------")
            print("[관리자 로그인]")
            manager_id = input("아이디:")
            manager_pw = input("비밀번호:")
            command = input("로그인 하시겠습니까? (y/다른 키를 입력하면 메인 메뉴로 이동합니다.):")
            
            #아이디 비번 모두 통과해야 is_valid가 True
            is_valid,insert = self.parser.manager_login_parse(manager_id,manager_pw,command) #날짜 검사 파서 만들어야함
            
            if is_valid:
                if command=='y': # 'y'를 받을 때만 관리자 아이디 넘기기
                    #정상 입력한 경우
                    # config에 현재 사용중인 사람으로 id 저장
                    ''' insert ID만 반환하는걸로?'''
                    return True,manager_id
                else:
                    # 사용자가 command로 y 이외의 값을 입력한 경우
                    return False
                
            #mod에 오류 메시지를 반환하도록 설계 다르게 해도 됨
            else:  
                print(insert)  # 오류 메시지 출력

    #관리자 메뉴 프롬프트
    def manager_menu_prompt(self):
        arrow = [0,1,2,3,4]
        while True:  # 잘못된 입력이면 모드 선택 프롬프트 반복
            print("-------------------------------------------")
            print("[관리자 메뉴]")
            print("0. 로그아웃")
            print("1. 도서 등록")
            print("2. 도서 삭제")
            print("3. 도서 검색")
            print("4. 도서 조회")
            command = int(input("원하는 메뉴의 번호를 입력해 주세요:"))
            
            if command in arrow:
                if command == 0: #로그아웃
                    break 
                #아래는 각 프롬프트로 이동해야함
                elif command == 1: # 도서 등록 >> 40권 넘어가면 오류처리 해야함
                    continue
                elif command == 2: # 도서 삭제
                    continue
                elif command == 3: # 도서 검색
                    continue
                elif command == 4: # 도서 조회
                    continue
            else:
                print("올바르지 않은 입력형식입니다. 다시 입력해주세요.")  # 오류 메시지 출력

    # 사용자 메뉴 프롬프트
    def user_menu_prompt(self):

        arrow = [0,1,2,3,4]
        while True:  # 잘못된 입력이면 모드 선택 프롬프트 반복
            print("-------------------------------------------")
            print("[사용자 메뉴]")
            print("0. 로그아웃")
            print("1. 도서 대출")
            print("2. 도서 반납")
            print("3. 도서 검색")
            print("4. 도서 조회")
            command = int(input("원하는 메뉴의 번호를 입력해 주세요:"))
            
            
            if command in arrow:
                if command == 0: # 로그아웃
                    break
                #아래는 각 프롬프트로 이동해야함
                elif command == 1: # 도서 대출
                    continue
                elif command == 2: # 도서 반납
                    continue
                elif command == 3: # 도서 검색
                    continue
                elif command == 4: # 도서 조회
                    continue
            else:
                print("올바르지 않은 입력형식입니다. 다시 입력해주세요.")  # 오류 메시지 출력

    #회원 가입
    def register(self,user_manager):
          while True:  # 잘못된 입력이면 모드 선택 프롬프트 반복
            print("-------------------------------------------")
            print("사용할 계정의 정보를 입력해주세요.")
            register_id = input("아이디:")
            register_pw = input("비밀번호:")
            register_name = input("이름:")
            command = input("회원가입 하시겠습니까? (y/다른 키를 입력하면 메인 메뉴로 이동합니다.):")
            
            
            is_valid, insert = user_manager.user_regist(user_manager,register_id,register_pw,register_name)
            
            if is_valid:
                if command=='y': 
                    user_manager.add_user(register_name,register_id,register_pw) ## UserManager에서 add_user 함수 필요
                    print(f"{register_name}님 회원가입에 성공하였습니다.초기화면으로 돌아갑니다.")
                    break
                else:
                    #사용자가 command로 y 이외의 값을 입력한 경우
                    print("초기화면으로 돌아갑니다.")
                    break
            else:
                print(insert)  # 오류 메시지 출력
                

