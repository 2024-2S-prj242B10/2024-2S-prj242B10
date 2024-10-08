import csv
import os
import random

class Book:
    def __init__(self, title, book_id, is_loaned=False):
        self.title = title
        self.book_id = book_id
        self.is_loaned = is_loaned

    def __str__(self):
        return f"{self.title}, {self.book_id}, {self.is_loaned}"

class BookManager:
    def __init__(self, file_path='data/booklist.txt'):
        self.file_path = file_path
        self.books = self.load_books()

    def load_books(self):
        books = []
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    title, book_id, is_loaned = row
                    books.append(Book(title, book_id, is_loaned == 'True'))
        return books

    def save_books(self):
        with open(self.file_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            for book in self.books:
                writer.writerow([book.title, book.book_id, book.is_loaned])

    def generate_book_id(self):
        existing_ids = {book.book_id for book in self.books}
        while True:
            new_book_id = str(random.randint(1000, 9999))
            if new_book_id not in existing_ids:
                return new_book_id

    def register_book(self, title):
        new_book_id = self.generate_book_id()
        new_book = Book(title, new_book_id)
        self.books.append(new_book)
        self.save_books()
        print(f"책 '{title}'이(가) ID '{new_book_id}'로 등록되었습니다.")

    def delete_book(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                self.books.remove(book)
                self.save_books()
                print(f"책 '{book.title}'이(가) 삭제되었습니다.")
                return
        print(f"ID가 {book_id}인 책을 찾을 수 없습니다.")

    def display_books(self, count=None):
        if not self.books:
            print("등록된 책이 없습니다.")
        else:
            sorted_books = sorted(self.books, key=lambda book: int(book.book_id))
            if count is None or count > len(sorted_books):
                count = len(sorted_books)
            for book in sorted_books[:count]:
                print(f"책 ID: {book.book_id}, 제목: {book.title}, 상태: {'대출 중' if book.is_loaned else '대출 가능'}")

    def search_book(self, title):
        found_books = [book for book in self.books if title.lower() in book.title.lower()]
        if found_books:
            for book in found_books:
                print(book)
        else:
            print(f"'{title}' 제목의 책을 찾을 수 없습니다.")