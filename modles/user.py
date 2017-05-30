from common.database import Database


class user(object):
    def __init__(self, account, password, email):
        self.account = account
        self.password = password
        self.email = email

    def account_valid(account, password):
        user_data = Database.find_one('user', {"account": account})
        if user_data is None:
            return False
        if user_data['password'] != password:
            return False
        return True

    def register_user(account, password, email):
        user_data = Database.find_one('user', {"account": account})
        if user_data.count() > 0:
            return False
        user(account, password, email).save_to_DB()
        return True

    def save_to_DB(self):
        Database.insert(collection='user', data=self.to_json())

    def to_json(self):
        return {
            "account": self.account,
            "password": self.password,
            "email": self.email
        }

    def find_user_data(account):
        user_data = Database.find(collection='user', query={"account": account})
        return
