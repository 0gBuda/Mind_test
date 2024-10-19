from fastapi import FastAPI
from app.auth.routes import router as user_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Подключаем маршруты для пользователей
app.include_router(user_router, prefix="/users")
