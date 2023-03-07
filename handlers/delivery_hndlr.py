from aiogram import types
from aiogram.dispatcher import FSMContext


from bot import dp, bot
from states import CommentsDelivery
from models.model_comments import Comment
from .function import *
from keyboards import create_inline_keyboard_order, create_inline_keyboard_comment_yesno

@dp.callback_query_handler(lambda c: 'not_delivered_order' in c.data)
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = int(callback_query.data.split('_')[-1])
    edit_status("delivery_canceled", user_id, 'delivery')
    await bot.send_message(callback_query.from_user.id,"Замовлення скасовано, написати причину", reply_markup=create_inline_keyboard_comment_yesno(user_id))


@dp.callback_query_handler(lambda c: 'delivered_order' in c.data)
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = int(callback_query.data.split('_')[-1])
    edit_status("delivered", user_id, 'delivery')
    await bot.send_message(callback_query.from_user.id, "Замовлення доставлене")


@dp.callback_query_handler(lambda c: 'no_comment' in c.data)
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Статус замовлення змінено")


@dp.callback_query_handler(lambda c: 'yes_comment' in c.data)
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Очікую на коментар")
    user_id = int(callback_query.data.split('_')[-1])
    comment = Comment(order_id=get_state_order(user_id, 'delivery_canceled').order_id,
                      author=f'delivery_{callback_query.from_user.id}')
    session.add(comment)
    session.commit()
    await CommentsDelivery.comment.set()


@dp.message_handler(state=CommentsDelivery.comment)
async def quantity_des(message: types.Message, state: FSMContext):
    add_comment = session.query(Comment).filter(Comment.author == f'delivery_{message.from_user.id}', Comment.comment == None).\
        update({Comment.comment: message.text,
                Comment.date_time: datetime.datetime.now().strftime("%H:%M %d/%m/%Y")})
    session.commit()
    await state.finish()
    await message.answer('Коментар записано')
