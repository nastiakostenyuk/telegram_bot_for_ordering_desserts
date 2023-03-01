from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import dp, bot
from states import Comments
from .function import *

@dp.callback_query_handler(lambda c: c.data == 'not_good_order')
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    edit_status("admin_canceled", callback_query.from_user.id, 'admin')
    await bot.send_message(callback_query.from_user.id, f"Замовлення скасовано")

@dp.callback_query_handler(lambda c: c.data == 'good_order')
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    edit_status("confirm", callback_query.from_user.id, 'admin')
    await bot.send_message(callback_query.from_user.id, f"Замовлення підтверджене")

@dp.callback_query_handler(lambda c: c.data == 'comment_to_order')
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, f"Чекаю на коментар")


@dp.message_handler(state=Comments.comment)
async def quantity_des(message: types.Message, state: FSMContext):
    pass