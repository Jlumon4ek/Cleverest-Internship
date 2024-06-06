from aiogram import Bot
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from schemas import UserMessage
from models.models import Truck
from config import TOKEN


app = FastAPI()
bot = Bot(token=TOKEN)


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
    try:
        await bot.send_message(user_message.user_id, str(truck))
        return {"status": "Message sent"}
    except Exception as e:
        return {"status": f"Error: {e}"}

@app.get('/')
async def root():
    return {"message": "Hello World"}
