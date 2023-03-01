from datetime import datetime

from sqlalchemy import Column, String, Integer, Numeric, VARCHAR, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TEXT


from models.database import base
from sqlalchemy import DateTime


class Comment(base):
    __tablename__ = 'comments'
    comment_id = Column(String, primary_key=True)
    order_id = Column(String, ForeignKey('orders.order_id'))
    author = Column(String)
    comment = Column(TEXT)
    date_time = Column(String)

    order = relationship("Order", back_populates='comment')


