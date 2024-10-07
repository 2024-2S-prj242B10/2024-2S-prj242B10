import csv
import os
from manager.validation import Validate 

class User:
    def __init__(self,user_name, user_id, user_password, loan_count=0, loan_date=None, is_admin=False):
        self.user_name = user_name
        self.user_id = user_id
        self.user_password = user_password
        self.loan_count = loan_count
        self.loan_date = loan_date
        self.is_admin = is_admin

    def __str__(self):
        return f"{self.user_name}, {self.user_id}, {self.user_password}, {self.loan_count}, {self.loan_date}, {self.is_admin}"

class UserManager:
    def __init__(self, user_file_path="data/userlist.txt"):
        self.validate = Validate()
        self.user_file_path = user_file_path
        self.users = self.load_users()
    
    def add_user(self,register_name,register_id,register_pw):
        new_user = User(register_name,register_id,register_pw,0,None,False)
        self.users.append(new_user)
        with open(self.user_file_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            for user in self.users:
                writer.writerow([user.user_name,user.user_id,user.user_password,user.loan_count,user.loan_date, str(user.is_admin)])

    def load_users(self):
        users = []
        if os.path.exists(self.user_file_path):
            with open(self.user_file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    user_name, user_id, user_password,loan_count,loan_date,is_admin = row
                    users.append(User(user_name, user_id,user_password,loan_count,loan_date,is_admin))
        else:
            print(f"{self.user_file_path} 파일이 존재하지 않아 새로 생성합니다.")
            os.makedirs(os.path.dirname(self.user_file_path), exist_ok=True)
            with open(self.user_file_path, 'w', encoding='utf-8') as file:
                file.write("ADMIN,admin,a1234,0,2000-01-01,False")
        return users


    def user_login(self,user_manager,logined_id,logined_pw)->tuple[bool,bool]:
        logined_id = logined_id.strip()
        logined_pw = logined_pw.strip()
        is_valid = False
        is_manager = False
        for user in user_manager.users:
            if (logined_id == user.user_id and logined_pw == user.user_pw):
                is_valid = True
                if logined_id =='admin':
                    is_manager = True
        return is_valid,is_manager
            


    def user_regist(self,user_manager,register_id,register_pw,register_name)->tuple[bool,any]:
        if len(user_manager.users) >=11:
            return False,"현재는 회원가입이 불가능합니다. 초기화면으로 이동합니다."
        else:
            #선 후 공백 제거
            register_id = register_id.strip()
            register_pw = register_pw.strip()
            register_name = register_name.strip()
            
            is_id = self.validate.validate_user_id(register_id)
            is_pw = self.validate.validate_user_pw(register_pw)
            is_name = self.validate.validate_user_name(register_name)
            if not (is_id and is_pw and is_name):
                return False,"아이디,비밀번호 또는 이름이 입력 형식에 맞지 않습니다. 다시 입력해 주세요."
            else:
                return True

