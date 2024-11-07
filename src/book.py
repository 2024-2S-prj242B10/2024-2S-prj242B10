import csv
import os
import random

class Book:
    def __init__(self, book_id, title, publisher, authors, book_code, is_loaned=False):
        self.book_id = book_id
        self.title = title
        self.publisher = publisher
        self.authors = authors
        self.book_code = book_code
        self.is_loaned = is_loaned

    def __str__(self):
        authors_str = ', '.join([f"{author[0]} [{author[1]}]" for author in self.authors])
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
                    book_code, book_id, title, is_loaned, publisher, author_name, author_code = row
                    authors = [(author_code, author_name)]
                    books.append(Book(book_id, title, publisher, authors, book_code, is_loaned == 'True'))
        return books

    def save_books(self):
        with open(self.book_file_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            for book in self.books:
                author_code, author_name = book.authors[0]
                writer.writerow(
                    [book.book_code, book.book_id, book.title, str(book.is_loaned), book.publisher, author_name, author_code])

    def build_authors(self):
        authors = {}
        for book in self.books:
            for author_code, author_name in book.authors:
                if author_code not in authors:
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

    def add_author(self, author_name):
        existing_author_codes = self.check_duplicate_author(author_name)
        if existing_author_codes:
            print("[동일한 이름의 저자가 존재합니다. 저자를 선택해주세요.]")
            for code in existing_author_codes:
                print(f"[{code}] - 저자: {author_name}")
            chosen_code = input("선택할 저자의 이름 구분자를 입력하세요 (새로운 저자를 등록하는 경우 0을 입력하세요): ").strip()
            if chosen_code == '0':
                author_code = self.generate_author_code()
            elif chosen_code in existing_author_codes:
                author_code = chosen_code
            else:
                print("올바르지 않은 입력입니다.")
                return None, None
        else:
            author_code = self.generate_author_code()

        self.authors[author_code] = author_name
        return author_code, author_name

    def check_duplicate_author(self, author_name):
        return [code for code, name in self.authors.items() if name == author_name]

    def register_book(self, title, publisher, author_list):
        book_code = self.generate_book_code()
        for book in self.books:
            if book.title == title and book.publisher == publisher and book.authors == author_list:
                book_code = book.book_code
                print("기존에 동일한 도서가 존재합니다.")
                confirm_duplicate = input(
                    "동일한 도서에 대해 추가 등록하시겠습니까? (y / 다른 키를 입력하면 취소합니다.): ").strip()
                if confirm_duplicate != 'y':
                    print("중복된 도서가 이미 존재합니다. 관리자 메뉴로 돌아갑니다.")
                    return
                break

        new_book_id = self.generate_book_id()
        new_book = Book(new_book_id, title, publisher, author_list, book_code)
        self.books.append(new_book)
        self.save_books()

        print(f"도서 '{title}'이(가) 등록되었습니다. 도서 ID: {new_book_id}, 도서 구분자: {book_code}, 저자: {author_list}")
        print("관리자 메뉴로 돌아갑니다.")

    def delete_book(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                self.books.remove(book)
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
            print(f"{'도서 ID':<9} {'도서 제목':<28} {'출판사':<19} {'저자':<29} {'상태':<5}")
            print("=" * 100)
            for book in sorted_books[:count]:
                authors_str = ", ".join([f"{author_name} [{author_code}]" for author_code, author_name in book.authors])
                status = '대출 중' if book.is_loaned else '대출 가능'
                print(f"{book.book_id}({book.book_code})  {book.title:<30} {book.publisher:<20} {authors_str:<30} {status:<10}")
            print("=" * 100)

    def search_book_by_title(self, title):
        title = title.strip()
        found_books = [book for book in self.books if book.title.strip() == title]
        sorted_books = sorted(found_books, key=lambda book: book.book_id)
        print(f"{'도서 ID':<9} {'도서 제목':<28} {'출판사':<19} {'저자':<29} {'상태':<5}")
        print("=" * 100)
        if sorted_books:
            for book in sorted_books:
                authors_str = ", ".join([f"{author_name} [{author_code}]" for author_code, author_name in book.authors])
                status = '대출 중' if book.is_loaned else '대출 가능'
                print(f"{book.book_id}({book.book_code})  {book.title:<30} {book.publisher:<20} {authors_str:<30} {status:<10}")
            print("=" * 100)
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
            command = input("원하는 메뉴의 번호를 입력해 주세요: ")

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
            
            command = input("변경을 희망하는 대출 기간을 입력해 주세요: ")

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
            command = input("변경을 희망하는 연체 기간을 입력해 주세요: ")

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
    
    