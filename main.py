# from sqlalchemy import func
#
import datetime

from sqlalchemy.exc import SQLAlchemyError

from models.model_desserts import Dessert
from models.model_orders import Order
from models.model_category import Category
from models.model_users import User
from models.database import session
from models.database import create_db as db_creator
#

def get_categories():
    categories_lst = [elem.category_name for elem in session.query(Category).all()]
    return categories_lst
# class Desserts:
#     __list_of_desserts = []
#
#     def __new__(cls, *args, **kwargs):
#         return None
#
#     @classmethod
#     def add_dessert(cls, dessert):
#         Desserts.__list_of_desserts.append(dessert)
#
#     @classmethod
#     def search_dessert(cls, param, value):
#         try:
#             for elem in Desserts.__list_of_desserts:
#                 if elem.__dict__[param] == value:
#                     return f"Результат пошуку: {elem}"
#             return "Десерту з таким параметром не знайшлось"
#         except ValueError:
#             print("Такого параметру немає")
#
#     @classmethod
#     def remove_dessert(cls, del_name):
#         delete_elem = None
#         for index, elem in enumerate(Desserts.__list_of_desserts):
#             if elem.dessert_name == del_name:
#                 delete_elem = Desserts.__list_of_desserts.pop(index)
#                 session.query(DessertData).filter(DessertData.dessert_name == del_name).delete()
#                 session.commit()
#         return f"Ви видалили елемент: {delete_elem}"
#
#     @classmethod
#     def get_desserts_types(cls):
#         types = []
#         for type in session.query(DessertData.dessert_type).distinct():
#             types.append(type.dessert_type)
#         return types
#
#     @classmethod
#     def return_lst_with_desserts(cls):
#         return Desserts.__list_of_desserts
#
#
# class Dessert:
#
#     def __init__(self, name, type, image, weight, price, ingredients):
#         self.dessert_name = name
#         self.dessert_type = type
#         self.image_url = image
#         self.weight_gram = weight
#         self.price = price
#         with open("additional_dessert_data/dessert_ingredients.txt", "a") as fl:
#             fl.write(f"{self.dessert_name} інгредієнти: \n{ingredients}\n\n")
#
#         data = DessertData(dessert_name=self.dessert_name, dessert_type=self.dessert_type, image_url=self.image_url,
#                            weight_gram=self.weight_gram, price=self.price, ingredients=ingredients)
#         session.add(data)
#         session.commit()
#
#     def __repr__(self):
#         return f"Назва виробу: {self.dessert_name},\nтип виробу: {self.dessert_type},\n" \
#                f"ціна виробу: {self.price},\nпосилання на фото: {self.image_url}\n"
#
#
# class Order:
#
#     def __init__(self, pib: str, telephone_number, order: dict):
#         self.pib =  pib
#         self.telephone_number = telephone_number
#         self.order = order
#         self.cost = 0
#         for key, value in self.order.items():
#             price = session.query(DessertData.price).filter(DessertData.dessert_name == key).limit(1).scalar()
#             self.cost += int(price) * value
#
#
#     def write_to_db(self):
#         name, first_name, second_name = self.pib.split(' ')
#         data = OrderData(name=name, first_name=first_name, second_name=second_name,
#                          telephone_number=self.telephone_number, order=self.__return_orders(), cost=self.cost)
#
#         session.add(data)
#         session.commit()
#     def __return_orders(self):
#         order_rerp = ''
#         for key, value in self.order.items():
#             order_rerp += f"{key} - {value}шт.\n"
#         return order_rerp
#
#     def __repr__(self):
#         return f"Замовлення на {self.pib}\n" \
#                f"Замовлення складається з:\n{self.__return_orders()}"
#
#     @staticmethod
#     def get_total_cost():
#         total = session.query(func.sum(OrderData.cost))
#         return f"Загальна вартість усіх замовлень: {total.scalar()}грн."
#

if __name__ == '__main__':
    db_creator()
    cat = Category(category_id=1, category_name='тістечко')
    cat2 = Category(category_id=2, category_name='торт')
    dessert_1 = Dessert(dessert_name="Наполеон", category_id=2,
                        image_url=r"https://images.unian.net/photos/2020_07/thumb_files/1000_545_1594640431-9859.jpg",
                        weight_gram=200, price=60, ingredients="мука, яйця, маргарин, сіль, жирне молоко, цукор, вершкове масло, ванілін")

    dessert_2 = Dessert(dessert_name="Десерт картошка", category_id=1,
                        image_url=r"https://rutxt.ru/files/16665/original/602389a6e8.jpg",
                        weight_gram=150, price=35, ingredients="печиво, згущене молоко, вершкове масло, какао")
    session.add_all([cat, dessert_1, cat2, dessert_2])
    session.commit()
    # try:
    #     query = session.query(Dessert).filter(Dessert.weight_gram == 150 and Dessert.price == 35). \
    #     update({Dessert.weight_gram: 180}, synchronize_session=False)
    #     session.commit()
    # except SQLAlchemyError:
    #     session.rollback()
    #     print({'error': 'error'})
    # print(True)
    # quant = session.query(Dessert).filter(Dessert.weight_gram == 50 and Dessert.price == 35). \
    #     update({Dessert.weight_gram: 180}, synchronize_session=False)
    # session.commit()

    # cat_1 = Category(category_name="тістечко")
    # cat_2 = Category(category_name="торт")
    # session.add_all([cat_1, cat_2])
    # us_1 = User(name='Nastia', first_name='Vasyilivna', second_name='Kosteniuk', telephone_number='0984972',
    #             address='novod')
    # dessert_1 = Dessert(dessert_name="Десерт картошка", category_id=1, image_url= r"https://rutxt.ru/files/16665/original/602389a6e8.jpg",
    #                     weight_gram=150, price=35, ingredients="печиво, згущене молоко, вершкове масло, какао")
    # session.add_all([us_1, dessert_1])
    # ord = Order(user_id=1, dessert_id=1, quantity=3, cost=23, state='hbj,kb' )
    # print(dessert_1.category)
    # print(ord.user)
    # session.add(ord)
    # session.commit()
    # res = session.query(Order).all()
    # print(res[0].user.second_name)
    # res = session.query(Category).filter(Category.category_name == 'тістечко').first()
    # result = session.query(Dessert).filter(Dessert.category_id == res.category_id).all()
    # print(result)

    # dessert_1 = Dessert("Десерт картошка", "тістечко", r"https://rutxt.ru/files/16665/original/602389a6e8.jpg",
    #                   150, 45, "печиво, згущене молоко, вершкове масло, какао")
    # dessert_2 = Dessert("Наполеон", "торт", "https://images.unian.net/photos/2020_07/thumb_files/1000_545_1594640431-9859.jpg",
    #                   200, 60, "мука, яйця, маргарин, сіль, жирне молоко, цукор, вершкове масло, ванілін")
    # dessert_3 = Dessert("Київський торт", "торт", "https://i.ytimg.com/vi/f8p56xqggsc/maxresdefault.jpg", 245, 65,
    #                      "Цукор, масло, горіх фундук, борошно, згущене молоко, яйце, какао, коньяк, ванілін" )
    #
    # Desserts.add_dessert(dessert_1)
    # Desserts.add_dessert(dessert_2)
    # Desserts.add_dessert(dessert_3)
    # order_1 = Order("Костенюк Анастасія Василівна", "0957861745", {"Наполеон": 2,
    #                                                                "Київський торт": 1})
    # order_2 = Order("Петренко Олег Вікторович", "09354926576", {"Десерт картошка": 3,
    #                                                                "Київський торт": 2,
    #                                                             "Наполеон": 1})



