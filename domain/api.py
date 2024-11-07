import psycopg2
from data.user import UserSex



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
            start_time timestamp with time zone,  
            end_time timestamp with time zone,    
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
        self.cur.execute("UPDATE users SET name = ? WHERE id = ?", (name, userId))
        self.connection.commit()

    def setUserGender(self, sex: UserSex, userId: int):
        try:
            self.cur.execute("UPDATE users SET gender = ? WHERE id = ?", (sex.value, userId))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Ошибка при обновлении гендера пользователя: {e}")
            return False

    def setTime(self, timeStart: datetime, timeEnd: datetime, userId: int):
        try:
            if timeStart >= timeEnd:
                raise ValueError("Время окончания должно быть позже времени начала.")

            self.cur.execute("""
                INSERT INTO preferences (user_id, start_time, end_time) 
                VALUES (%s, %s, %s) 
                ON CONFLICT (user_id) DO UPDATE SET start_time = excluded.start_time, end_time = excluded.end_time;
            """, (userId, timeStart, timeEnd))
            self.conn.commit()
            return True

        except ValueError as e:
            print(f"Ошибка ввода времени: {e}")
            return False
        except (Exception, psycopg2.Error) as error:
            print(f"Ошибка при записи времени в базу данных: {error}")
            self.conn.rollback()  # отмена транзакции в случае ошибки
            return False


    # def setDescription(self,other:str):
     #   self

    def getUser(self,telegramId:str):
        try:
            self.cur.execute("SELECT * FROM users WHERE tg_id = ?", (telegramId,))
            user = self.cur.fetchone()  # Получаем первую найденную строку
            return user  # Возвращаем кортеж с данными пользователя или None, если пользователь не найден

        except Exception as e:
            print(f"Ошибка при получении пользователя: {e}")
            return None

    def search(self, user: User):
        try:
            start_time = user.start_time
            end_time = user.end_time

            if start_time is None or end_time is None:
                print("У пользователя не указано предпочитаемое время.")
                return []

            # BETWEEN для поиска пересекающихся интервалов
            self.cur.execute("""
                SELECT u.user_id, u.username
                FROM users u
                JOIN preferences p ON u.user_id = p.user_id
                WHERE p.start_time <= %s AND p.end_time >= %s AND u.user_id != %s;
            """, (end_time, start_time, user.user_id))

            matches = self.cur.fetchall()
            result = [{'user_id': row[0], 'username': row[1]} for row in matches]
            return result

        except (Exception, psycopg2.Error) as error:
            print(f"Ошибка при поиске пользователей: {error}")
            return []





DATABASES = Databases()
