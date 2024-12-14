import csv
from datetime import datetime, timedelta
from manager.var import *


# 파일 경로 설정
user_file = 'data/userlist.txt'
book_file = 'data/booklist.txt'
log_file = 'data/loglist.txt'
totallog_file = 'data/totallog.txt'


def is_valid_book(book_id):
    with open(book_file, 'r', encoding='utf-8') as f:
        books = f.readlines()

    # 각 도서 정보를 확인하여 book_id가 존재하는지 검사
    for book in books:
        info = book.split(',')
        if info[1].strip() == book_id:  # 도서 ID가 입력한 ID와 일치하는지 확인
            return True  # 도서 ID가 존재함
    return False  # 도서 ID가 존재하지 않음


def get_current_date():
    with open('data/startdate.txt', 'r', encoding='utf-8') as f:
        date = f.readline().strip()
    return date


def get_user_borrow_info(user_id):
    with open(user_file, 'r', encoding='utf-8') as f:
        users = f.readlines()

    for user in users:
        info = user.split(',')
        if info[1].strip() == user_id:
            borrow_count = int(info[3].strip())  # 대출 권수
            next_borrow_date = info[4].strip()  # 대출 가능 날짜
            return borrow_count, next_borrow_date
    return 0, '2000-01-01'  # 기본값 (유효하지 않은 경우)


def has_overdue_books(user_id, current_date):
    with open(log_file, 'r', encoding='utf-8') as f:
        logs = f.readlines()

    # 로그 파일이 비어있는 경우
    if not logs:
        return False  # 대출 중인 도서가 없음

    # current_date를 datetime 객체로 변환
    current_date_obj = datetime.strptime(current_date, "%Y-%m-%d")

    for log in logs:
        log_info = log.split(',')
        if log_info[1].strip() == user_id and log_info[2].strip() == 'True':  # 대출 중인 도서
            return_date = log_info[3].strip()  # 반납 예정일
            # return_date를 datetime 객체로 변환
            return_date_obj = datetime.strptime(return_date, "%Y-%m-%d")

            # 반납 예정일이 현재 날짜보다 과거인 경우 연체
            if return_date_obj < current_date_obj:
                return True
    return False


# def get_book_title(book_id):
#     with open(book_file, 'r', encoding='utf-8') as f:
#         books = f.readlines()

#     for book in books:
#         info = book.split(',')
#         if info[1].strip() == book_id:
#             return info[2].strip()
#     return ""

def get_book_info(book_id):
    with open(book_file, 'r', encoding='utf-8') as f:
        books = f.readlines()

    for book in books:
        info = book.split(',')
        if info[1].strip() == book_id:
            return info
    return ""



def calculate_return_date(current_date, days):
    date_format = "%Y-%m-%d"
    current = datetime.strptime(current_date, date_format)
    return_date = current + timedelta(days=int(days))
    return return_date.strftime(date_format)


def update_log(user_id, book_id, borrow, return_date):
    updated_logs = []
    is_existing_log = False  # 로그에 기존 도서가 있는지 여부

    with open(log_file, 'r', encoding='utf-8') as f:
        logs = f.readlines()

    # 기존 로그에서 도서 ID와 사용자 ID를 찾아서 수정
    for log in logs:
        log_info = log.split(',')
        if log_info[0].strip() == book_id and log_info[1].strip() == user_id:
            log_info[2] = str(borrow)  # 대출 여부 업데이트
            log_info[3] = return_date+"\n"  # 반납 예정일 업데이트
            updated_logs.append(','.join(log_info))
            is_existing_log = True  # 기존 로그가 업데이트되었음을 표시
        else:
            updated_logs.append(log)

    # 새로운 도서를 대출하는 경우 추가
    if not is_existing_log:
        new_log_entry = f"{book_id},{user_id},{borrow},{return_date}\n"
        updated_logs.append(new_log_entry)

    # 로그 파일에 다시 기록
    with open(log_file, 'w', encoding='utf-8') as f:
        f.writelines(updated_logs)


# totallog.txt 로그 저장 함수
def update_totallog_borrow(user_id, book_id, borrow, return_date):
    current_date = get_current_date()

    log_data = f"{book_id},{user_id},{borrow},{current_date},{return_date}\n"
    #print(log_data)

    # 로그 파일에 다시 기록
    with open(totallog_file, 'a', encoding='utf-8') as f:
        f.writelines(log_data)


def update_totallog_return(user_id, book_id, borrow, return_date):
    current_date = get_current_date()

    log_data = f"{book_id},{user_id},{borrow},{current_date},{return_date}\n"

    # 로그 파일에 다시 기록
    with open(totallog_file, 'a', encoding='utf-8') as f:
        f.writelines(log_data)


