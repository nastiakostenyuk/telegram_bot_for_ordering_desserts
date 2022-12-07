from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from main import Desserts


inline_btn_order = InlineKeyboardButton('Переглянути меню та зробити замовлення ', callback_data='order')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_order)

def create_types_keyboard():
    types_lst = Desserts.get_desserts_types()
    types_kb = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True,
                                   input_field_placeholder='Виберіть тип десертику')
    for elem in types_lst:
        types_kb.insert(KeyboardButton(elem))

    return types_kb

