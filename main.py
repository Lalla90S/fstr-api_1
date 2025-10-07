from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from database import DatabaseManager

# Создаем FastAPI приложение
app = FastAPI(
    title="FSTR API",
    description="API для Федерации Спортивного Туризма России",
    version="2.0.0"
)

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


class UpdateResponse(BaseModel):
    state: int  # 1 - успех, 0 - ошибка
    message: str


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


@app.get("/submitData/{pass_id}", response_model=Dict[str, Any])
async def get_pass_by_id(pass_id: int):
    """
    Получить информацию о перевале по ID
    """
    try:
        pass_data = db.get_pass_by_id(pass_id)

        if not pass_data:
            raise HTTPException(status_code=404, detail="Перевал не найден")

        # Форматируем ответ согласно оригинальной структуре JSON
        response = {
            "id": pass_data["id"],
            "beauty_title": pass_data["beauty_title"],
            "title": pass_data["title"],
            "other_titles": pass_data["other_titles"],
            "connect": pass_data["connect"],
            "add_time": pass_data["add_time"].strftime("%Y-%m-%d %H:%M:%S"),
            "status": pass_data["status"],
            "user": {
                "email": pass_data["user_email"],
                "fam": pass_data["user_fam"],
                "name": pass_data["user_name"],
                "otc": pass_data["user_otc"],
                "phone": pass_data["user_phone"]
            },
            "coords": {
                "latitude": str(pass_data["coord_latitude"]),
                "longitude": str(pass_data["coord_longitude"]),
                "height": str(pass_data["coord_height"])
            },
            "level": {
                "winter": pass_data["level_winter"],
                "summer": pass_data["level_summer"],
                "autumn": pass_data["level_autumn"],
                "spring": pass_data["level_spring"]
            },
            "images": pass_data["images"] or []
        }

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


@app.patch("/submitData/{pass_id}", response_model=UpdateResponse)
async def update_pass_data(pass_id: int, update_data: PassData):
    """
    Обновить данные перевала (только если статус 'new')
    """
    try:
        # Преобразуем данные для обновления
        update_dict = update_data.dict()

        # Удаляем пользовательские данные (нельзя редактировать)
        if 'user' in update_dict:
            del update_dict['user']

        # Преобразуем координаты для базы данных
        if 'coords' in update_dict:
            update_dict['coord_latitude'] = float(update_dict['coords']['latitude'])
            update_dict['coord_longitude'] = float(update_dict['coords']['longitude'])
            update_dict['coord_height'] = int(update_dict['coords']['height'])
            del update_dict['coords']

        # Преобразуем уровни сложности
        if 'level' in update_dict:
            update_dict['level_winter'] = update_dict['level'].get('winter')
            update_dict['level_summer'] = update_dict['level'].get('summer')
            update_dict['level_autumn'] = update_dict['level'].get('autumn')
            update_dict['level_spring'] = update_dict['level'].get('spring')
            del update_dict['level']

        # Обновляем данные в базе
        success, message = db.update_pass_data(pass_id, update_dict)

        return UpdateResponse(
            state=1 if success else 0,
            message=message
        )

    except Exception as e:
        return UpdateResponse(
            state=0,
            message=f"Ошибка при обновлении: {str(e)}"
        )


@app.get("/submitData/", response_model=List[Dict[str, Any]])
async def get_passes_by_user_email(user_email: str = Query(..., alias="user__email")):
    """
    Получить все перевалы, отправленные пользователем с указанным email
    """
    try:
        passes = db.get_passes_by_email(user_email)

        response = []
        for pass_data in passes:
            response.append({
                "id": pass_data["id"],
                "beauty_title": pass_data["beauty_title"],
                "title": pass_data["title"],
                "other_titles": pass_data["other_titles"],
                "connect": pass_data["connect"],
                "add_time": pass_data["add_time"].strftime("%Y-%m-%d %H:%M:%S"),
                "status": pass_data["status"],
                "user": {
                    "email": user_email
                },
                "coords": {
                    "latitude": str(pass_data["coord_latitude"]),
                    "longitude": str(pass_data["coord_longitude"]),
                    "height": str(pass_data["coord_height"])
                },
                "level": {
                    "winter": pass_data["level_winter"],
                    "summer": pass_data["level_summer"],
                    "autumn": pass_data["level_autumn"],
                    "spring": pass_data["level_spring"]
                }
            })

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


@app.get("/")
async def root():
    """Корневой endpoint для проверки работы API"""
    return {
        "message": "FSTR API работает!",
        "status": "OK",
        "version": "2.0.0",
        "endpoints": {
            "POST /submitData": "Добавить данные о перевале",
            "GET /submitData/{id}": "Получить перевал по ID",
            "PATCH /submitData/{id}": "Обновить перевал (только статус new)",
            "GET /submitData/?user__email={email}": "Получить все перевалы пользователя"
        }
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья приложения и подключения к БД"""
    try:
        conn = db.get_connection()
        if conn:
            conn.close()
            return {"status": "healthy", "database": "connected", "api": "running"}
        else:
            return {"status": "unhealthy", "database": "disconnected", "api": "running"}
    except:
        return {"status": "unhealthy", "database": "error", "api": "running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)