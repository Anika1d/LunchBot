from data.user import UserSex, UserStatus
from domain.db import DATABASES


class UserTable:

    def __init__(self):
        self.db = DATABASES

    def create_user(self, chatId: int, userId: int):
        self.db.create_user(chat_id=chatId, userId=userId)

    def setUserName(self, name: str, userId: int):
        self.db.setUserName(name, userId)

    def setUserGender(self, sex: UserSex, userId: int):
        self.db.setUserGender(sex, userId)

    def changeUserStatus(self, userStatus: UserStatus, userId: int):
        self.db.setUserStatus(userStatus, userId)
USER_TABLE = UserTable()
