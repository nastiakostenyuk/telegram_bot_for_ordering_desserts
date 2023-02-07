from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hide_link
import emoji
import datetime

from bot import dp, bot
# from main import Desserts
from models.model_desserts import Dessert
from models.model_category import Category
from models.model_users import User
from models.database import session
from states import OrderStates, Quantity
from main import Order
from keyboards import inline_kb1,create_types_keyboard, create_inline_keyboard, inline_kb3, remove_keyboard, number_keyboard, inline_kb4
from main import get_categories

def total_order(user_id):
    sp = emoji.emojize(':sparkles:')
    money = emoji.emojize(':money_with_wings:')
    cupcake = emoji.emojize(':cupcake:')
    orders = session.query(Order).filter(Order.user_id == user_id, Order.state == 'in progress').all()
    order = [f"{sp}{elem.dessert.dessert_name}{sp}\nКількість{cupcake}: {elem.quantity}\nНа суму{money}: {elem.cost} грн.\n\n" for elem in orders]
    return ''.join(order)

@dp.callback_query_handler(lambda c: c.data in ['order', 'continue_order'])
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Вибирайте категорію десерту{emoji.emojize(':shortcake:')}",
                           reply_markup=create_types_keyboard())

@dp.callback_query_handler(lambda c: c.data == 'confirm_order')
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Замовлення прийняте!"
                                                        f"\nДякуємо!{emoji.emojize(':cupcake:')}{emoji.emojize(':growing_heart:')}")
    edit_order = session.query(Order).filter(Order.user_id == callback_query.from_user.id, Order.state == "in progress"). \
        update({Order.state: "finished"}, synchronize_session=False)
    session.commit()

@dp.callback_query_handler(lambda c: c.data == 'cancel_order')
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Замовлення скасовано {emoji.emojize(':man_gesturing_NO:')}")
    edit_order = session.query(Order).filter(Order.user_id == callback_query.from_user.id,
                                             Order.state == "in progress"). \
        update({Order.state: "canceled"}, synchronize_session=False)
    session.commit()

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
    dessert = session.query(Order).filter(Order.user_id == message.from_user.id, Order.quantity == None).first()

    quant = session.query(Order).filter(Order.user_id == message.from_user.id, Order.quantity == None).\
            update({Order.quantity: message.text,
                    Order.cost: int(dessert.dessert.price) * int(message.text)},  synchronize_session = False)
    session.commit()
    print('ok')
    await message.reply(f"Все добре{emoji.emojize(':heart_hands:')}, що далі {emoji.emojize(':white_question_mark:')}",
                        reply_markup=inline_kb3)
    await state.finish()

    # get_users_order = users.orders.filter(state = in progress)

@dp.callback_query_handler(lambda c: c.data == 'end_order')
async def process_callback_end_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_data = session.query(User).filter(User.user_id == callback_query.from_user.id).first()
    if user_data.name is None and user_data.second_name is None:
        await bot.send_message(callback_query.from_user.id, f"Введіть ім'я та фамілію замовника{emoji.emojize(':sunflower:')}")
        await OrderStates.pib.set()
    else:
        await bot.send_message(callback_query.from_user.id,f"Тепер напишіть адресу{emoji.emojize(':house_with_garden:')}, на яку потрібно доставити замовлення {emoji.emojize(':white_question_mark:')}")
        await OrderStates.location.set()


@dp.message_handler(state=OrderStates.pib)
async def location_state(message: types.Message, state: FSMContext):
    update_user = session.query(User).filter(User.user_id == message.from_user.id).\
        update({User.name: message.text.split()[0], User.second_name: message.text.split()[-1]})
    session.commit()
    await message.answer(f"Тепер напишіть адресу{emoji.emojize(':house_with_garden:')}, на яку потрібно доставити замовлення {emoji.emojize(':white_question_mark:')}")
    await OrderStates.location.set()

@dp.message_handler(state=OrderStates.location)
async def phone_state(message: types.Message, state: FSMContext):
    update_user = session.query(User).filter(User.user_id == message.from_user.id). \
        update({User.address: message.text})
    session.commit()
    user_data = session.query(User).filter(User.user_id == message.from_user.id).first()
    if user_data.telephone_number is None:
        await message.answer(f"Тепер поділіться номером телефону {emoji.emojize(':telephone_receiver:')}", reply_markup=number_keyboard)
        await OrderStates.phone.set()
    else:
        await state.finish()
        await message.answer(f'Ваше замовлення: \n{total_order(message.from_user.id)}', reply_markup=inline_kb4)


@dp.message_handler(content_types=types.ContentType.CONTACT, state=OrderStates.phone)
async def result_order(message: types.Message, state: FSMContext ):
    phonenumber= str(message.contact.phone_number)
    update_user = session.query(User).filter(User.user_id == message.from_user.id). \
        update({User.telephone_number: phonenumber})
    session.commit()
    await state.finish()
    await message.answer(f'Ваше замовлення: \n{total_order(message.from_user.id)}', reply_markup=inline_kb4)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(f"Привіт!{emoji.emojize(':waving_hand:')} Це кафе-кондитерська Sweeeet dream!{emoji.emojize(':cupcake:')}\n"
                        f"Очікуємо на твоє замовлення, обирай тістечка та насолоджуйся!{emoji.emojize(':smiling_face_with_hearts:')}",
                        reply_markup = inline_kb1)
    users_id_lst = [elem.user_id for elem in session.query(User).all()]

    if message.from_user.id not in users_id_lst:
        new_user = User(user_id=message.from_user.id)
        session.add(new_user)
        session.commit()
        print("add new user")

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
