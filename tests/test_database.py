import pytest
from database import DatabaseManager


class TestDatabaseManager:

    def test_connection(self):
        """Тест подключения к базе данных"""
        db = DatabaseManager()
        conn = db.get_connection()
        assert conn is not None
        conn.close()

    def test_submit_pass_data(self):
        """Тест добавления данных о перевале"""
        db = DatabaseManager()

        test_data = {
            "beauty_title": "пер.",
            "title": "Тестовый перевал",
            "other_titles": "Тест",
            "connect": "",
            "add_time": "2024-01-20 10:00:00",
            "user": {
                "email": "test@example.com",
                "fam": "Тестов",
                "name": "Тест",
                "otc": "Тестович",
                "phone": "+79990001122"
            },
            "coords": {
                "latitude": "45.1234",
                "longitude": "7.5678",
                "height": "1500"
            },
            "level": {
                "winter": "",
                "summer": "1А",
                "autumn": "1А",
                "spring": ""
            },
            "images": []
        }

        pass_id = db.submit_pass_data(test_data)
        assert pass_id is not None
        assert isinstance(pass_id, int)

    def test_get_pass_by_id(self):
        """Тест получения перевала по ID"""
        db = DatabaseManager()

        # Сначала создаем перевал
        test_data = {
            "title": "Перевал для теста GET",
            "add_time": "2024-01-20 11:00:00",
            "user": {
                "email": "get_test@example.com",
                "fam": "Геттестов",
                "name": "Геттест",
                "otc": "Геттестович",
                "phone": "+79991112233"
            },
            "coords": {
                "latitude": "45.5555",
                "longitude": "7.8888",
                "height": "1800"
            },
            "level": {
                "winter": "",
                "summer": "1А",
                "autumn": "1А",
                "spring": ""
            },
            "images": []
        }

        pass_id = db.submit_pass_data(test_data)

        # Затем получаем его
        pass_data = db.get_pass_by_id(pass_id)

        assert pass_data is not None
        assert pass_data['id'] == pass_id
        assert pass_data['title'] == test_data['title']

    def test_get_passes_by_email(self):
        """Тест получения перевалов по email"""
        db = DatabaseManager()
        email = "filter@example.com"

        passes = db.get_passes_by_email(email)
        assert isinstance(passes, list)