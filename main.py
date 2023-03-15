# from sqlalchemy import func
#
import datetime

import psycopg2
from sqlalchemy.exc import SQLAlchemyError

from db_utils.models import *
from db_utils.database import session
from db_utils.database import create_db as db_creator, delete_tables
#

def get_categories():
    categories_lst = [elem.category_name for elem in session.query(Category).all()]
    return categories_lst


if __name__ == '__main__':
    delete_tables()
    db_creator()
    image1 = open('image/картошка', 'rb').read()

    cat = Category(category_id=1, category_name='тістечко')
    cat2 = Category(category_id=2, category_name='торт')
    with open('image/maxresdefault.jpg', 'rb') as fl:
        bts = fl.read()
        dessert_1 = Dessert(dessert_name="Наполеон", category_id=2,
                            image_url=bts,
                            weight_gram=200, price=60, ingredients="мука, яйця, маргарин, сіль, жирне молоко, цукор, вершкове масло, ванілін")

    with open('image/картошка', 'rb') as fl:
        bts = fl.read()
        dessert_2 = Dessert(dessert_name="Десерт картошка", category_id=1,
                            image_url=bts,
                            weight_gram=150, price=35, ingredients="печиво, згущене молоко, вершкове масло, какао")
    session.add_all([cat, dessert_1, cat2])
    session.add(dessert_2)
    session.commit()
    # with open('image/maxresdefault.jpg', 'rb') as fl:
    #     bts = fl.read()
    #     edit_desert_image = session.query(Dessert).filter(
    #         Dessert.image_url == "https://rutxt.ru/files/16665/original/602389a6e8.jpg"). \
    #         update({Dessert.image_url: bts})
    #     session.commit()
    # image2 = open('image/картошка', 'rb').read()
    # bnr1 = psycopg2.Binary(image2)

    # edit_desert_image1 = session.query(Dessert).filter(
    #     Dessert.image_url == "https://rutxt.ru/files/16665/original/602389a6e8.jpg"). \
    #     update({Dessert.image_url: psycopg2.BINARY(
    #     r"https://rutxt.ru/files/16665/original/602389a6e8.jpg")})

    # session.commit()


