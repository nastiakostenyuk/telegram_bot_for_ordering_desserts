import os

from flask import Flask, render_template, request, redirect, url_for, flash, abort, Markup
from flask_admin import Admin, form, AdminIndexView, expose
import flask_login as login
from flask_admin import helpers, expose

from flask_admin.contrib.sqla import ModelView

from db_utils.models import *
from config import PASSWORD, PATH_TO_IMAGE


app = Flask(__name__)
app.secret_key = PASSWORD

# user_datastore = SQLAlchemySessionUserDatastore(session, AdminUser, Role)
# security = Security(app, user_datastore)

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')



admin = Admin(app, name='Sweeet Dream', index_view=MyHomeView(),  template_mode='bootstrap3')


class AdminUserView(ModelView):
    column_hide_backrefs = False
    can_create = False
    can_edit = False


def name_gen_image(model, file_data):
    hash_name =  f"{model.dessert_name}"
    return hash_name


class DessertView(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return ''

        return Markup(
            f'<img src={url_for("static", filename=os.path.join("dessert_image/", model.image))} width="100">'
        )
    # f'{url_for("static", filename=os.path.join("image/", model.image))} width="100">'
    # url = url_for('static', filename=os.path.join('image/', model.image))
    # if model.image.split('.')[-1] in ['jpg', 'jpeg', 'png', 'svg']:
    #     return Markup(f'<img scr={url} width="100">')

    column_formatters = {
        'image': _list_thumbnail
    }

    form_extra_fields = {
        'dessert_image': form.ImageUploadField(
            'Image', base_path='static/dessert_image/')
    }

admin.add_view(ModelView(User, session))
admin.add_view(ModelView(Category, session))
admin.add_view(ModelView(Comment, session))
admin.add_view(ModelView(Order, session))
admin.add_view(DessertView(Dessert, session))
admin.add_view(ModelView(OrderDessert, session))
admin.add_view(AdminUserView(AdminUser, session))
admin.add_view(ModelView(Role, session))

@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'

if __name__ == '__main__':
    # user_datastore.create_user(email='nastia_admin@gmail.com', password="admin")
    # session.commit()
    app.run(debug=True)
