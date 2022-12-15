from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from main import Desserts


inline_btn_order = InlineKeyboardButton('Переглянути меню та зробити замовлення ', callback_data='order')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_order)

inline_btn_continue = InlineKeyboardButton("Продовжити замовлення", callback_data='order_1')
inline_btn_end = InlineKeyboardButton("Оформити замовлення", callback_data='end')
inline_kb3 = InlineKeyboardMarkup(row_width=2).add(inline_btn_continue).insert(inline_btn_end)

remove_keyboard = ReplyKeyboardRemove()
def create_inline_keyboard(dessert_name):
    inline_btn_order_dessert = InlineKeyboardButton('Замовити десерт', callback_data=f'order_dessert_{dessert_name}')
    inline_kb2 = InlineKeyboardMarkup().add(inline_btn_order_dessert)
    return inline_kb2

def create_types_keyboard():
    types_lst = Desserts.get_desserts_types()
    types_kb = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True,
                                   input_field_placeholder='Types.....')
    for elem in types_lst:
        types_kb.insert(KeyboardButton(elem))

    return types_kb

