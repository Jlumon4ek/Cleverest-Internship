import asyncio
from aiogram import Bot, Dispatcher, types
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
from schemas import UserMessage
from models.models import Truck
app = FastAPI()
bot = Bot(token="6385726296:AAGpeQ1aLGpzJj0SrNtDxZf4_2i-FC8h-z8")


register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.post("/send_message/")
async def send_message(user_message: UserMessage):
    truck = await Truck.filter(id=user_message.truck_id).first()
    await bot.send_message(user_message.user_id, str(truck))
