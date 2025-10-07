import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def check_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('FSTR_DB_HOST', 'localhost'),
            database='fstr_db',
            user=os.getenv('FSTR_DB_LOGIN', 'postgres'),
            password=os.getenv('FSTR_DB_PASS', '12345')  # замени на свой пароль!
        )
        print("✅ Подключение к базе успешно!")

        cursor = conn.cursor()

        # Проверяем таблицы
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        print("📊 Таблицы в базе:", [table[0] for table in tables])

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")


if __name__ == "__main__":
    check_connection()