from aiogram import Bot
from fastapi import FastAPI, Request, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from schemas import UserMessage
from models.models import Truck
from config import TOKEN
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from fastapi.responses import JSONResponse


app = FastAPI()
bot = Bot(token=TOKEN)

# Инициализация Limiter с использованием get_remote_address
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Кастомный обработчик исключений для RateLimitExceeded
@app.exception_handler(RateLimitExceeded)
async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests, please try again later."}
    )

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    return response

@app.post("/send_message/")
async def send_message(user_message: UserMessage):
    truck = await Truck.filter(id=user_message.truck_id).first()
    try:
        await bot.send_message(user_message.user_id, str(truck))
        return {"status": "Message sent"}
    except Exception as e:
        return {"status": f"Error: {e}"}

@app.get('/')
async def root():
    return {"message": "Hello World"}

# Пример ограниченного маршрута
@app.get("/limited")
@limiter.limit("5/minute")
async def limited_endpoint(request: Request):
    return {"message": "Этот маршрут ограничен до 5 запросов в минуту", }