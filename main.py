import os
import sys
from src.book import BookManager
from manager.validation import validate_book_title, validate_book_id, validate_book_exist, validate_book_can_borrow,File_util
from manager.ui import admin_menu
from src.user import UserManager
from src.date_manager import Date_manager


def main():
    #무결성 검사
    file_util = File_util()
    file_util.validate_startdate_file
    file_util.validate_booklist_file
    file_util.validate_userlist_file
    file_util.validate_loglist_file

    date_manager = Date_manager()
    date_manager.read_file()

    #가상날짜 입력 프롬프트
    while True:  # 잘못된 입력이면 모드 선택 프롬프트 반복
            print("-------------------------------------------")
            print("프로그램을 종료하려면 숫자 0을 입력해주세요.")
           
            command = input("프로그램에서 사용할 날짜를 입력해주세요 (yyyy-mm-dd):")
            
            is_valid, insert = date_manager.parse_insert(command)
            
            if is_valid:
                if insert==0: # 0을 입력해 종료하려는 경우
                    os.system('pause')
                    sys.exit()
                else:
                    break
    
    #loan_manager = LoanManaer()
    user_manager = UserManager()
    book_manager = BookManager()

    
    while True:
        admin_menu()
        choice = int(input("원하는 메뉴의 번호를 입력해주세요: "))

        if choice == 0:
            print("로그아웃 되었습니다.")
            break

        if choice == 1:
            print("등록할 도서의 정보를 입력해주세요.")
            register_title = input("도서 제목: ").strip()
            if validate_book_title(register_title):
                if input("도서를 등록하시겠습니까? (y / 다른 키를 입력하면 등록을 취소하고 관리자 메뉴로 이동합니다.):").strip() == 'y':
                    book_manager.register_book(register_title)
                else:
                    print("도서 등록을 취소합니다. 관리자 메뉴로 돌아갑니다.")
                    pass
            else:
                print("올바르지 않은 입력형식입니다. 관리자 메뉴로 돌아갑니다.")

        elif choice == 2:
            print("삭제할 도서의 정보를 입력해주세요.")
            book_id = input("도서 ID: ").strip()
            if validate_book_id(book_id):
                if validate_book_exist(book_id):
                    if validate_book_can_borrow(book_id):
                        if input("도서를 삭제하시겠습니까? (y / 다른 키를 입력하면 등록을 취소하고 관리자 메뉴로 이동합니다.):").strip() == 'y':
                            book_manager.delete_book(book_id)
                        else:
                            print("도서 등록을 취소합니다. 관리자 메뉴로 돌아갑니다.")
                            pass
                    else:
                        print("대출중인 도서는 삭제할 수 없습니다. 관리자 메뉴로 돌아갑니다.")
                else:
                    print(f"존재하지 않는 도서입니다. 관리자 메뉴로 돌아갑니다.")
            else:
                print("올바르지 않은 입력형식입니다. 관리자 메뉴로 돌아갑니다.")

        elif choice == 3:
            print("[도서 검색]")
            search_title = input("\n검색할 도서 제목을 입력해주세요: ").strip()
            book_manager.search_book_by_title(search_title)

        elif choice == 4:
            print("[도서 목록]")
            book_manager.display_books()

        else:
            print("올바르지 않은 입력형식입니다. 다시 입력해주세요.")


if __name__ == "__main__":
    main()
