from manager.validation import *
from manager.var import *
from src.user import *
from src.book import *
from manager.var import *

class Prompt:

    # 로그인 프롬프트
    def login_prompt(self,user_manager)-> tuple[bool,bool,any]:
        while True:  # 잘못된 입력이면 로그인 프롬프트 반복
            print("-------------------------------------------")
            print("[로그인]")
            logined_id = input("아이디:").strip()
            logined_pw = input("비밀번호:").strip()
            command = input("로그인 하시겠습니까? (y/다른 키를 입력하면 초기화면으로 이동합니다.):").strip()
            
            
            if command == 'y':
                is_valid,is_manager = user_manager.user_login(user_manager,logined_id,logined_pw)
                if is_valid:
                    if is_manager:
                        print("관리자 모드로 접속합니다. 관리자 메뉴화면으로 이동합니다.")
                        return is_valid,is_manager,logined_id
                    else:
                        print("사용자 모드로 접속합니다. 사용자 메뉴화면으로 이동합니다.")
                        return is_valid,is_manager,logined_id
                else:
                    print("로그인에 실패했습니다. 다시 입력해주세요.")

            else:
                print("초기화면으로 이동합니다.")
                return False,False,0
            
    def manager_menu_prompt(self, book_manager):
        validate = Validate()
        arrow = [0, 1, 2, 3, 4, 5, 6]
        while True:  # 잘못된 입력이면 모드 선택 프롬프트 반복
            print("-------------------------------------------")
            print("[관리자 메뉴]")
            print("0. 로그아웃")
            print("1. 도서 등록")
            print("2. 도서 삭제")
            print("3. 도서 검색")
            print("4. 도서 조회")
            print("5. 대출 및 연체 기간 수정")
            print("6. 도서 연혁 열람")
            command = input("원하는 메뉴의 번호를 입력해 주세요:").strip()
            
            if command.isdigit():  # 입력값이 숫자로만 이루어졌는지 확인
                command = int(command)
            else:
                print('올바르지 않은 입력형식입니다. 관리자 메뉴로 돌아갑니다.')
                continue
            
            if command in arrow:
                if command == 0:  # 로그아웃
                    print("로그아웃 되었습니다.")
                    break 
                
                elif command == 1:  # 도서 등록
                    print("-------------------------------------------")
                    if len(book_manager.books) >= var.MAX_BOOK_CNT:
                        print("등록된 도서가 400권을 초과하여 더 이상 등록할 수 없습니다. 관리자 메뉴로 돌아갑니다.")
                        continue

                    print("등록할 도서의 정보를 입력해주세요.")
                    register_title = input("도서 제목: ").strip()
                    if not(validate.validate_book_title(register_title)):
                        print("올바르지 않은 입력형식입니다. 관리자 메뉴로 돌아갑니다.")
                        continue

                    author_list = []
                    #var = Var()
                    max_attempts = var.MAX_WRITER_CNT # 이것도 나중에 상수로 빼는게 좋을듯?
                    attempt = 0
                    valid_input = True  # Flag 변수 추가
                    
                    while attempt < max_attempts:
                        register_author = input(f"{attempt + 1}번째 도서 저자(없다면 그냥 엔터): ").strip()

                        # 공백 입력이면 즉시 종료
                        if not register_author:
                            break

                        # 입력값 형식 검증
                        if not validate.validate_book_writer(register_author):
                            print("올바르지 않은 입력 형식입니다. 관리자 메뉴로 돌아갑니다.")
                            valid_input = False  # Flag 설정
                            break  # 내부 while 탈출

                        # 저자 코드와 이름 추가
                        author_code, author_name = book_manager.add_author(register_author, author_list)
                        if author_code == "duplicate":
                            continue
                        if not author_code:
                            valid_input = False  # 추가 실패 시 탈출
                            break

                        author_list.append((author_code, author_name))  # 리스트에 추가
                        attempt += 1  # 입력 성공 시 카운터 증가
                    
                    if not valid_input:  # 내부 루프에서 문제가 발생한 경우
                        continue  # 바깥쪽 while 루프로 돌아감

                    # 나머지 빈 공간을 [-,-]로 채우기
                    while len(author_list) < max_attempts:
                        author_list.append(("-", "-"))

                    register_publisher = input("도서 출판사: ").strip()
                    if not (validate.validate_book_publisher(register_publisher)):
                        print("올바르지 않은 입력형식입니다. 관리자 메뉴로 돌아갑니다.")
                        continue

                    confirm = input("도서를 등록하시겠습니까? (y / 다른 키를 입력하면 취소합니다.): ").strip().lower()
                    if confirm == 'y':
                        book_manager.register_book(register_title, register_publisher, author_list)
                    else:
                        print("도서 등록을 취소합니다. 관리자 메뉴로 돌아갑니다.")
                    continue

                
                elif command == 2:  # 도서 삭제
                    print("-------------------------------------------")
                    print("삭제할 도서의 정보를 입력해주세요.")
                    book_id = input("도서 ID: ").strip()
                    if validate.validate_book_id(book_id):
                        if validate.validate_book_exist(book_id):
                            if validate.validate_book_can_borrow(book_id):
                                book_manager.books = book_manager.load_books()
                                book = book_manager.search_book_by_id(book_id)
                                if book.deleted_date == "":

                                    print(f"\n삭제할 도서 정보:")
                                    print(f"도서 ID: {book.book_id}")
                                    print(f"도서 구분자: {book.book_code}")
                                    print(f"제목: {book.title}")
                                    print(f"출판사: {book.publisher}")
                                    #authors_str = ', '.join([f"{author[1]} [{author[0]}]" for author in book.authors])
                                    authors_str = ", ".join([f"{author_name} [{author_code}]" for author_code, author_name in book.authors if author_code != "-" or author_name != "-"])
                                    print(f"저자: {authors_str}")
                                    print(f"대출 상태: {'대출 중' if book.is_loaned else '대출 가능'}\n")
                                    if input("도서를 삭제하시겠습니까? (y / 다른 키를 입력하면 등록을 취소하고 관리자 메뉴로 이동합니다.):").strip() == 'y':
                                        book_manager.delete_book(book_id)
                                    else:
                                        print("도서 삭제를 취소합니다. 관리자 메뉴로 돌아갑니다.")
                                        pass
                                else:
                                    print("이미 삭제된 도서입니다. 관리자 메뉴로 돌아갑니다.")
                            else:
                                print("대출 중인 도서는 삭제할 수 없습니다. 관리자 메뉴로 돌아갑니다.")
                        else:
                            print(f"존재하지 않는 도서입니다. 관리자 메뉴로 돌아갑니다.")
                    else:
                        print("올바르지 않은 입력형식입니다. 관리자 메뉴로 돌아갑니다.")
                    continue
                elif command == 3:  # 도서 검색
                    print("-------------------------------------------")
                    print("[도서 검색]")
                    search_title = input("\n검색할 도서 제목을 입력해주세요: ").strip()
                    book_manager.search_book_by_title(search_title)
                    continue
                elif command == 4:  # 도서 조회
                    print("-------------------------------------------")
                    print("[도서 목록]")
                    book_manager.display_books()
                    continue
                elif command == 5:  # 대출 및 연체 기간 수정
                    book_manager.update_loan_overdue_date()
                    continue
                elif command == 6:  # 도서 연혁 조회
                    display_book_history_admin()
                    continue
            else:
                print("올바르지 않은 입력형식입니다. 다시 입력해주세요.")  # 오류 메시지 출력



    # 사용자 메뉴 프롬프트
    def user_menu_prompt(self, book_manager, user_id):

        arrow = [0,1,2,3,4,5]
        while True:  # 잘못된 입력이면 모드 선택 프롬프트 반복
            print("-------------------------------------------")
            print("[사용자 메뉴]")
            print("0. 로그아웃")
            print("1. 도서 대출")
            print("2. 도서 반납")
            print("3. 도서 검색")
            print("4. 도서 조회")
            print("5. 도서 연혁 열람")
            command = input("원하는 메뉴의 번호를 입력해 주세요:").strip()
            
            if command.isdigit():  # 입력값이 숫자로만 이루어졌는지 확인
                command = int(command)
            else:
                print('올바르지 않은 입력형식입니다. 다시 입력해 주세요')
                continue
            
            if command in arrow:
                if command == 0: # 로그아웃
                    break
                #아래는 각 프롬프트로 이동해야함
                elif command == 1: # 도서 대출
                    borrow_book(user_id)
                    continue
                elif command == 2: # 도서 반납
                    return_book(user_id)
                    continue
                elif command == 3: # 도서 검색
                    search_book(book_manager)
                    continue
                elif command == 4: # 도서 조회
                    view_books(book_manager)
                    continue
                elif command == 5: # 도서 연혁 조회
                    display_book_history_user()
                    continue
            else:
                print("올바르지 않은 입력형식입니다. 다시 입력해주세요.")  # 오류 메시지 출력

    #회원 가입
    def register(self,user_manager):
        var = Var()
        if len(user_manager.users) >= (var.MAX_USER_CNT + 1):
            print("현재는 회원가입이 불가능합니다. 초기화면으로 이동합니다.")
            return
        
        while True:  # 잘못된 입력이면 모드 선택 프롬프트 반복
            print("-------------------------------------------")
            print("사용할 계정의 정보를 입력해주세요.")
            register_id = input("아이디:").strip()
            register_id = register_id.strip()
            is_id = user_manager.validate.validate_user_id(register_id)
            is_id_repeat = False
            if is_id:
                is_id_repeat = user_manager.validate.validate_user_id_duplicate(register_id)
                if not is_id_repeat: # 중복되면 FALSE
                    print("아이디가 중복되었습니다. 다시 입력해 주세요.")
                    continue
            else:
                print("아이디,비밀번호 또는 이름이 입력 형식에 맞지 않습니다. 다시 입력해 주세요.")
                continue

            if is_id_repeat:
                register_pw = input("비밀번호:").strip()
                register_name = input("이름:").strip()
                command = input("회원가입 하시겠습니까? (y/다른 키를 입력하면 초기화면으로 이동합니다.):").strip()
                
                
                is_valid, insert = user_manager.user_regist(user_manager,register_id,register_pw,register_name)
                
                if command=='y': 
                    if is_valid:
                        user_manager.add_user(register_name,register_id,register_pw) 
                        print(f"{register_name}님 회원가입에 성공하였습니다.초기화면으로 돌아갑니다.")
                        break
                    else:
                        print(insert)  # 오류 메시지 출력
                else:
                    print("초기화면으로 돌아갑니다.")
                    break
            
                
            
                
