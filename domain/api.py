import psycopg2

from data.user import UserSex, User

psycopg2


class Databases:

    def __init__(self):
        DATABASE_URL = "postgresql://postgres:2002@localhost:5432/tg_LunchBot"

        create_tables_sql = """
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            tg_id BIGINT UNIQUE NOT NULL,
            username VARCHAR(255),
            phone_number VARCHAR(20),
            rating REAL,
            gender VARCHAR(10) CHECK (gender IN ('Мужской', 'Женский', 'Другой'))
        );

        CREATE TABLE matches (
            match_id SERIAL PRIMARY KEY,
            matched_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE preferences (
            preference_id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
            preferred_time TIME,
            diet TEXT,
            additional_preferences TEXT
        );


        CREATE TABLE match_participants (
            match_participant_id SERIAL PRIMARY KEY,
            match_id INTEGER REFERENCES matches(match_id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE
        );
        """

        try:
            self.conn = psycopg2.connect(DATABASE_URL)
            self.cur = self.conn.cursor()

            self.cur.execute(create_tables_sql)
            self.conn.commit()

            print("Таблицы успешно созданы!")

        except psycopg2.Error as e:
            print(f"Ошибка при создании таблиц: {e}")

    def setUserName(self, name: str, userId: int):
        self.cur.execute("")

    def setUserGender(self, sex: UserSex, userId: int):
        self


class Databases:

    def __init__(self):
        DATABASE_URL = "postgresql://postgres:2002@localhost:5432/tg_LunchBot"

        create_tables_sql = """
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            tg_id BIGINT UNIQUE NOT NULL,
            username VARCHAR(255),
            phone_number VARCHAR(20),
            rating REAL,
            gender VARCHAR(10) CHECK (gender IN ('Мужской', 'Женский', 'Другой'))
        );

        CREATE TABLE matches (
            match_id SERIAL PRIMARY KEY,
            matched_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE preferences (
            preference_id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
            preferred_time TIME,
            diet TEXT,
            additional_preferences TEXT
        );


        CREATE TABLE match_participants (
            match_participant_id SERIAL PRIMARY KEY,
            match_id INTEGER REFERENCES matches(match_id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE
        );
        """

        try:
            self.conn = psycopg2.connect(DATABASE_URL)
            self.cur = self.conn.cursor()

            self.cur.execute(create_tables_sql)
            self.conn.commit()

            print("Таблицы успешно созданы!")

        except psycopg2.Error as e:
            print(f"Ошибка при создании таблиц: {e}")

    def setUserName(self, name: str, userId: int):
        self.cur.execute("")

    def setUserGender(self, sex: UserSex, userId: int):
        self

    def setTime(self, timeStart:str, timeEnd:str,useriD:int):
        "11:00"

    def setDescription(self,other:str):
        self

    def getUser(self,telegramId:str):
        self

    def search(self,user:User):
        self

class UserTable:

    def __init__(self):
        self.db = Databases()

    def setUserName(self, name: str, userId: int):
        self.db.setUserName(name, userId)

    def setUserGender(self, sex: UserSex, userId: int):
        self.db.setUserGender(sex, userId)
