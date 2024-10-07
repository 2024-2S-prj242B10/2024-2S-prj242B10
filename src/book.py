import csv
import os
import random

class Book:
    def __init__(self, book_id, title, is_loaned=False):
        self.book_id = book_id
        self.title = title
        self.is_loaned = is_loaned

    def __str__(self):
        return f" {self.book_id}, {self.title}, {self.is_loaned}"

class BookManager:
    def __init__(self, book_file_path='data/booklist.txt', loglist_file_path='data/loglist.txt'):
        self.book_file_path = book_file_path
        self.loglist_file_path = loglist_file_path
        self.books = self.load_books()

    def load_books(self):
        books = []
        if os.path.exists(self.book_file_path):
            with open(self.book_file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    book_id, title, is_loaned = row
                    books.append(Book(book_id, title, is_loaned == 'True'))
        else:
            print(f"{self.book_file_path} 파일이 존재하지 않아 새로 생성합니다.")
            os.makedirs(os.path.dirname(self.book_file_path), exist_ok=True)
            with open(self.book_file_path, 'w', encoding='utf-8') as file:
                pass
        return books

    def save_books(self):
        with open(self.book_file_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            for book in self.books:
                writer.writerow([book.book_id, book.title, str(book.is_loaned)])

    def generate_book_id(self):
        existing_ids = {book.book_id for book in self.books}
        while True:
            new_book_id = str(random.randint(1000, 9999))
            if new_book_id not in existing_ids:
                return new_book_id

    def update_loan_status(self):
        with open(self.loglist_file_path, "r", encoding="utf-8") as file:
            loan_status = {}
            for line in file:
                book_id, user_id, is_loaned, date = line.strip().split(", ")
                loan_status[book_id] = is_loaned == "True"

            for book in self.books:
                if book.book_id in loan_status:
                    book.is_loaned = loan_status[book.book_id]

    def loan_book(self, book_id, user_id, date):
        with open(self.loglist_file_path, "a", encoding="utf-8") as file:
            file.write(f"{book_id}, {user_id}, True, {date}\n")
        self.update_loan_status()

    def register_book(self, title):
        new_book_id = self.generate_book_id()
        new_book = Book(new_book_id, title)
        self.books.append(new_book)
        self.save_books()
        print(f"도서 '{title}'이(가) ID '{new_book_id}'로 등록되었습니다.")
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
            print(f"{'도서 ID':<9} {'도서 제목':<53} {'상태':<5}")
            print("=" * 75)
            for book in sorted_books[:count]:
                status = '대출 중' if book.is_loaned else '대출 가능'
                print(f"{book.book_id:<10} {book.title:<55} {status:<10}")
            print("=" * 75)

    def search_book_by_title(self, title):
        title = title.strip()
        found_books = [book for book in self.books if book.title.strip() == title]
        sorted_books = sorted(found_books, key=lambda book: book.book_id)
        print(f"{'도서 ID':<9} {'도서 제목':<53} {'상태':<5}")
        print("=" * 75)
        if sorted_books:
            for book in sorted_books:
                status = '대출 중' if book.is_loaned else '대출 가능'
                print(f"{book.book_id:<10} {book.title:<55} {status:<10}")
            print("=" * 75)
        else:
            print(f"'{title}' 제목의 도서를 찾을 수 없습니다. 사용자 메뉴로 돌아갑니다.")
