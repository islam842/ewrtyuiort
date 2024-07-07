from config import dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
from kb.kb_client import one_marcup, bs_marcup, menu
import random
#from handlers.functwo import register_handlers_extra  # Импортируем функции из вашего файла handlers
#from handlers.funcone import register_handlers_extra1  # Импортируем функции из вашего файла handlers
#from handlers.functhree import register_handlers_extraa  # Импортируем функции из вашего файла handlers
#from handlers.funcfour import register_handlers_extras
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# logging.basicConfig(level=logging.INFO)
# register_handlers_extra1(dp)
# register_handlers_extraa(dp)
# register_handlers_extras(dp)
from aiogram.utils import executor
from config import bot

class Test(StatesGroup):
    a2 = State()
    BS = State()

async def send_registration_data_to_admins(user_info):
    admin_ids = ['1074399140', '6140506666', '6770137109']  # Замените на ваши Telegram ID
    for admin_id in admin_ids:
        try:
            await bot.send_message(admin_id, user_info)
            logging.info(f"Сообщение успешно отправлено админу {admin_id}")
        except Exception as e:
            logging.error(f"Ошибка отправки сообщения админу {admin_id}: {e}")


@dp.message_handler(commands=['start'])
async def answer_q1(message: types.Message, state: FSMContext):
    await message.answer('Добро пожаловать! На какой турнир хотите зарегистрироваться?', reply_markup=one_marcup)
    await Test.a2.set()

@dp.message_handler(state=Test.a2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer = message.text.strip()
    async with state.proxy() as data:
        data['a2'] = answer
    await state.update_data(a2=answer)

    if answer in ["Brawl Stars", "Pubg mobile", "Free Fire"]:
        await message.answer("Выберите режим турнира:\n[ОДИНОЧНЫЙ] [КОМАНДНЫЙ]\n", reply_markup=bs_marcup)
        await Test.BS.set()
    else:
        await message.answer("Введите турнир, на который хотите зарегистрироваться!")


@dp.message_handler(state=Test.BS)
async def answer_end(message: types.Message, state: FSMContext):
    answer = message.text.strip()
    if answer in ["ОДИНОЧНЫЙ", "КОМАНДНЫЙ"]:
        data = await state.get_data()
        tournament = data.get('a2', 'Unknown')
        username = message.from_user.username
        user_id = message.from_user.id
        if username is None:
            contact_link = f"tg://user?id={user_id}"
            username_display = f"[ссылка](tg://user?id={user_id})"
        else:
            contact_link = f"@{username}"
            username_display = f"@{username}"

        user_info = (f"Новый пользователь зарегистрирован!\n\n"
                     f"Имя пользователя: {username_display}\n"
                     f"ID: {user_id}\n"
                     f"Турнир: {tournament}\n"
                     f"Режим: {answer}")

        logging.info(f"Попытка отправки сообщения администраторам: {user_info}")
        await send_registration_data_to_admins(user_info)
        try:
            # Отправка сообщения пользователю
            await message.answer(
                "Успешная регистрация! С вами сейчас же свяжется менеджер. \n"
                "Для новой регистрации отправьте команду (/start)\n"
                "\n"
                "Пока вступите в подходящую вам группу по ссылке ниже:\n"
                "\n"
                "СООБЩЕСТВО GO-TURNIR - https://t.me/GO_TURNIR_GAMING\n"
                "\n"
                "FREE FIRE:\n"
                "https://t.me/freefiregoturnir\n"
                "PUBG:\n"
                "https://t.me/pubggoturnir\n"
                "BRAWLSTARS:\n"
                "https://t.me/goturnirbrawlstars\n", reply_markup=menu)
        except Exception as e:
            logging.error(f"Ошибка отправки сообщения пользователю: {e}")

        await state.finish()
    else:
        await message.answer("Пожалуйста, выберите режим турнира: [ОДИНОЧНЫЙ] [КОМАНДНЫЙ]")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
