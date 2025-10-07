# FSTR API - REST API для Федерации Спортивного Туризма России

Проект реализован в рамках виртуальной стажировки SkillFactory.

## Первый спринт завершен ✅

### Реализовано:
- База данных PostgreSQL с таблицами passes и images
- Класс DatabaseManager для работы с БД
- REST API на FastAPI с методом POST /submitData
- Поддержка переменных окружения

### Запуск проекта:
1. Установите зависимости: `pip install -r requirements.txt`
2. Создайте файл .env с настройками БД
3. Запустите: `uvicorn main:app --reload`

### Документация API:
http://localhost:8000/docs