# def return_date(user_id, book_id):
#     with open(log_file, 'r', encoding='utf-8') as f:
#         logs = f.readlines()
#
#     for log in logs:
#         log_info = log.split(',')
#         if log_info[0].strip() == book_id and log_info[1].strip() == user_id:
#             # 반납 예정일 리턴
#             return log_info[3].strip()


def update_book_status(book_id):
    updated_books = []
    with open(book_file, 'r', encoding='utf-8') as f:
        books = f.readlines()

    # 도서 목록에서 도서 ID를 찾아서 대출 여부를 True로 변경
    for book in books:
        info = book.split(',')
        if info[1].strip() == book_id:
            info[3] = 'True'  # 대출 여부를 True로 변경
        updated_books.append(','.join(info))

    # 도서 목록을 파일에 다시 기록
    with open(book_file, 'w', encoding='utf-8') as f:
        f.writelines(updated_books)


def update_user_borrow_count(user_id, delta):
    updated_users = []
    with open(user_file, 'r', encoding='utf-8') as f:
        users = f.readlines()

    # 사용자 정보에서 대출 권수 업데이트
    for user in users:
        info = user.split(',')
        if info[1].strip() == user_id:
            borrow_count = int(info[3].strip()) + delta
            info[3] = str(borrow_count)  # 대출 권수 업데이트
            user = ','.join(info)
        updated_users.append(user)

    # 사용자 파일에 다시 기록
    with open(user_file, 'w', encoding='utf-8') as f:
        f.writelines(updated_users)


def is_book_borrowed(book_id):
    with open(book_file, 'r', encoding='utf-8') as f:
        books = f.readlines()

    # 도서 목록에서 도서 ID가 존재하고 대출 여부가 True인지 확인
    for book in books:
        info = book.split(',')
        if info[1].strip() == book_id and info[3].strip() == "True":  # 도서 ID와 대출 여부 확인
            return True  # 도서가 대출 중임
    return False  # 도서가 대출 중이 아님


#--------------------------------
def view_borrowed_books(user_id):
    borrowed_books = []
    with open(log_file, 'r', encoding='utf-8') as f:
        logs = f.readlines()

    for log in logs:
        log_info = log.split(',')
        if log_info[1].strip() == user_id and log_info[2].strip() == 'True':
            book_id = log_info[0].strip()
            book_info = get_book_info(book_id)
            book_code = book_info[0]
            book_title = book_info[2]
            book_publisher = book_info[4]
            book_author = book_info[5]

            print(f"[{book_id}({book_code}) - {book_title} - {book_publisher} - {book_author}] / 대출기한: {log_info[3].strip()}")
            borrowed_books.append(book_id)

    return borrowed_books


def return_book_process(user_id, book_id):
    current_date = get_current_date()  # 현재 가상 날짜
    return_date = get_return_date(book_id, user_id)  # 대출 시 기록된 반납 예정일

    # 날짜 형식 변환: 문자열을 datetime 객체로 변환 (YYYY-MM-DD 형식)
    current_date_obj = datetime.strptime(current_date, "%Y-%m-%d")
    return_date_obj = datetime.strptime(return_date, "%Y-%m-%d")

    updated_users = []
    updated_books = []

    with open(user_file, 'r', encoding='utf-8') as f:
        users = f.readlines()
    with open(book_file, 'r', encoding='utf-8') as f:
        books = f.readlines()

    # 연체 여부 확인 (반납 예정일이 현재 날짜보다 이전이면 연체된 것)
    is_overdue = return_date_obj < current_date_obj

    # 로그 파일에서 도서 반납 처리
    update_log(user_id, book_id, False, current_date)  # 반납 처리

    # 도서 목록에서 도서 ID를 찾아 대출 여부를 False로 변경
    for book in books:
        book_info = book.split(',')
        if book_info[1].strip() == book_id:
            book_info[3] = str(False)
        updated_books.append(','.join(book_info))

    # 변경된 도서 목록을 다시 파일에 기록
    with open(book_file, 'w', encoding='utf-8') as f:
        f.writelines(updated_books)

    # 사용자 파일에서 해당 사용자 정보 업데이트 (대출 가능 권수 감소 및 대출 가능 날짜 변경)
    for user in users:
        user_info = user.split(',')
        if user_info[1].strip() == user_id:
            # 2. 대출 가능 권수 줄이기
            borrow_count = int(user_info[3].strip()) - 1
            user_info[3] = str(borrow_count)

            if is_overdue:
                # 3. 연체된 경우 대출 가능 날짜 계산 및 업데이트
                next_borrow_date = calculate_next_borrow_date(current_date)
                user_info[4] = next_borrow_date  # 대출 가능 날짜를 업데이트

        updated_users.append(','.join(user_info))

    # 사용자 정보 파일에 기록
    with open(user_file, 'w', encoding='utf-8') as f:
        f.writelines(updated_users)

    return is_overdue  # 연체 여부를 반환

