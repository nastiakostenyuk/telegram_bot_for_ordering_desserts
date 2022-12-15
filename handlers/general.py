from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hide_link

from bot import dp, bot
from main import Desserts
from models.model_desserts import DessertData
from models.model_orders import OrderData
from models.database import session
from states import OrderStates, Quantity
from main import Order
from keyboards import inline_kb1,create_types_keyboard, create_inline_keyboard, inline_kb3, remove_keyboard


@dp.callback_query_handler(lambda c: c.data in ['order', 'order_1'])
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Вибирайте категорію десерту',
                           reply_markup=create_types_keyboard())

new_order = {}
@dp.callback_query_handler(lambda c:  'order_dessert' in c.data)
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Напишіть кількість десерту(наприклад: 1, 2...)',
                           reply_markup=types.ReplyKeyboardRemove())
    dessert = session.query(DessertData.dessert_name).filter(DessertData.dessert_id == callback_query.data.split('_')[-1]).limit(1).scalar()
    if callback_query.from_user.id in new_order.keys():
        if dessert not in new_order[callback_query.from_user.id]:
            new_order[callback_query.from_user.id][dessert] = None
    else:
        new_order[callback_query.from_user.id] = {dessert: None}

    await Quantity.quantity_desserts.set()
    print(new_order)

@dp.message_handler(state=Quantity.quantity_desserts)
async def quantity_des(message: types.Message, state: FSMContext):
    if  message.text.isdigit() and 0 < int(message.text) <= 50:
        async with state.proxy() as data:
            data[f'quantity{message.message_id}'] = message.text
        for key, elem in new_order[message.from_user.id].items():
            if elem is None:
                new_order[message.from_user.id][key] = message.text
        await message.reply('Все добре, що далі', reply_markup=inline_kb3)
    else:
        await message.answer('Неправильно введена кількість, спробуйте знову')
    await state.finish()
    print(new_order)

@dp.callback_query_handler(lambda c: c.data == 'order')
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Вибирайте категорію десерту',
                           reply_markup=create_types_keyboard())

@dp.callback_query_handler(lambda c: c.data == 'end')
async def process_callback_end_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введіть ПІБ замовника')
    await OrderStates.pib.set()


@dp.message_handler(state=OrderStates.pib)
async def location_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pib'] = message.text
    await message.answer('Тепер напишіть адресу, на яку потрібно доставити замовлення')
    await OrderStates.location.set()


@dp.message_handler(state=OrderStates.location)
async def phone_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['location'] = message.text
    await message.answer('Тепер поділіться номеорм телефону')
    await OrderStates.phone.set()

@dp.message_handler(state=OrderStates.phone)
async def result_order(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
        print(data)
    await state.finish()
    await message.answer('Замовлення прийняте')


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):

    await message.reply("Привіт! Це кафе-кондитерська Sweeeet dream!\n"
                        "Очікуємо на твоє замовлення, обирай тістечка та насолоджуйся!",
                        reply_markup = inline_kb1)


@dp.message_handler(commands=['about'])
async def send_about(message: types.Message):
    await message.reply("За допомогою цього телеграм бота, ти можеш зробити замовлення в кондитерській "
                        "Пару кнопочок і можеш насолоджуватись улюбленими тістечками не виходячи з дому!")


@dp.message_handler(lambda message: message.text in Desserts.get_desserts_types())
async def get_desserts(message: types.Message):
    result = session.query(DessertData).filter(DessertData.dessert_type ==  message.text).all()
    for elem in result:
        await message.answer(text=f'{elem}{hide_link(elem.image_url)}',  parse_mode='HTML',
                             reply_markup = create_inline_keyboard(elem.dessert_id))
