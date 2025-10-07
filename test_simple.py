import requests
import json


def test_api():
    base_url = "http://localhost:8000"

    print("=== ТЕСТИРУЕМ API ===\n")

    # 1. Проверяем что API работает
    try:
        response = requests.get(f"{base_url}/")
        print("✅ API работает:", response.json())
    except:
        print("❌ API не запущен")
        return

    # 2. Проверяем здоровье
    try:
        response = requests.get(f"{base_url}/health")
        print("✅ Health check:", response.json())
    except Exception as e:
        print("❌ Health check failed:", e)

    # 3. Пробуем получить перевал по ID 1
    try:
        response = requests.get(f"{base_url}/submitData/1")
        if response.status_code == 200:
            print("✅ GET по ID 1: Успех!")
            data = response.json()
            print(f"   Название: {data['title']}")
            print(f"   Статус: {data['status']}")
        elif response.status_code == 404:
            print("⚠️  GET по ID 1: Перевал не найден (но API работает!)")
        else:
            print(f"❌ GET по ID 1: Ошибка {response.status_code}")
    except Exception as e:
        print("❌ GET по ID 1: Ошибка подключения")

    # 4. Пробуем получить перевалы по email
    try:
        response = requests.get(f"{base_url}/submitData/?user__email=test@mail.ru")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ GET по email: Найдено {len(data)} перевалов")
        else:
            print(f"❌ GET по email: Ошибка {response.status_code}")
    except Exception as e:
        print("❌ GET по email: Ошибка подключения")


if __name__ == "__main__":
    test_api()