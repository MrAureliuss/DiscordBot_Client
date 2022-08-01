import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bot_init import bot, load_extensions
from config import settings
from web import routes

origins = [
    "http://localhost:8080"
]

api = FastAPI()  # Подключаем библиотеку для работы с API.
api.include_router(routes.router)  # Подключаем файл с маршрутами.
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.on_event("startup")
async def startup_event():
    load_extensions(bot)
    asyncio.create_task(bot.start(settings['token']))
