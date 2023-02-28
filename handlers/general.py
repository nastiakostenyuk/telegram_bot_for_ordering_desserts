from aiogram import types
from aiogram.utils.markdown import hide_link
from uuid import uuid4

from bot import dp
from models.model_desserts import Dessert
from models.model_category import Category
from models.model_users import User
from keyboards import inline_menu, create_inline_keyboard
from main import get_categories
from function import *



@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(f"Привіт!{emoji.emojize(':waving_hand:')} Це кафе-кондитерська Sweeeet dream!{emoji.emojize(':cupcake:')}\n"
                        f"Очікуємо на твоє замовлення, обирай тістечка та насолоджуйся!{emoji.emojize(':smiling_face_with_hearts:')}",
                        reply_markup = inline_menu)
    users_id_lst = [elem.user_id for elem in session.query(User).all()]
    if message.from_user.id not in users_id_lst:
        new_user = User(user_id=message.from_user.id)
        session.add(new_user)
        session.commit()
        print("add new user")
    unique_id = str(uuid4())
    order = Order(order_id=unique_id, user_id=message.from_user.id,
                  time=datetime.datetime.now().strftime("%H:%M %d/%m/%Y"),
                  state='checkout')
    session.add(order)
    session.commit()


@dp.message_handler(commands=['about'])
async def send_about(message: types.Message):
    await message.reply(f"За допомогою цього телеграм бота, ти можеш зробити замовлення в кондитерській  {emoji.emojize(':butterfly:')}"
                        "Пару кнопочок і можеш насолоджуватись улюбленими тістечками не виходячи з дому!"
                        f"{emoji.emojize(':cupcake:')}{emoji.emojize(':shortcake:')}{emoji.emojize(':doughnut:')}")


@dp.message_handler(lambda message: message.text in get_categories())
async def get_desserts(message: types.Message):
    category_id = session.query(Category).filter(Category.category_name == message.text).first()
    result = session.query(Dessert).filter(Dessert.category_id == category_id.category_id).all()
    for elem in result:
        await message.answer(text=f'{elem}{hide_link(elem.image_url)}',  parse_mode='HTML',
                             reply_markup = create_inline_keyboard(elem.dessert_id))
