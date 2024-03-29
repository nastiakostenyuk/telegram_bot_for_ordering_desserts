from aiogram.dispatcher.filters.state import StatesGroup, State


class Quantity(StatesGroup):
    quantity_desserts = State()

class OrderStates(StatesGroup):
    pib = State()
    location = State()
    phone = State()

class CommentsAdmin(StatesGroup):
    comment = State()

class CommentsDelivery(StatesGroup):
    comment = State()
