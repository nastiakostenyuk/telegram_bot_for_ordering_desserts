from sqlalchemy import Column, String, Integer, Numeric, VARCHAR, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from models.model_users import User
from models.model_desserts import Dessert
from models.database import base



STATE = {'in_progress', 'finished', 'canceled'}


class Order(base):
    __tablename__ = 'orders'

    order_id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    desserts = Column(postgresql.ARRAY(String), default = None)
    cost = Column(Numeric, default = None)
    state = Column(String, default = None)
    time = Column(String)
    comment = Column(String, default = None)

    user = relationship("User", back_populates="order")
    order_dessert = relationship('OrderDessert', back_populates='order')


