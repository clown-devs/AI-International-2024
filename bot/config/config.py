import os
from dotenv import load_dotenv
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv()

storage = MemoryStorage()
token = os.getenv("TOKEN")
api = os.getenv("API")
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)