import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime


class DatabaseManager:
    def __init__(self):
        # Получаем данные из переменных окружения (дополнительные баллы!)
        self.db_host = os.getenv('FSTR_DB_HOST', 'localhost')
        self.db_port = os.getenv('FSTR_DB_PORT', '5432')
        self.db_login = os.getenv('FSTR_DB_LOGIN', 'postgres')
        self.db_password = os.getenv('FSTR_DB_PASS', '12345')  # замени на свой пароль
        self.db_name = 'fstr_db'

    def get_connection(self):
        """Создает подключение к базе данных"""
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                database=self.db_name,
                user=self.db_login,
                password=self.db_password,
                cursor_factory=RealDictCursor
            )
            return conn
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
            return None

    def submit_pass_data(self, pass_data):
        """
        Добавляет данные о перевале в базу данных
        Возвращает ID новой записи или None при ошибке
        """
        conn = self.get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()

            # Вставляем данные в таблицу passes
            cursor.execute("""
                INSERT INTO passes (
                    beauty_title, title, other_titles, connect, add_time,
                    user_email, user_fam, user_name, user_otc, user_phone,
                    coord_latitude, coord_longitude, coord_height,
                    level_winter, level_summer, level_autumn, level_spring
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                pass_data.get('beauty_title'),
                pass_data.get('title'),
                pass_data.get('other_titles'),
                pass_data.get('connect'),
                pass_data.get('add_time'),
                pass_data['user']['email'],
                pass_data['user']['fam'],
                pass_data['user']['name'],
                pass_data['user'].get('otc'),
                pass_data['user']['phone'],
                float(pass_data['coords']['latitude']),
                float(pass_data['coords']['longitude']),
                int(pass_data['coords']['height']),
                pass_data['level'].get('winter'),
                pass_data['level'].get('summer'),
                pass_data['level'].get('autumn'),
                pass_data['level'].get('spring')
            ))

            # Получаем ID новой записи
            pass_id = cursor.fetchone()['id']

            # Добавляем изображения если они есть
            if 'images' in pass_data:
                for image in pass_data['images']:
                    cursor.execute("""
                        INSERT INTO images (pass_id, image_data, title)
                        VALUES (%s, %s, %s)
                    """, (
                        pass_id,
                        image.get('data'),  # Пока сохраняем как есть, позже обработаем
                        image.get('title')
                    ))

            conn.commit()
            return pass_id

        except Exception as e:
            conn.rollback()
            print(f"Ошибка при добавлении данных: {e}")
            return None
        finally:
            cursor.close()
            conn.close()


# Тестовые данные для проверки
if __name__ == "__main__":
    db = DatabaseManager()

    # Тестовые данные как в задании
    test_data = {
        "beauty_title": "пер.",
        "title": "Пхия",
        "other_titles": "Триев",
        "connect": "",
        "add_time": "2021-09-22 13:18:13",
        "user": {
            "email": "qwerty@mail.ru",
            "fam": "Пупкин",
            "name": "Василий",
            "otc": "Иванович",
            "phone": "+7 555 55 55"
        },
        "coords": {
            "latitude": "45.3842",
            "longitude": "7.1525",
            "height": "1200"
        },
        "level": {
            "winter": "",
            "summer": "1А",
            "autumn": "1А",
            "spring": ""
        },
        "images": [
            {"data": "test_image_1", "title": "Седловина"},
            {"data": "test_image_2", "title": "Подъём"}
        ]
    }

    # Тестируем добавление данных
    result_id = db.submit_pass_data(test_data)
    if result_id:
        print(f"✅ Данные успешно добавлены! ID: {result_id}")
    else:
        print("❌ Ошибка при добавлении данных")