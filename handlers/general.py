from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hide_link
from time import sleep
import datetime

from bot import dp, bot
# from main import Desserts
from models.model_desserts import Dessert
from models.model_category import Category
from models.model_users import User
from models.database import session
from states import OrderStates, Quantity
from main import Order
from keyboards import inline_kb1,create_types_keyboard, create_inline_keyboard, inline_kb3, remove_keyboard, number_keyboard
from main import get_categories

@dp.callback_query_handler(lambda c: c.data in ['order', 'continue_order'])
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Вибирайте категорію десерту',
                           reply_markup=create_types_keyboard())

@dp.callback_query_handler(lambda c:  'order_dessert' in c.data)
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Напишіть кількість десерту(наприклад: 1, 2...)',
                           reply_markup=types.ReplyKeyboardRemove())
    dessert_id = int(callback_query.data.split('_')[-1])
    order = Order(user_id=callback_query.from_user.id, dessert_id=dessert_id, state='in progress',
                  time=datetime.datetime.now().strftime("%H:%M %d/%m/%Y"))
    session.add(order)
    session.commit()
    await Quantity.quantity_desserts.set()

@dp.message_handler(state=Quantity.quantity_desserts)
async def quantity_des(message: types.Message, state: FSMContext):
    # async with state.proxy() as data:
    #     data[f'quantity'] = int(message.text)
    quant = session.query(Order).filter(Order.user_id == message.from_user.id, Order.quantity == None).\
            update({Order.quantity: message.text},  synchronize_session = False)
    session.commit()
    print('ok')
    await message.reply('Все добре, що далі', reply_markup=inline_kb3)
    await state.finish()

    # get_users_order = users.orders.filter(state = in progress)

@dp.callback_query_handler(lambda c: c.data == 'end_order')
async def process_callback_end_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_data = session.query(User).filter(User.user_id == callback_query.from_user.id).first()
    if user_data.name is None and user_data.second_name is None:
        await bot.send_message(callback_query.from_user.id, "Введіть ім'я та фамілію замовника")
        await OrderStates.pib.set()
    else:
        await bot.send_message(callback_query.from_user.id, 'Тепер напишіть адресу, на яку потрібно доставити замовлення')
        await OrderStates.location.set()


@dp.message_handler(state=OrderStates.pib)
async def location_state(message: types.Message, state: FSMContext):
    update_user = session.query(User).filter(User.user_id == message.from_user.id).\
        update({User.name: message.text.split()[0], User.second_name: message.text.split()[-1]})
    session.commit()
    await message.answer('Тепер напишіть адресу, на яку потрібно доставити замовлення')
    await OrderStates.location.set()

@dp.message_handler(state=OrderStates.location)
async def phone_state(message: types.Message, state: FSMContext):
    update_user = session.query(User).filter(User.user_id == message.from_user.id). \
        update({User.address: message.text})
    session.commit()
    user_data = session.query(User).filter(User.user_id == message.from_user.id).first()
    if user_data.telephone_number is None:
        await message.answer('Тепер поділіться номером телефону', reply_markup=number_keyboard)
        await OrderStates.phone.set()
    else:
        await state.finish()
        await message.answer(f'Ваше замовлення: \n ')


@dp.message_handler(content_types=types.ContentType.CONTACT, state=OrderStates.phone)
async def result_order(message: types.Message, state: FSMContext ):
    phonenumber= str(message.contact.phone_number)
    update_user = session.query(User).filter(User.user_id == message.from_user.id). \
        update({User.telephone_number: phonenumber})
    session.commit()
    await state.finish()
    await message.answer('Замовлення прийняте')


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привіт! Це кафе-кондитерська Sweeeet dream!\n"
                        "Очікуємо на твоє замовлення, обирай тістечка та насолоджуйся!",
                        reply_markup = inline_kb1)
    users_id_lst = [elem.user_id for elem in session.query(User).all()]

    if message.from_user.id not in users_id_lst:
        new_user = User(user_id=message.from_user.id)
        session.add(new_user)
        session.commit()
        print("add new user")

@dp.message_handler(commands=['about'])
async def send_about(message: types.Message):
    await message.reply("За допомогою цього телеграм бота, ти можеш зробити замовлення в кондитерській "
                        "Пару кнопочок і можеш насолоджуватись улюбленими тістечками не виходячи з дому!")


@dp.message_handler(lambda message: message.text in get_categories())
async def get_desserts(message: types.Message):
    category_id = session.query(Category).filter(Category.category_name == message.text).first()
    result = session.query(Dessert).filter(Dessert.category_id == category_id.category_id).all()
    for elem in result:
        await message.answer(text=f'{elem}{hide_link(elem.image_url)}',  parse_mode='HTML',
                             reply_markup = create_inline_keyboard(elem.dessert_id))
