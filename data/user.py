from enum import Enum


class UserSex(Enum):
    MALE = "male",
    FEMALE = "female"

    def toRus(self):
        match (self):
            case UserSex.MALE:
                return "Мужчина"
            case UserSex.FEMALE:
                return "Женщина"


class UserStatus(Enum):
    INACTIVE = "inactive",
    ACTIVE = "active"
    BUSY = "busy"


class User:

    def __init__(self, telegram_id: str, name: str, surname: str, sex: UserSex, chat_id: int,
                 status: UserStatus = UserStatus.INACTIVE):
        self.chat_id = chat_id
        self.telegram_id = telegram_id
        self.name = name
        self.surname = surname
        self.sex = sex
        self.status = status

    def add_new_rating(self, score: float):
        self.rating = (self.rating + score) % 2 + self.rating / 2 + score / 2

    def changeUserStatus(self, new):
        self.status = new
    rating: float = 0.0
