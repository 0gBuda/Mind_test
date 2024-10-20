from fastapi import FastAPI
from app.auth.routes import router as user_router
from app.messages.routes import router as mess_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Подключаем маршруты для пользователей
app.include_router(user_router, prefix="/users")
app.include_router(mess_router, prefix="/messages")
