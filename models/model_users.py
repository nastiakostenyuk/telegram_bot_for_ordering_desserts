from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from models.database import base


class User(base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String, default = None)
    second_name = Column(String, default = None)
    telephone_number = Column(String, default = None)
    address = Column(String, default = None)

    order = relationship("Order", back_populates='user')