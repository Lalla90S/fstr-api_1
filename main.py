from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from database import DatabaseManager

# Создаем FastAPI приложение
app = FastAPI(title="FSTR API", description="API для Федерации Спортивного Туризма России")

# Инициализируем менеджер базы данных
db = DatabaseManager()


# Модели данных для Pydantic (валидация входных данных)
class User(BaseModel):
    email: str
    fam: str
    name: str
    otc: Optional[str] = None
    phone: str


class Coords(BaseModel):
    latitude: str
    longitude: str
    height: str


class Level(BaseModel):
    winter: Optional[str] = ""
    summer: Optional[str] = ""
    autumn: Optional[str] = ""
    spring: Optional[str] = ""


class Image(BaseModel):
    data: str  # Пока как строка, позже можно сделать обработку base64
    title: str


class PassData(BaseModel):
    beauty_title: Optional[str] = ""
    title: str
    other_titles: Optional[str] = ""
    connect: Optional[str] = ""
    add_time: str
    user: User
    coords: Coords
    level: Level
    images: List[Image]


class ResponseModel(BaseModel):
    status: int
    message: Optional[str] = None
    id: Optional[int] = None


@app.post("/submitData", response_model=ResponseModel)
async def submit_data(pass_data: PassData):
    """
    Метод для добавления данных о перевале
    """
    try:
        # Проверяем обязательные поля
        if not pass_data.title:
            return ResponseModel(status=400, message="Отсутствует обязательное поле: title", id=None)

        if not pass_data.user.email or not pass_data.user.fam or not pass_data.user.name or not pass_data.user.phone:
            return ResponseModel(status=400, message="Не все обязательные поля пользователя заполнены", id=None)

        if not pass_data.coords.latitude or not pass_data.coords.longitude or not pass_data.coords.height:
            return ResponseModel(status=400, message="Не все координаты заполнены", id=None)

        # Преобразуем данные в словарь для базы данных
        pass_dict = pass_data.dict()

        # Добавляем данные в базу
        pass_id = db.submit_pass_data(pass_dict)

        if pass_id:
            return ResponseModel(status=200, message=None, id=pass_id)
        else:
            return ResponseModel(status=500, message="Ошибка при сохранении в базу данных", id=None)

    except Exception as e:
        return ResponseModel(status=500, message=f"Внутренняя ошибка сервера: {str(e)}", id=None)


@app.get("/")
async def root():
    """Корневой endpoint для проверки работы API"""
    return {"message": "FSTR API работает!", "status": "OK"}


@app.get("/health")
async def health_check():
    """Проверка здоровья приложения и подключения к БД"""
    try:
        conn = db.get_connection()
        if conn:
            conn.close()
            return {"status": "healthy", "database": "connected"}
        else:
            return {"status": "unhealthy", "database": "disconnected"}
    except:
        return {"status": "unhealthy", "database": "error"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)