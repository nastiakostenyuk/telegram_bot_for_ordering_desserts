from sqlalchemy import Column, String, Integer, Numeric, VARCHAR

from models.database import base


class OrderData(base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    name = Column(String)
    first_name = Column(String)
    second_name = Column(String)
    telephone_number = Column(String)
    order = Column(VARCHAR)
    cost = Column(Numeric)


