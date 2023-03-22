from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


from main import get_categories

def create_inline_keyboard_dessert(dessert_name):
    inline_btn_order_dessert = InlineKeyboardButton('Замовити десерт', callback_data=f'order_dessert_{dessert_name}')
    inline_kb2 = InlineKeyboardMarkup().add(inline_btn_order_dessert)
    return inline_kb2

def create_inline_keyboard_order(user_id, comment=None):
    btn_confirm = InlineKeyboardButton("Готово", callback_data=f'good_order_{user_id}')
    btn_cancel = InlineKeyboardButton("Скасувати", callback_data=f'not_good_order_{user_id}')
    if comment:
        btn_comment = InlineKeyboardButton("Коментар", callback_data=f'comment_to_order_{user_id}')
        inline_admin_confirm = InlineKeyboardMarkup(row_width=2).add(btn_confirm).insert(btn_cancel).insert(btn_comment)
    else:
        inline_admin_confirm = InlineKeyboardMarkup(row_width=2).add(btn_confirm).insert(btn_cancel)
    return inline_admin_confirm

def create_inline_keyboard_comment_yesno(user_id):
    btn_confirm = InlineKeyboardButton("Так", callback_data=f'yes_comment_{user_id}')
    btn_cancel = InlineKeyboardButton("Ні", callback_data=f'no_comment_{user_id}')
    inline_comment_confirm = InlineKeyboardMarkup(row_width=2).add(btn_confirm).insert(btn_cancel)
    return inline_comment_confirm


def create_inline_keyboard_delivery(user_id, comment=None):
    btn_confirm = InlineKeyboardButton("Доставлене", callback_data=f'delivered_order_{user_id}')
    btn_cancel = InlineKeyboardButton("Не доставлене", callback_data=f'not_delivered_order_{user_id}')
    inline_delivery_confirm = InlineKeyboardMarkup(row_width=2).add(btn_confirm).insert(btn_cancel)
    return inline_delivery_confirm


def create_types_keyboard():
    types_lst = get_categories()
    types_kb = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True,
                                   input_field_placeholder='Types.....')
    for elem in types_lst:
        types_kb.insert(KeyboardButton(elem))

    return types_kb

remove_keyboard = ReplyKeyboardRemove()

inline_btn_order = InlineKeyboardButton('Переглянути меню та зробити замовлення ', callback_data='order')
inline_menu = InlineKeyboardMarkup().add(inline_btn_order)


inline_btn_continue = InlineKeyboardButton("Продовжити замовлення", callback_data='continue_order')
inline_btn_end = InlineKeyboardButton("Оформити замовлення", callback_data='end_order')
inline_choice = InlineKeyboardMarkup(row_width=2).add(inline_btn_continue).insert(inline_btn_end)


inline_btn_confirm = InlineKeyboardButton("Підтвердити замовлення", callback_data='confirm_order')
inline_btn_cancel = InlineKeyboardButton("Скасувати", callback_data='cancel_order')
inline_order_confirmation = InlineKeyboardMarkup(row_width=2).add(inline_btn_confirm).insert(inline_btn_cancel)


number_keyboard  = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
button_phone = KeyboardButton(text="Поділитись номером телефона", request_contact=True )
number_keyboard.add(button_phone)

inline_btn_wrong_quantity = InlineKeyboardButton('Спробувати знову', callback_data=f'wrong_quantity')
inline_kb_wrong = InlineKeyboardMarkup().add(inline_btn_wrong_quantity)



