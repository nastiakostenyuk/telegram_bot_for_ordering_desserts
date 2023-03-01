import emoji
import datetime

from models.order_dessert import OrderDessert
from models.database import session, db
from main import Order



def get_order_from_user(user_id):
    order = session.query(Order).filter(Order.user_id == user_id, Order.state == 'checkout').first()
    return order


def get_order(user_id, whom):
    order = get_order_from_user(user_id)
    desserts = session.query(OrderDessert).filter(OrderDessert.order_id == order.order_id).all()
    lst_order = []
    total_cost = 0
    if whom == 'client':
        sp = emoji.emojize(':sparkles:')
        money = emoji.emojize(':money_with_wings:')
        cupcake = emoji.emojize(':cupcake:')
        for elem in desserts:
            total_cost += elem.cost
            certain_order = f"{sp}{elem.dessert.dessert_name}{sp}\nКількість{cupcake}: {elem.quantity}\nНа суму{money}: {elem.cost} грн.\n\n"
            lst_order.append(certain_order)
    else:
        lst_order.append(f"Замовник: {order.user.name + ' ' + order.user.second_name}\nНомер телефону: {order.user.telephone_number}\nАдреса: {order.user.address}\n\n")
        for elem in desserts:
            total_cost += elem.cost
            certain_order = f"{elem.dessert.dessert_name}\nКількість: {elem.quantity}\nНа суму: {elem.cost} грн.\n\n"
            lst_order.append(certain_order)
    lst_order.append(f"Загальна сума замовленя: {total_cost}грн.")
    return ''.join(lst_order)


def edit_status(status, user_id):
    order = get_order_from_user(user_id)
    desserts = session.query(OrderDessert).filter(OrderDessert.order_id == order.order_id).all()
    lst_desserts = []
    total_cost = 0
    for dessert in desserts:
        lst_desserts.append(dessert.dessert.dessert_name)
        total_cost += dessert.cost
    edit_order = session.query(Order).filter(Order.order_id == order.order_id). \
        update({Order.state: status,
                Order.desserts: lst_desserts,
                Order.time: datetime.datetime.now().strftime("%H:%M %d/%m/%Y"),
                Order.cost: total_cost}, synchronize_session=False)
    session.commit()