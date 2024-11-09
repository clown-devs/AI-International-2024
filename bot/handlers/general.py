import os
import requests
from aiogram import types, Dispatcher
from config import bot, api
from static import messages


async def api_predict(message: types.message, **kwargs):
    """
        Обращение к api с целью получения ответа на вопрос
    """
    data_json = {"question": f"{message.text}"}
    mesg = await bot.send_message(message.from_user.id, messages.process_mesg)
    
    try:
        resp = requests.post(f"http://{api}/predict", json=data_json)
        answer_json = resp.json()
        await mesg.edit_text(f"{answer_json['answer']}")
    except:
        await mesg.edit_text(messages.went_wrong)

def register_handlers_general(_dp: Dispatcher):
    _dp.register_message_handler(api_predict)