def is_book_borrowed_by_user(book_id, user_id):
    with open(log_file, 'r', encoding='utf-8') as f:
        logs = f.readlines()

    # 로그 파일에서 해당 도서가 사용자에게 대출 중인지 확인
    for log in logs:
        log_info = log.split(',')
        if log_info[0].strip() == book_id and log_info[1].strip() == user_id and log_info[2].strip() == 'True':
            return True  # 사용자가 해당 도서를 대출 중임
    return False  # 사용자가 해당 도서를 대출 중이 아님


def get_return_date(book_id, user_id):
    with open(log_file, 'r', encoding='utf-8') as f:
        logs = f.readlines()

    # 로그 파일에서 해당 도서와 사용자에 대한 반납 예정일을 가져옴
    for log in logs:
        log_info = log.split(',')
        if log_info[0].strip() == book_id and log_info[1].strip() == user_id:
            return log_info[3].strip()  # 반납 예정일 반환

    return None  # 해당 도서에 대한 반납 예정일이 없을 경우


def calculate_next_borrow_date(current_date):
    var = Var()
    date_format = "%Y-%m-%d"
    current_date_obj = datetime.strptime(current_date, date_format)  # 현재 날짜를 datetime 객체로 변환
    next_borrow_date_obj = current_date_obj + timedelta(days=int(var.OVERDUE_DATE))  # days일 후 대출 가능
    return next_borrow_date_obj.strftime(date_format)  # 다시 문자열 형식으로 변환하여 반환


# 도서 연혁 조회 관련 함수
def calculate_overdue_days(return_date, expected_date):
    """반납 예정일을 초과한 경우 연체일을 계산"""
    return_date_obj = datetime.strptime(return_date, "%Y-%m-%d")
    expected_date_obj = datetime.strptime(expected_date, "%Y-%m-%d")
    if return_date_obj > expected_date_obj:
        return (return_date_obj - expected_date_obj).days
    return None

def display_book_history_user(totallog_path='data/totallog.txt', booklist_path='data/booklist.txt'):
    """도서 ID를 기반으로 해당 도서의 연혁 출력"""

    while True:
        book_id = input("연혁을 열람할 도서 ID를 입력하세요(0 입력시 사용자 메뉴로 돌아갑니다.): ").strip()

        # 양의 정수 판별
        if book_id.isdigit() and int(book_id) >= 0:
            book_id = str(int(book_id))
        else:
            print("올바르지 않은 입력입니다. 다시 입력해주세요.")
            continue

        # 0을 입력한 경우 사용자 메뉴로 돌아감
        if book_id == '0':
            print("도서 연혁 열람이 취소되었습니다.")
            return

        # 유효한 도서 ID 확인
        if not is_valid_book(book_id):
            print("존재하지 않는 도서입니다. 다시 입력해주세요.")
            continue

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
        var = Var()
        booklist = []
        with open(booklist_path, 'r') as file:
            reader = csv.reader(file)
            for data in reader:
                # 저자 정보 추출: 5번째 인덱스부터 10개의 값을 가져와 2개씩 묶음
                authors = []
                none_authors_cnt = 0
                #max_index = 5 + 5 * 2  # MAX_WRITER_CNT = 5
                
                max_index = 5 + var.MAX_WRITER_CNT * 2
                for i in range(5, max_index, 2):  # 5부터 시작해서 2개씩 건너뛰기 (5~14)
                    author_code = data[i] if i < len(data) else "-"
                    author_name = data[i + 1] if (i + 1) < len(data) else "-"
                    if author_code.strip("[]") == '-' and author_name.strip("[]") == '-':
                        none_authors_cnt += 1
                    else:
                        authors.append((author_code.strip("[]"), author_name.strip("[]")))
                if none_authors_cnt == var.MAX_WRITER_CNT:
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
                # 삭제된 도서는 제외
                # if not book['delete_date']:
                booklist.append(book)

        # 주어진 도서 ID에 해당하는 도서 정보 검색
        book = next((b for b in booklist if b['book_id'] == book_id), None)

        if book['delete_date']:
            print(f"도서 ID [{book_id}]는 삭제된 도서입니다.")
            print("사용자 메뉴로 돌아갑니다.")
            return

        if not book:
            print(f"도서 ID [{book_id}]에 해당하는 기록이 없습니다.")
            print("사용자 메뉴로 돌아갑니다.")
            return

        # 도서 연혁 출력
        print(f"[{book_id}] - [{book['book_identifier']}] - [{book['title']}] - "
              f"[{', '.join(['-'.join(author) if isinstance(author, tuple) else author for author in book['authors']])}] - [{book['publisher']}]에 대한 연혁입니다.")
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
            print(f"{book['delete_date']} 삭제")  # 삭제일 출력 (실제로는 삭제된 도서는 나오지 않음)

        print("사용자 메뉴로 돌아갑니다.")
        return