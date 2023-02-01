from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Numeric, VARCHAR, ForeignKey

from models.database import base, session


class Dessert(base):
    __tablename__ = 'desserts'

    dessert_id = Column(Integer, primary_key=True)
    dessert_name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    image_url = Column(String)
    weight_gram = Column(Numeric)
    price = Column(Numeric)
    ingredients = Column(VARCHAR)

    category = relationship("Category", back_populates='dessert')
    order = relationship("Order", back_populates='dessert')

    def __repr__(self):
        return f"Десертик: {self.dessert_name},\nкатегорія: {self.category.category_name},\n"\
               f"ціна: {self.price} грн."\
               f"Десертик складається з:\n{self.ingredients}"

