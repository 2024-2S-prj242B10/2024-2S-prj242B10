from manager.validation import Validate  

class User:
    def __init__(self, name, user_id, password, loan_count=0, loan_date=None, is_admin=False):
        self.name = name
        self.user_id = user_id
        self.password = password
        self.loan_count = loan_count
        self.loan_date = loan_date
        self.is_admin = is_admin

    def __str__(self):
        return f"{self.name}, {self.user_id}, {self.password}, {self.loan_count}, {self.loan_date}, {self.is_admin}"

class UserManager:
    def __init__(self, file_path):
        self.validate = Validate()
        self.file_path = file_path
        self.users = self.load_users()

    def user_regist(self,user_manager,register_id,register_pw,register_name)->tuple[bool,any]:
        if len(user_manager.users) >=11:
            return False,"현재는 회원가입이 불가능합니다. 초기화면으로 이동합니다."
        else:
            is_id = self.validate.validate_user_id(register_id)
            is_pw = self.validate.validate_user_pw(register_pw)
            is_name = self.validate.validate_user_name(register_name)
            if not (is_id and is_pw and is_name):
                return False,"아이디,비밀번호 또는 이름이 입력 형식에 맞지 않습니다. 다시 입력해 주세요."
            else:
                return True

