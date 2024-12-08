import csv
import os
import random
from datetime import datetime

from manager.var import Var as var
from src.user_utils import is_valid_book, calculate_overdue_days


class Book:
    def __init__(self, book_id, title, publisher, authors, book_code, is_loaned=False, registered_date=None, deleted_date=""):
        self.book_id = book_id
        self.title = title
        self.publisher = publisher
        self.authors = authors
        self.book_code = book_code
        self.is_loaned = is_loaned
        self.registered_date = registered_date  # 생성일
        self.deleted_date = deleted_date        # 삭제일

    def __str__(self):
        #authors_str = ', '.join([f"{author[0]} [{author[1]}]" for author in self.authors])
        authors_str = ", ".join([f"{author_name} [{author_code}]" for author_code, author_name in self.authors if author_code != "-" or author_name != "-"])
        return (f"도서 ID: {self.book_id}, 도서 구분자: {self.book_code}, 제목: {self.title}, "
                f"출판사: {self.publisher}, 저자: {authors_str}, 대출 상태: {'대출 중' if self.is_loaned else '대출 가능'}")

class BookManager:
    def __init__(self, book_file_path='data/booklist.txt'):
        self.book_file_path = book_file_path
        self.books = self.load_books()
        self.authors = self.build_authors()

    def load_books(self):
        books = []
        if os.path.exists(self.book_file_path):
            with open(self.book_file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    # 기본 정보 추출
                    book_code = row[0]      # 도서 구분자
                    book_id = row[1]        # 도서 ID
                    title = row[2]          # 도서 제목
                    is_loaned = row[3] == 'True'  # 대출 상태
                    publisher = row[4]      # 출판사

                    # 저자 정보 추출: 5번째 인덱스부터 10개의 값을 가져와 2개씩 묶음
                    authors = []
                    max_index = 5 + var.MAX_WRITER_CNT * 2
                    for i in range(5, max_index, 2):  # 5부터 시작해서 2개씩 건너뛰기 (5~14)
                        author_code = row[i] if i < len(row) else "-"
                        author_name = row[i+1] if (i+1) < len(row) else "-"
                        authors.append((author_code.strip("[]"), author_name.strip("[]")))

                    # 등록일과 삭제일 추출
                    registered_date = row[max_index] if len(row) > max_index else ""  # 등록일
                    deleted_date = row[max_index+1] if len(row) > max_index+1 else ""     # 삭제일

                    # Book 객체 생성 및 리스트에 추가
                    books.append(Book(
                        book_id=book_id,
                        title=title,
                        publisher=publisher,
                        authors=authors,
                        book_code=book_code,
                        is_loaned=is_loaned,
                        registered_date=registered_date,
                        deleted_date=deleted_date
                    ))
        return books

    def save_books(self):
        with open("data/startdate.txt", 'r', encoding='utf-8') as date_file:
            start_date = date_file.readline().strip()  # 첫 번째 줄 읽기 및 공백 제거

        # 도서 정보를 파일에 저장
        with open(self.book_file_path, 'w', encoding='utf-8') as file:
            for book in self.books:
                # 기본 정보 저장
                row = [
                    book.book_code,  # 도서 구분자
                    book.book_id,    # 도서 ID
                    book.title,      # 도서 제목
                    str(book.is_loaned),  # 대출 상태
                    book.publisher   # 출판사
                ]

                # 저자 목록을 [이름,코드] 형식으로 추가
                for author_name, author_code in book.authors:
                    row.append(f"[{author_name},{author_code}]")

                # 등록일과 삭제일 추가
                row.append(book.registered_date)  # startdate.txt에서 읽어온 등록일
                row.append(book.deleted_date) # 삭제일은 공백

                # 쉼표로 구분된 문자열로 변환 후 파일에 쓰기
                file.write(",".join(row) + "\n")



    def build_authors(self):
        authors = {}
        for book in self.books:
            for author_code, author_name in book.authors:
                if author_name != '-' and author_code not in authors:
                    authors[author_code] = author_name
        return authors

    def generate_book_id(self):
        existing_ids = {book.book_id for book in self.books}
        while True:
            new_book_id = str(random.randint(1000, 9999))
            if new_book_id not in existing_ids:
                return new_book_id

    def generate_book_code(self):
        existing_codes = {book.book_code for book in self.books}
        while True:
            new_book_code = str(random.randint(100, 999))
            if new_book_code not in existing_codes:
                return new_book_code

    def generate_author_code(self):
        existing_codes = set(self.authors.keys())
        while True:
            new_author_code = str(random.randint(100, 999))
            if new_author_code not in existing_codes:
                return new_author_code

    def add_author(self, author_name, current_authors):
        # 기존 authors와 현재 도서의 입력된 저자 리스트에서 중복 검사
        existing_author_codes = self.check_duplicate_author(author_name)
        current_author_codes = [code for code, name in current_authors if name == author_name]

        all_author_codes = list(set(existing_author_codes + current_author_codes))

        if all_author_codes:  # 중복된 이름이 존재할 경우
            print("[동일한 이름의 저자가 존재합니다. 저자를 선택해주세요.]")
            for code in all_author_codes:
                print(f"[{code}] - 저자: {author_name}")

            chosen_code = input("선택할 저자의 구분자를 입력하세요 (새로운 저자를 등록하려면 0을 입력하세요): ").strip()

            # 사용자가 선택한 저자 코드가 현재 저자 리스트에 이미 있는 경우
            if chosen_code in [code for code, _ in current_authors]:
                print("올바르지 않은 입력입니다. 관리자 메뉴로 돌아갑니다.")
                return None, None

            if chosen_code == '0':
                author_code = self.generate_author_code()
            elif chosen_code in all_author_codes:
                author_code = chosen_code
            else:
                print("올바르지 않은 입력입니다. 관리자 메뉴로 돌아갑니다.")
                return None, None
        else:
            # 중복이 없을 경우 새로운 코드 생성
            author_code = self.generate_author_code()

        return author_code, author_name


    def check_duplicate_author(self, author_name):
        return [code for code, name in self.authors.items() if name == author_name]


    def register_book(self, title, publisher, author_list):
        book_code = self.generate_book_code()
        duplicate_books = []  # 중복된 도서 목록 저장

        # 시작 날짜 읽기
        with open("data/startdate.txt", 'r', encoding='utf-8') as date_file:
            start_date = date_file.readline().strip()

        # 제목, 출판사, 저자가 같은 도서 찾기
        for book in self.books:
            if book.title == title and book.publisher == publisher and book.authors == author_list:
                duplicate_books.append((book.book_code, book.title))

        # 중복 도서가 있을 경우
        if duplicate_books:
            print("[동일한 제목, 출판사, 저자의 도서가 존재합니다. 추가 등록할 도서를 선택해주세요.]")
            for code, name in duplicate_books:
                print(f"[{code}] - 도서명: {name}")

            chosen_code = input("선택할 도서의 구분자를 입력하세요 (새로운 도서를 등록하려면 0을 입력하세요): ").strip()

            # 사용자가 0을 입력하면 새로운 도서로 등록
            if chosen_code == '0':
                print("새로운 도서로 등록합니다.")
            elif chosen_code in [code for code, _ in duplicate_books]:
                print(f"선택된 도서 [{chosen_code}]에 대한 추가 등록을 진행합니다.")
                book_code = chosen_code  # 기존 도서의 book_code 사용
            else:
                print("올바르지 않은 입력입니다. 관리자 메뉴로 돌아갑니다.")
                return  # 등록 중단

        # 새로운 도서 등록
        new_book_id = self.generate_book_id()
        new_book = Book(new_book_id, title, publisher, author_list, book_code, False, start_date)
        self.books.append(new_book)
        self.save_books()

        # 저자 리스트를 authors에 추가
        for code, name in author_list:
            if code != '-':
                self.authors[code] = name


        authors_str = ", ".join([f"{author_name} [{author_code}]" for author_code, author_name in author_list if author_code != "-" or author_name != "-"])

        print(f"도서 '{title}'이(가) 등록되었습니다. 도서 ID: {new_book_id}, 도서 구분자: {book_code}, 저자: {authors_str}")
        print("관리자 메뉴로 돌아갑니다.")



    def delete_book(self, book_id):
        with open("data/startdate.txt", 'r', encoding='utf-8') as date_file:
            delete_date = date_file.readline().strip()  # 첫 번째 줄 읽기 및 공백 제거

        for book in self.books:
            if book.book_id == book_id:
                # self.books.remove(book)
                book.deleted_date = delete_date  # 삭제일 필드에 삭제 날짜 기록
                self.save_books()
                print(f"도서 '{book.title}'이(가) 삭제되었습니다.")
                return
        print(f"ID가 {book_id}인 도서를 찾을 수 없습니다.")

    def display_books(self, count=None):
        if not self.books:
            print("등록된 책이 없습니다.")
        else:
            sorted_books = sorted(self.books, key=lambda book: book.book_id)
            if count is None or count > len(sorted_books):
                count = len(sorted_books)
            print(f"{'도서 ID(도서 구분자)':<9} {'도서 제목':<50} {'출판사':<19} {'저자[이름 구분자]':<29} {'상태':<5}")
            print("=" * 130)
            for book in sorted_books[:count]:
                #authors_str = ", ".join([f"{author_name} [{author_code}]" for author_code, author_name in book.authors])
                authors_str = ", ".join([f"{author_name} [{author_code}]" for author_code, author_name in book.authors if author_code != "-" or author_name != "-"])

                book.is_loaned = book.is_loaned == 'True' or book.is_loaned == True
                status = '대출 중' if book.is_loaned else '대출 가능'
                print(f"{book.book_id}({book.book_code})        {book.title:<52} {book.publisher:<20} {authors_str:<30} {status:<10}")
            print("=" * 130)

    def search_book_by_title(self, title):
        title = title.strip()
        found_books = [book for book in self.books if book.title.strip() == title]
        sorted_books = sorted(found_books, key=lambda book: book.book_id)
        print(f"{'도서 ID(도서 구분자)':<9} {'도서 제목':<50} {'출판사':<19} {'저자[이름 구분자]':<29} {'상태':<5}")
        print("=" * 130)
        if sorted_books:
            for book in sorted_books:
                #authors_str = ", ".join([f"{author_name} [{author_code}]" for author_code, author_name in book.authors])
                authors_str = ", ".join([f"{author_name} [{author_code}]" for author_code, author_name in book.authors if author_code != "-" or author_name != "-"])
                book.is_loaned = book.is_loaned == 'True' or book.is_loaned == True
                status = '대출 중' if book.is_loaned else '대출 가능'
                print(f"{book.book_id}({book.book_code})        {book.title:<52} {book.publisher:<20} {authors_str:<30} {status:<10}")
            print("=" * 130)
        else:
            print(f"'{title}' 제목의 도서를 찾을 수 없습니다.")

    def search_book_by_id(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None


    def update_loan_overdue_date(self):
        arrow = [0,1,2]
        while True:
            print("-------------------------------------------")
            print("[대출 및 연체 기간 수정]")

            print("0. 뒤로가기")
            print("1. 대출 기간 수정")
            print("2. 연체 패널티 기간 수정")
            command = input("원하는 메뉴의 번호를 입력해 주세요: ").strip()

            if command.isdigit():
                command = int(command)
            else:
                print('올바르지 않은 입력형식입니다. 다시 입력해주세요.')
                continue

            if command in arrow:
                if command == 0:
                    #print("뒤로가기")
                    break
                elif command == 1:
                    self.update_loan_date()
                    break
                elif command == 2:
                    self.update_overdue_date()
                    break
            else:
                print("올바르지 않은 입력형식입니다. 다시 입력해주세요.")  # 오류 메시지 출력

        return None


    def update_loan_date(self):
        print("-------------------------------------------")
        print("[대출 기간 수정]")
        from manager.var import Var as var
        print("현재 대출 기간: "+str(var.LOAN_DATE)+"일")
        while True:

            command = input("변경을 희망하는 대출 기간을 입력해 주세요: ").strip()

            if command.isdigit():
                command = int(command)
            else:
                print('올바르지 않은 입력형식입니다. 다시 입력해주세요.')
                continue

            if command < 1 or command > 100:
                print('변경 가능한 대출 기간은 1일 이상, 100일 이하입니다.')
                continue
            break

        var.LOAN_DATE = command

        with open('data/startinfo.txt', 'w', encoding='utf-8') as file:
            file.write(str(var.LOAN_DATE)+","+str(var.OVERDUE_DATE))

        print("대출 기간이 "+str(var.LOAN_DATE)+"일로 수정되었습니다.")
        print("관리자 메뉴로 돌아갑니다.")
        return None

    def update_overdue_date(self):
        print("-------------------------------------------")
        print("[연체 기간 수정]")
        from manager.var import Var as var
        print("현재 연체 기간: "+str(var.OVERDUE_DATE)+"일")
        while True:
            command = input("변경을 희망하는 연체 기간을 입력해 주세요: ").strip()

            if command.isdigit():
                command = int(command)
            else:
                print('올바르지 않은 입력형식입니다. 다시 입력해주세요.')
                continue

            if command < 1 or command > 100:
                print('변경 가능한 연체 기간은 1일 이상, 100일 이하입니다.')
                continue

            break


        var.OVERDUE_DATE = command

        with open('data/startinfo.txt', 'w', encoding='utf-8') as file:
            file.write(str(var.LOAN_DATE)+","+str(var.OVERDUE_DATE))

        print("연체 기간이 "+str(var.OVERDUE_DATE)+"일로 수정되었습니다.")
        print("관리자 메뉴로 돌아갑니다.")
        return None



def display_book_history_admin(totallog_path='data/totallog.txt', booklist_path='data/booklist.txt'):
    """도서 ID를 기반으로 해당 도서의 연혁 출력"""

    while True:
        book_id = input("연혁을 조회할 도서 ID를 입력하세요(0 입력시 관리자 메뉴로 돌아갑니다.): ").strip()

        # 양의 정수 판별
        if book_id.isdigit() and int(book_id) >= 0:
            book_id = str(int(book_id))
        else:
            print("올바르지 않은 입력입니다. 다시 입력해주세요.")
            continue
        # 0을 입력한 경우 사용자 메뉴로 돌아감
        if book_id == '0':
            print("도서 연혁 조회가 취소되었습니다.")
            return

        # 대출 및 반납 기록 파일 로드
        totallog = []
        with open(totallog_path, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                record = {
                    'book_id': data[0],  # 도서 ID
                    'user_id': data[1],  # 사용자 ID
                    'borrowed': data[2] == 'True',  # 대출 여부
                    'date': data[3],  # 대출 또는 반납일
                    'expected_date': data[4]  # 반납 예정일
                }
                totallog.append(record)

        # 도서 정보 파일 로드
        booklist = []
        with open(booklist_path, 'r') as file:
            reader = csv.reader(file)
            for data in reader:
                # 저자 정보 추출: 5번째 인덱스부터 10개의 값을 가져와 2개씩 묶음
                authors = []
                none_authors_cnt = 0
                max_index = 5 + var.MAX_WRITER_CNT * 2
                for i in range(5, max_index, 2):  # 5부터 시작해서 2개씩 건너뛰기 (5~14)
                    author_code = data[i] if i < len(data) else "-"
                    author_name = data[i + 1] if (i + 1) < len(data) else "-"
                    if author_code.strip("[]") == '-' and author_name.strip("[]") == '-':
                        none_authors_cnt+=1
                    else:
                        authors.append((author_code.strip("[]"), author_name.strip("[]")))
                    if none_authors_cnt == 5:
                        authors.append("-")

                book = {
                    'book_id': data[1],  # 도서 ID
                    'book_identifier': data[0],  # 도서 구분자
                    'title': data[2],  # 도서 제목
                    'borrowed': data[3] == 'True',  # 도서 대출 여부
                    'publisher': data[4],  # 출판사
                    'authors': authors,
                    'entry_date': data[-2] if len(data) >= 11 else None,  # 등록일
                    'delete_date': data[-1] if len(data) > 11 else None  # 삭제일
                }
                booklist.append(book)
        # 주어진 도서 ID에 해당하는 도서 정보 검색
        book = next((b for b in booklist if b['book_id'] == book_id), None)
        if not book:
            print(f"도서 ID [{book_id}]에 해당하는 기록이 없습니다.")
            return

        # 도서 연혁 출력
        print(f"[{book_id}] - [{book['book_identifier']}] - [{book['title']}] - "
              f"[{book['authors']}] - [{book['publisher']}]에 대한 연혁입니다.")
        print("대출 및 반납 내역")

        if book['entry_date']:
            print(f"{book['entry_date']} 등록")  # 등록일 출력

        # 대출 및 반납 내역 출력
        for log in sorted([l for l in totallog if l['book_id'] == book_id],
                          key=lambda x: x['date']):
            if log['borrowed']:
                print(f"{log['date']} 대출 [{log['user_id']}] - [{log['expected_date']}]")
            else:
                overdue = calculate_overdue_days(log['date'], log['expected_date'])
                overdue_text = f"- [{overdue}일 연체]" if overdue else ""
                print(f"{log['date']} 반납 [{log['user_id']}] {overdue_text}")

        if book['delete_date']:
            print(f"{book['delete_date']} 삭제")  # 삭제일 출력

        print("관리자 메뉴로 돌아갑니다.")
        return
