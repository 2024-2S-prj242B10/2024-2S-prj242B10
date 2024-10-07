import re
from src.book import BookManager

def validate_book_title(title):
    if re.fullmatch(r'^[a-zA-Z가-힣\s]{1,50}$', title):
        return True
    return False

def validate_book_id(book_id):
    if book_id.isdigit():
        book_id = int(book_id)
        if 1000 <= book_id <= 9999:
            return True
    return False

def validate_book_exist(book_id):
    return any(book.book_id == book_id for book in BookManager().books)

def validate_book_can_borrow(book_id):
    for book in BookManager().books:
        if book.book_id == book_id:
            return not book.is_loaned
    return False