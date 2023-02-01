from sqlalchemy import Column, String, Integer, Numeric, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship

from models.model_users import User
from models.model_desserts import Dessert
from models.database import base
from sqlalchemy import DateTime


STATE = {'in_progress', 'finished', 'canceled'}


class Order(base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    dessert_id = Column(Integer, ForeignKey('desserts.dessert_id'))
    quantity = Column(Integer, default = None)
    cost = Column(Numeric, default = None)
    state = Column(String)
    time = Column(String)

    user = relationship("User", back_populates="order")
    dessert = relationship("Dessert", back_populates="order")


