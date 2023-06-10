from sqlalchemy import Column, String, Integer, Numeric, VARCHAR, ForeignKey, ARRAY, Boolean
from sqlalchemy.dialects.postgresql import TEXT, TIMESTAMP, BYTEA
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import emoji
import bcrypt

from db_utils.database import base, session as db_session


class Category(base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String)

    dessert = relationship("Dessert", back_populates='category')

    def __repr__(self):
        return self.category_name


class Dessert(base):
    __tablename__ = 'desserts'

    dessert_id = Column(Integer, primary_key=True)
    dessert_name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    image = Column(String)
    weight_gram = Column(Numeric)
    price = Column(Numeric)
    ingredients = Column(VARCHAR)

    category = relationship("Category", back_populates='dessert')
    order_dessert = relationship("OrderDessert", back_populates='dessert')

    def __repr__(self):
        return f"{emoji.emojize(':sparkles:')}Десертик: {self.dessert_name},\n{emoji.emojize(':sparkles:')}категорія: {self.category.category_name},\n"\
               f"{emoji.emojize(':sparkles:')}ціна: {self.price} грн.\n"\
               f"{emoji.emojize(':sparkles:')}Десертик складається з:\n{self.ingredients}"


class User(base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String, default = None)
    second_name = Column(String, default = None)
    telephone_number = Column(String, default = None)
    address = Column(String, default = None)

    order = relationship("Order", back_populates='user')

    def __repr__(self):
        return f"{self.second_name} - {self.name}\n{self.telephone_number}"


class Comment(base):
    __tablename__ = 'comments'
    comment_id = Column(Integer, primary_key=True)
    order_id = Column(String, ForeignKey('orders.order_id'))
    author = Column(String)
    comment = Column(TEXT, default = None)
    date_time = Column(TIMESTAMP, server_default = func.now())

    order = relationship("Order", back_populates='comment')

    def __repr__(self):
        return f"{self.author} - {self.comment}"


class Order(base):
    __tablename__ = 'orders'

    order_id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    desserts = Column(ARRAY(String), default = None)
    cost = Column(Numeric, default = None)
    state = Column(String, default = None)
    date_time = Column(TIMESTAMP, server_default = func.now())

    user = relationship("User", back_populates="order")
    order_dessert = relationship('OrderDessert', back_populates='order')
    comment = relationship('Comment', back_populates='order')

    def __repr__(self):
        return f"{self.user.second_name} - {self.user.telephone_number}\n{self.desserts} - {self.state}"


class OrderDessert(base):
    __tablename__ = 'order_dessert'
    order_id = Column(String,  ForeignKey("orders.order_id"), primary_key=True)
    dessert_id = Column(Integer, ForeignKey("desserts.dessert_id"), primary_key=True)
    quantity = Column(Integer, default = None)
    cost = Column(Integer)

    order = relationship("Order", back_populates='order_dessert')
    dessert = relationship("Dessert", back_populates='order_dessert')



class AdminUser(base):
    __tablename__ = 'admin_user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String, unique=True)

    def __repr__(self):
        return f"{self.username} - {self.password}"

