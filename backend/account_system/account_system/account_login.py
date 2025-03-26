from auth import Account

class AccountLogin(Account):
    
    def __init__(self, loginID: str, password: str):
        super().__init__(loginID, password)

    def authenticate(self, loginID, password):
        return super().authenticate(loginID, password)
    
