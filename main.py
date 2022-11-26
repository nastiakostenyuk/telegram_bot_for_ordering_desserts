from sqlalchemy import func

from models.model_desserts import DessertData
from models.model_orders import OrderData
from models.database import session
from models.database import create_db as db_creator


class Desserts:
    __list_of_desserts = []

    def __new__(cls, *args, **kwargs):
        return None

    @classmethod
    def add_dessert(cls, dessert):
        Desserts.__list_of_desserts.append(dessert)

    @classmethod
    def search_dessert(cls, param, value):
        try:
            for elem in Desserts.__list_of_desserts:
                if elem.__dict__[param] == value:
                    return elem
            return "Десерту з таким параметром не знайшлось"
        except ValueError:
            print("Такого параметру немає")

    @classmethod
    def remove_dessert(cls, del_name):
        delete_elem = None
        for index, elem in enumerate(Desserts.__list_of_desserts):
            if elem.dessert_name == del_name:
                delete_elem = Desserts.__list_of_desserts.pop(index)
                session.query(DessertData).filter(DessertData.dessert_name == del_name).delete()
                session.commit()
        return delete_elem

    @classmethod
    def get_desserts_types(cls):
        types = []
        for type in session.query(DessertData.dessert_type).distinct():
            types.append(type.dessert_type)
        return f"Типи десертів: {types}"

    @classmethod
    def return_lst_with_desserts(cls):
        return Desserts.__list_of_desserts


class Dessert:

    def __init__(self, name, type, image, weight, price, ingredients):
        self.dessert_name = name
        self.dessert_type = type
        self.image_url = image
        self.weight_gram = weight
        self.price = price
        with open("additional_dessert_data/dessert_ingredients.txt", "a") as fl:
            fl.write(f"{self.dessert_name} інгредієнти: \n{ingredients}\n\n")

        data = DessertData(dessert_name=self.dessert_name, dessert_type=self.dessert_type, image_url=self.image_url,
                           weight_gram=self.weight_gram, price=self.price, ingredients=ingredients)
        session.add(data)
        session.commit()

    def __repr__(self):
        return f"Назва виробу: {self.dessert_name},\nтип виробу: {self.dessert_type},\n" \
               f"ціна виробу: {self.price},\nпосилання на фото: {self.image_url}\n"


class Order:

    def __init__(self, pib: str, telephone_number, order: dict):
        self.name, self.first_name, self.second_name = pib.split(' ')
        self.telephone_number = telephone_number
        self.order = order
        self.cost = 0
        for key, value in self.order.items():
            price = session.query(DessertData).filter(DessertData.dessert_name == "Десерт картошка").one()
            self.cost += int(price.price) * value

        data = OrderData(name=self.name, first_name=self.second_name, second_name=self.second_name,
                         telephone_number=self.telephone_number, order=self.__return_orders(), cost=self.cost)

        session.add(data)
        session.commit()

    def __return_orders(self):
        order_rerp = ''
        for key, value in self.order.items():
            order_rerp += f"{key} - {value}шт.\n"
        return order_rerp

    def __repr__(self):
        return f"Замовлення на {self.name} {self.first_name} {self.second_name}\n" \
               f"Замовлення складається з:\n{self.__return_orders()}"

    @staticmethod
    def get_total_cost():
        total = session.query(func.sum(OrderData.cost))
        return f"Загальна вартість усіх замовлень: {total.scalar()}грн."


if __name__ == '__main__':

    db_creator()

    dessert_1 = Dessert("Десерт картошка", "тістечко", r"https://rutxt.ru/files/16665/original/602389a6e8.jpg",
                      150, 45, "печиво, згущене молоко, вершкове масло, какао")
    dessert_2 = Dessert("Наполеон", "торт", "https://images.unian.net/photos/2020_07/thumb_files/1000_545_1594640431-9859.jpg",
                      200, 60, "мука, яйця, маргарин, сіль, жирне молоко, цукор, вершкове масло, ванілін")
    dessert_3 = Dessert("Київський торт", "торт", "https://i.ytimg.com/vi/f8p56xqggsc/maxresdefault.jpg", 245, 65,
                         "Цукор, масло, горіх фундук, борошно, згущене молоко, яйце, какао, коньяк, ванілін" )

    Desserts.add_dessert(dessert_1)
    Desserts.add_dessert(dessert_2)
    Desserts.add_dessert(dessert_3)
    print(Desserts.get_desserts_types())
    order_1 = Order("Костенюк Анастасія Василівна", "0957861745", {"Наполеон": 2,
                                                                   "Київський торт": 1})
    order_2 = Order("Петренко Олег Вікторович", "09354926576", {"Десерт картошка": 3,
                                                                   "Київський торт": 2,
                                                                "Наполеон": 1})
    print(Order.get_total_cost())


