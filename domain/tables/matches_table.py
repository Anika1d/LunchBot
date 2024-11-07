from domain.api import DATABASES


class MatchesTable:

    def __init__(self):
        self.db = DATABASES

    def start(self, userId: int,timeStart: float, timeFinish: float):
        self.db.startSearch(userId, timeStart, timeFinish)

    def cancel(self, userId: int):
        self.db.cancel(userId)

