from fastapi import FastAPI
from sqladmin import Admin, ModelView

from models.database import db
from models.model_category import Category
from models.model_comments import Comment
from models.model_users import User
from models.model_orders import Order
from models.model_desserts import Dessert
from models.order_dessert import OrderDessert

app = FastAPI()
admin = Admin(app, db)


class CategoryAdmin(ModelView, model=Category):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = [Category.category_id, Category.category_name]

class CommentAdmin(ModelView, model=Comment):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = [Comment.comment_id, Comment.author, Comment.comment, Comment.date_time, Comment.order_id]

class  UserAdmin(ModelView, model=User):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = [User.user_id, User.name, User.second_name, User.address, User.telephone_number]

class  OrderAdmin(ModelView, model=Order):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = [Order.order_id, Order.user_id, Order.desserts, Order.cost, Order.state, Order.time]

class  DessertAdmin(ModelView, model=Dessert):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = [Dessert.dessert_id, Dessert.dessert_name, Dessert.category_id, Dessert.image_url,
                   Dessert.weight_gram, Dessert.price, Dessert.ingredients]

# class  OrderDessertAdmin(ModelView, model=OrderDessert):
#     can_create = False
#     can_edit = False
#     can_delete = False
#     can_view_details = False
#     column_list = [OrderDessert.order_id, OrderDessert.dessert_id, OrderDessert.quantity, OrderDessert.cost]


admin.add_view(CategoryAdmin)
admin.add_view(CommentAdmin)
admin.add_view(UserAdmin)
admin.add_view(OrderAdmin)
admin.add_view(DessertAdmin)
# admin.add_view(OrderDessertAdmin)
