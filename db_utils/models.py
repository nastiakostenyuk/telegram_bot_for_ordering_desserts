from sqlalchemy import Column, String, Integer, Numeric, VARCHAR, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import TEXT, BYTEA
from sqlalchemy.orm import relationship
import emoji


from db_utils.database import base, session


class Category(base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String)

    dessert = relationship("Dessert", back_populates='category')


class Dessert(base):
    __tablename__ = 'desserts'

    dessert_id = Column(Integer, primary_key=True)
    dessert_name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    image_url = Column(BYTEA)
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


class Comment(base):
    __tablename__ = 'comments'
    comment_id = Column(Integer, primary_key=True)
    order_id = Column(String, ForeignKey('orders.order_id'))
    author = Column(String)
    comment = Column(TEXT, default = None)
    date_time = Column(String)

    order = relationship("Order", back_populates='comment')


class Order(base):
    __tablename__ = 'orders'

    order_id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    desserts = Column(ARRAY(String), default = None)
    cost = Column(Numeric, default = None)
    state = Column(String, default = None)
    time = Column(String)

    user = relationship("User", back_populates="order")
    order_dessert = relationship('OrderDessert', back_populates='order')
    comment = relationship('Comment', back_populates='order')


class OrderDessert(base):
    __tablename__ = 'order_dessert'
    order_id = Column(String,  ForeignKey("orders.order_id"), primary_key=True)
    dessert_id = Column(Integer, ForeignKey("desserts.dessert_id"), primary_key=True)
    quantity = Column(Integer, default = None)
    cost = Column(Integer)

    order = relationship("Order", back_populates='order_dessert')
    dessert = relationship("Dessert", back_populates='order_dessert')
