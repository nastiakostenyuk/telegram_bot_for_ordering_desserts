from bot import dp, bot
from aiogram import types
from aiogram.dispatcher.filters import Text
from main import Desserts
from models.model_desserts import DessertData
from models.model_orders import OrderData
from models.database import session


from keyboards import inline_kb1,create_types_keyboard


@dp.callback_query_handler(lambda c: c.data == 'order')
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Вибирайте категорію десерту',
                           reply_markup=create_types_keyboard())


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):

    await message.reply("Привіт! Це кафе-кондитерська Sweeeet deream!\n"
                        "Очікуємо на твоє замовлення, обирай тістечка та насолоджуйся!",
                        reply_markup = inline_kb1)


@dp.message_handler(commands=['about'])
async def send_about(message: types.Message):
    await message.reply("За допомогою цього телеграм бота, ти можеш зробити замовлення в кондитерській "
                        "Пару кнопочок і можеш насолоджуватись улюбленими тістечками не виходячи з дому!")


@dp.message_handler(commands=['photo'])
async def send_about(message: types.Message):
    await dp.send_photo("https://rutxt.ru/files/16665/original/602389a6e8.jpg")


@dp.message_handler(lambda message: message.text in Desserts.get_desserts_types())
async def without_puree(message: types.Message):
    result = session.query(DessertData).filter(DessertData.dessert_type == "торт").all()
    await message.answer(*result)