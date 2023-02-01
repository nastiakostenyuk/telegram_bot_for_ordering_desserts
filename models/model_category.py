from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


from models.database import base, session


class Category(base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String)

    dessert = relationship("Dessert", back_populates='category')




