# from sqlalchemy import func
#
import datetime

from sqlalchemy.exc import SQLAlchemyError

from models.model_desserts import Dessert
from models.model_orders import Order
from models.model_category import Category
from models.model_users import User
from models.order_dessert import OrderDessert
from models.database import session
from models.database import create_db as db_creator, delete_tables
#

def get_categories():
    categories_lst = [elem.category_name for elem in session.query(Category).all()]
    return categories_lst


if __name__ == '__main__':
    delete_tables()
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


