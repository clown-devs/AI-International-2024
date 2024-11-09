from config import dp
from aiogram.utils import executor
from handlers import start, general

start.register_handlers_start(dp)
general.register_handlers_general(dp)

async def on_startup(_):
    print("Бот запущен")


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)