from enum import Enum

class UserSex(Enum):
    MALE = "male",
    FEMALE = "female"


class User:
    def __init__(self, telegram_id: str, name: str, surname: str, sex: UserSex):
        self.telegram_id = telegram_id
        self.name = name
        self.surname = surname
        self.sex = sex


