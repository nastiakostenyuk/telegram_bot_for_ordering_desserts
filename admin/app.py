from flask import Flask, render_template, request, redirect, url_for, flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


from models.database import session
from models.model_category import Category
from models.model_comments import Comment
from models.model_desserts import Dessert
from models.model_orders import Order
from models.model_users import User
from models.order_dessert import OrderDessert



app = Flask(__name__)
app.secret_key = 'dghnsoi4356tbn4862bt2'

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


admin = Admin(app, name='microblog', template_mode='bootstrap3')
# Add administrative views here


admin.add_view(ModelView(User, session))
admin.add_view(ModelView(Category, session))
admin.add_view(ModelView(Comment, session))
admin.add_view(ModelView(Order, session))
admin.add_view(ModelView(Dessert, session))
admin.add_view(ModelView(OrderDessert, session))



if __name__ == '__main__':
    app.run(debug=True)
