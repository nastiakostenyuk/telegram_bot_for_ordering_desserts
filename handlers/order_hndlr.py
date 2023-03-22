from uuid import uuid4

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import dp, bot
from db_utils.models import User
from states import OrderStates, Quantity
from keyboards import create_types_keyboard, inline_choice, number_keyboard, inline_order_confirmation, \
    create_inline_keyboard_order, inline_kb_wrong
from .function import *



@dp.callback_query_handler(lambda c: c.data in ['order', 'continue_order'])
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Вибирайте категорію десерту{emoji.emojize(':shortcake:')}",
                           reply_markup=create_types_keyboard())



@dp.callback_query_handler(lambda c:  'order_dessert' in c.data)
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Напишіть кількість десерту(наприклад: 1, 2...)',
                           reply_markup=types.ReplyKeyboardRemove())
    dessert_id = int(callback_query.data.split('_')[-1])
    order = get_state_order(callback_query.from_user.id, 'checkout')
    if order is None:
        unique_id = str(uuid4())
        order = Order(order_id=unique_id, user_id=callback_query.from_user.id,
                      date_time=datetime.datetime.now(),
                      state='checkout')
        session.add(order)
        session.commit()

    order_dessert = OrderDessert(order_id=order.order_id, dessert_id=dessert_id)
    session.add(order_dessert)
    session.commit()
    print("add dessert")
    await Quantity.quantity_desserts.set()


@dp.callback_query_handler(lambda c: c.data == 'wrong_quantity')
async def process_callback_wrong_quantity(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Напишіть нову кількість десерту(наприклад: 1, 2...)',
                           reply_markup=types.ReplyKeyboardRemove())
    await Quantity.quantity_desserts.set()



@dp.message_handler(state=Quantity.quantity_desserts)
async def quantity_des(message: types.Message, state: FSMContext):
    try:
        int(message.text)
    except ValueError:
        await message.reply(f"Щось пішло не так, не розумію цю кількість - {message.text}", reply_markup=inline_kb_wrong)
        await state.finish()
    else:
        order = get_state_order(message.from_user.id, 'checkout')
        dessert = session.query(OrderDessert).filter(OrderDessert.order_id==order.order_id, OrderDessert.quantity == None).first()
        end_order_dessert = session.query(OrderDessert).filter(OrderDessert.order_id==order.order_id, OrderDessert.quantity == None).\
        update({OrderDessert.quantity: message.text,
                OrderDessert.cost : int(dessert.dessert.price) * int(message.text)}, synchronize_session = False)
        session.commit()

        await message.reply(f"Все добре{emoji.emojize(':heart_hands:')}, що далі {emoji.emojize(':white_question_mark:')}",
                            reply_markup=inline_choice)
        await state.finish()


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
        await message.answer(f"Тепер поділіться номером телефону {emoji.emojize(':telephone_receiver:')}\n"
                             f"(натисніть кнопочку {emoji.emojize(':right_arrow_curving_down:')})", reply_markup=number_keyboard)
        await OrderStates.phone.set()
    else:
        await state.finish()
        await message.answer(f'Ваше замовлення: \n{get_order(message.from_user.id, "client")}',
                             reply_markup=inline_order_confirmation)


@dp.message_handler(content_types=types.ContentType.CONTACT, state=OrderStates.phone)
async def result_order(message: types.Message, state: FSMContext ):
    phonenumber= str(message.contact.phone_number)
    update_user = session.query(User).filter(User.user_id == message.from_user.id). \
        update({User.telephone_number: phonenumber})
    session.commit()
    await state.finish()
    await message.answer(f'Ваше замовлення: \n{get_order(message.from_user.id, "client")}',
                         reply_markup=inline_order_confirmation)


@dp.callback_query_handler(lambda c: c.data == 'confirm_order')
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Замовлення прийняте!"
                                                        f"\nДякуємо!{emoji.emojize(':cupcake:')}{emoji.emojize(':growing_heart:')}\n"
                                                        f"Очікуйте, на підтвердження!")
    await bot.send_message(chat_id=893972667, text=f'Замовлення: \n\n{get_order(callback_query.from_user.id, "admin")}',
                           reply_markup=create_inline_keyboard_order(get_state_order(callback_query.from_user.id, 'checkout').user_id, 'comment'))
    edit_status('not confirmed', callback_query.from_user.id, 'user')


@dp.callback_query_handler(lambda c: c.data == 'cancel_order')
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Замовлення скасовано {emoji.emojize(':man_gesturing_NO:')}")
    edit_status('user_canceled', callback_query.from_user.id, 'user')
