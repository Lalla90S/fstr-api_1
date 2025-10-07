import psycopg2


def create_tables():
    try:
        # Подключаемся к базе
        conn = psycopg2.connect(
            host="localhost",
            database="fstr_db",
            user="postgres",
            password="12345"  # замени на свой пароль!
        )
        cursor = conn.cursor()

        print("✅ Подключение к базе успешно!")

        # Создаем таблицу passes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS passes (
                id SERIAL PRIMARY KEY,
                beauty_title VARCHAR(255),
                title VARCHAR(255) NOT NULL,
                other_titles VARCHAR(255),
                connect TEXT,
                add_time TIMESTAMP NOT NULL,
                status VARCHAR(20) DEFAULT 'new',
                user_email VARCHAR(255) NOT NULL,
                user_fam VARCHAR(100) NOT NULL,
                user_name VARCHAR(100) NOT NULL,
                user_otc VARCHAR(100),
                user_phone VARCHAR(50) NOT NULL,
                coord_latitude DECIMAL(10, 6) NOT NULL,
                coord_longitude DECIMAL(10, 6) NOT NULL,
                coord_height INTEGER NOT NULL,
                level_winter VARCHAR(10),
                level_summer VARCHAR(10),
                level_autumn VARCHAR(10),
                level_spring VARCHAR(10)
            )
        """)
        print("✅ Таблица 'passes' создана!")

        # Создаем таблицу images
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS images (
                id SERIAL PRIMARY KEY,
                pass_id INTEGER REFERENCES passes(id),
                image_data BYTEA,
                title VARCHAR(255) NOT NULL
            )
        """)
        print("✅ Таблица 'images' создана!")

        conn.commit()
        cursor.close()
        conn.close()

        print("🎉 ВСЕ ТАБЛИЦЫ СОЗДАНЫ УСПЕШНО!")

    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    create_tables()