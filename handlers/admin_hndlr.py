from aiogram import types
from aiogram.dispatcher import FSMContext


from bot import dp, bot
from states import CommentsAdmin
from models.model_comments import Comment
from .function import *
from keyboards import create_inline_keyboard_order, create_inline_keyboard_delivery

@dp.callback_query_handler(lambda c: 'not_good_order' in c.data)
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = int(callback_query.data.split('_')[-1])
    edit_status("admin_canceled", user_id , 'admin')
    await bot.send_message(callback_query.from_user.id,"Замовлення скасовано")

@dp.callback_query_handler(lambda c: 'good_order' in c.data)
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = int(callback_query.data.split('_')[-1])
    edit_status("confirm", user_id, 'admin')
    await bot.send_message(callback_query.from_user.id, "Замовлення підтверджене")
    await bot.send_message(chat_id=893972667,
                           text=f'Замовлення: \n\n{get_order(user_id, "delivery")}',
                           reply_markup=create_inline_keyboard_delivery(user_id))


@dp.callback_query_handler(lambda c: 'comment_to_order' in c.data)
async def process_callback_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Чекаю на коментар")
    user_id = int(callback_query.data.split('_')[-1])
    comment = Comment(order_id=get_state_order(user_id, 'not confirmed').order_id,
                      author=f'admin_{callback_query.from_user.id}')
    session.add(comment)
    session.commit()
    await CommentsAdmin.comment.set()


@dp.message_handler(state=CommentsAdmin.comment)
async def quantity_des(message: types.Message, state: FSMContext):
    add_comment = session.query(Comment).filter(Comment.author == f'admin_{message.from_user.id}',
                                                Comment.comment == None). \
        update({Comment.comment: message.text,
                Comment.date_time: datetime.datetime.now().strftime("%H:%M %d/%m/%Y")})

    session.commit()
    comment = session.query(Comment).filter(Comment.author == f'admin_{message.from_user.id}').first()
    await state.finish()
    await message.answer('Коментар записано, виберіть статус замовлення', reply_markup=create_inline_keyboard_order(get_user_id_from_order_id(comment.order_id)))
