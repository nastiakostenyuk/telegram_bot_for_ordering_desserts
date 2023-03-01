from sqlalchemy import Column, String, Integer, Numeric, VARCHAR, ForeignKey, Table
from sqlalchemy.orm import relationship


from models.database import base
from sqlalchemy import DateTime


class OrderDessert(base):
    __tablename__ = 'order_dessert'
    order_id = Column(String,  ForeignKey("orders.order_id"), primary_key=True)
    dessert_id = Column(Integer, ForeignKey("desserts.dessert_id"), primary_key=True)
    quantity = Column(Integer, default = None)
    cost = Column(Integer)

    order = relationship("Order", back_populates='order_dessert')
    dessert = relationship("Dessert", back_populates='order_dessert')

