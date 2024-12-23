
from manager.validation import Validate
import os
from src.user_utils import *
import csv
from src.book import *
from manager.var import *


class User:
    def __init__(self,user_name, user_id, user_password, loan_count=0, loan_date=None, is_user=True):
        self.user_name = user_name
        self.user_id = user_id
        self.user_password = user_password
        self.loan_count = loan_count
        self.loan_date = loan_date
        self.is_user = is_user

    def __str__(self):
        return f"{self.user_name}, {self.user_id}, {self.user_password}, {self.loan_count}, {self.loan_date}, {self.is_user}"

class UserManager:
    def __init__(self, user_file_path="data/userlist.txt"):
        self.validate = Validate()
        self.user_file_path = user_file_path
        self.users = self.load_users()
    
    def add_user(self,register_name,register_id,register_pw):
        new_user = User(register_name,register_id,register_pw,0,'2000-01-01',True)
        self.users.append(new_user)
        with open(self.user_file_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            for user in self.users:
                writer.writerow([user.user_name,user.user_id,user.user_password,user.loan_count,user.loan_date, str(user.is_user)])

    def load_users(self):
        users = []
        if os.path.exists(self.user_file_path):
            with open(self.user_file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    user_name, user_id, user_password,loan_count,loan_date,is_user = row
                    users.append(User(user_name, user_id,user_password,loan_count,loan_date,is_user))
        return users


    def user_login(self,user_manager,logined_id,logined_pw)->tuple[bool,bool]:
        logined_id = logined_id.strip()
        logined_pw = logined_pw.strip()
        is_valid = False
        is_manager = False
        for user in user_manager.users:
            if (logined_id == user.user_id and logined_pw == user.user_password):
                is_valid = True
                if logined_id =='admin':
                    is_manager = True
        return is_valid,is_manager



    def user_regist(self,user_manager,register_id,register_pw,register_name)->tuple[bool,any]:        
        #선 공백 제거
        register_pw = register_pw.strip()
        register_name = register_name.strip()
        is_id = self.validate.validate_user_id(register_id)
        is_pw = self.validate.validate_user_pw(register_pw)
        is_name = self.validate.validate_user_name(register_name)
        
        if not (is_id and is_pw and is_name):
            return False,"아이디,비밀번호 또는 이름이 입력 형식에 맞지 않습니다. 다시 입력해 주세요."
        else:
            if self.validate.validate_user_id_duplicate(register_id):
                return True,None
            else:
                return False,"이미 존재하는 사용자 ID 입니다. 다시 입력해주세요."





def borrow_book(user_id):
    current_date = get_current_date()  # 현재 가상 날짜를 startdate.txt에서 가져옴

    # 대출 권수와 대출 가능 날짜 확인
    borrow_count, next_borrow_date = get_user_borrow_info(user_id)

    if borrow_count >= 3:
        print("현재 대출 권수가 3권이므로 더이상 대출을 할 수 없습니다. 사용자 메뉴로 돌아갑니다.")
        return

    if next_borrow_date > current_date:
        print(f"대출 가능 날짜는 {next_borrow_date} 이후입니다. 사용자 메뉴로 돌아갑니다.")
        return

    if has_overdue_books(user_id, current_date):
        print("현재 반납하지 않은 연체된 도서가 존재합니다. 사용자 메뉴로 돌아갑니다.")
        return

    print("--------------------------------------------------------------")
    print("[도서 대출]\n")
    print(f"{user_id}님 \n현재 {borrow_count}권 대출 중이므로 {3 - borrow_count}권 대출 가능합니다.")

    while True:
        book_id = input("원하는 도서의 ID(번호)를 입력해주세요(0 입력시 사용자 메뉴로 돌아갑니다.): ").strip()

        # 양의 정수 판별
        if book_id.isdigit() and int(book_id) >= 0:
            book_id = str(int(book_id))
        else:
            print("올바르지 않은 입력입니다. 다시 입력해주세요.")
            continue

        # 0을 입력한 경우 사용자 메뉴로 돌아감
        if book_id == '0':
            print("사용자 메뉴로 돌아갑니다.")
            return

        # 유효한 도서 ID 확인
        if not is_valid_book(book_id):
            print("존재하지 않는 도서입니다. 다시 입력해주세요.")
            continue

        # 도서가 이미 대출 중인지 확인
        if is_book_borrowed(book_id):
            print("다른 사용자가 이미 대출중인 도서입니다. 다시 입력해주세요.")
            continue

        # 대출 진행
        var = Var()
        
        return_date = calculate_return_date(current_date, var.LOAN_DATE)  # 대출 기간 10일 후 날짜 계산
        #print(f"{book_id} - {book_title}을 선택하셨습니다.")
        book_info = get_book_info(book_id)
        book_code = book_info[0]
        book_title = book_info[2]
        book_publisher = book_info[4]
        book_author = book_info[5]


        print(f"[{book_id}({book_code}) - {book_title} - {book_publisher} - {book_author}] 도서를 선택하셨습니다.")



        print(f"{book_title}을(를) {return_date}까지 대출합니다.")  # 대출일 + 10일

        confirm = input("도서를 대출하시겠습니까? (y / 다른 키를 입력하면 대출을 취소하고 사용자 메뉴로 이동합니다.): ").strip()
        if confirm == 'y':
            # 대출 기록 업데이트 및 사용자 대출 권수 업데이트
            update_log(user_id, book_id, True, return_date)
            update_totallog_borrow(user_id, book_id, True, return_date)
            update_user_borrow_count(user_id, 1)
            # 도서 대출 여부 업데이트
            update_book_status(book_id)  # 대출 여부를 True로 변경
            print("도서가 정상적으로 대출되었습니다.")
        else:
            print("도서 대출이 취소되었습니다.")

        break  # 정상적으로 대출이 끝난 후 루프를 빠져나감

# 도서 반납 함수
def return_book(user_id):

    # 사용자 대출 권수 확인
    borrow_count, _ = get_user_borrow_info(user_id)

    if borrow_count == 0:
        print("대출한 도서가 없어 반납을 진행할 수 없습니다. 사용자 메뉴로 돌아갑니다.")
        return

    # 대출 중인 도서 조회
    print("--------------------------------------------------------------")
    print("[도서 반납]")
    print(f"{user_id}님 대출 현황")
    borrowed_books = view_borrowed_books(user_id)

    if not borrowed_books:
        print("대출한 도서가 없습니다. 사용자 메뉴로 돌아갑니다.")
        return
    
    print()
    while True:
        book_id = input("반납을 원하는 도서의 도서 ID를 입력해주세요(0 입력시 사용자 메뉴로 돌아갑니다.): ").strip()

        # 양의 정수 판별
        if book_id.isdigit() and int(book_id) >= 0:
            book_id = str(int(book_id))
        else:
            print("올바르지 않은 입력입니다. 다시 입력해주세요.")
            continue

        # 0을 입력한 경우 사용자 메뉴로 돌아감
        if book_id == '0':
            print("도서 반납이 취소되었습니다.")
            return

        # # 유효한 도서 ID 확인
        # if not is_valid_book(book_id):
        #     print("존재하지 않는 도서ID입니다. 사용자 메뉴로 돌아갑니다.")
        #     return

        # 도서 반납 여부 확인
        if not is_book_borrowed_by_user(book_id, user_id):
            print("대출되지 않은 도서입니다. 사용자 메뉴로 돌아갑니다.")
            return

        # 도서 반납 진행
        print("도서를 반납하시겠습니까? (y / 다른 키를 입력하면 반납을 취소하고 사용자 메뉴로 이동합니다.): ", end="")
        confirm = input().strip()

        if confirm == 'y':

            # 반납예정일 먼저 가져와서 토탈로그에 찍히게
            return_date_ = get_return_date(book_id, user_id)
            update_totallog_return(user_id, book_id, False, return_date_)

            # 도서 반납 처리
            is_overdue = return_book_process(user_id, book_id)

            book_info = get_book_info(book_id)
            book_code = book_info[0]
            book_title = book_info[2]
            book_publisher = book_info[4]
            book_author = book_info[5]


            if is_overdue:
                next_borrow_date = calculate_next_borrow_date(get_current_date())
                print(f"[{book_id}({book_code}) - {book_title} - {book_publisher} - {book_author}] 도서를 반납했습니다.")
                print(f"연체된 도서이므로 다음 도서 대출 가능 날짜는 {next_borrow_date}입니다.")
            else:
                print(f"[{book_id}({book_code}) - {book_title} - {book_publisher} - {book_author}] 도서를 반납했습니다.")
            return
        else:
            print("도서 반납이 취소되었습니다.")
            return

# 도서 검색 함수
def search_book(book_manager):
    print("--------------------------------------------------------------")
    print("[도서 검색]")

    # 검색할 도서 제목 입력 받기
    search_title = input("\n검색할 도서 제목을 입력해주세요: ").strip()
    book_manager.search_book_by_title(search_title, 'user')

# 도서 조회 기능
def view_books(book_manager):
    book_manager.display_books(None, 'user')


def search_book_log():

    while True:
        book_id = input("원하는 도서의 ID(번호)를 입력해주세요(0 입력시 사용자 메뉴로 돌아갑니다.): ").strip()

        # 양의 정수 판별
        if book_id.isdigit() and int(book_id) >= 0:
            book_id = str(int(book_id))
        else:
            print("올바르지 않은 입력입니다. 다시 입력해주세요.")
            continue

        # 0을 입력한 경우 사용자 메뉴로 돌아감
        if book_id == '0':
            print("사용자 메뉴로 돌아갑니다.")
            return

        # 유효한 도서 ID 확인
        if not is_valid_book(book_id):
            print("존재하지 않는 도서입니다. 다시 입력해주세요.")
            continue
    title = title.strip()
    found_books = [book for book in self.books if book.title.strip() == title]
    sorted_books = sorted(found_books, key=lambda book: book.book_id)
    print(f"{'도서 ID(도서 구분자)':<9} {'도서 제목':<50} {'출판사':<19} {'저자[이름 구분자]':<29} {'상태':<5}")
    print("=" * 130)
    if sorted_books:
        for book in sorted_books:
            authors_str = ", ".join([f"{author_name} [{author_code}]" for author_code, author_name in book.authors])
            book.is_loaned = book.is_loaned == 'True' or book.is_loaned == True
            status = '대출 중' if book.is_loaned else '대출 가능'
            print(f"{book.book_id}({book.book_code})        {book.title:<52} {book.publisher:<20} {authors_str:<30} {status:<10}")
        print("=" * 130)
    else:
        print(f"'{title}' 제목의 도서를 찾을 수 없습니다.")