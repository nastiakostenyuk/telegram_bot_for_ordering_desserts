from sqlalchemy import Column, String, Integer, Numeric, VARCHAR

from models.database import base


class DessertData(base):
    __tablename__ = 'desserts'

    dessert_id = Column(Integer, primary_key=True)
    dessert_name = Column(String, nullable=False)
    dessert_type = Column(String)
    image_url = Column(String)
    weight_gram = Column(Numeric)
    price = Column(Numeric)
    ingredients = Column(VARCHAR)

    def __repr__(self):
        return f"Назва виробу: {self.dessert_name},\nтип виробу: {self.dessert_type},\n" \
               f"ціна виробу: {self.price} грн."


