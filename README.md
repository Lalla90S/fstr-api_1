## 📋 Реализованные функции

### Спринт 1 ✅
- База данных PostgreSQL с таблицами passes и images
- Класс DatabaseManager для работы с БД  
- REST API на FastAPI с методом POST /submitData
- Поддержка переменных окружения

### Спринт 2 ✅
- GET /submitData/{id} - получение перевала по ID
- PATCH /submitData/{id} - редактирование перевала (только статус new)
- GET /submitData/?user__email={email} - все перевалы пользователя
- Полная валидация данных и обработка ошибок

## 🚀 Быстрый старт

1. Установите зависимости: `pip install -r requirements.txt`
2. Настройте .env файл с параметрами БД
3. Запустите: `uvicorn main:app --reload`
4. Откройте: http://localhost:8000/docs

## 📚 API Endpoints

- `POST /submitData` - добавить перевал
- `GET /submitData/{id}` - получить перевал по ID  
- `PATCH /submitData/{id}` - редактировать перевал (только new)
- `GET /submitData/?user__email={email}` - перевалы пользователя
- `GET /health` - проверка здоровья