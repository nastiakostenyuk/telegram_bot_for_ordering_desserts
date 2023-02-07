from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Numeric, VARCHAR, ForeignKey
import emoji
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
        return f"{emoji.emojize(':sparkles:')}Десертик: {self.dessert_name},\n{emoji.emojize(':sparkles:')}категорія: {self.category.category_name},\n"\
               f"{emoji.emojize(':sparkles:')}ціна: {self.price} грн.\n"\
               f"{emoji.emojize(':sparkles:')}Десертик складається з:\n{self.ingredients}"

