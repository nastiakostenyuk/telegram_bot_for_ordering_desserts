from flask import Flask, render_template, request, redirect, url_for, flash
from flask_admin import Admin, form
from flask_admin.contrib.sqla import ModelView
from flask import url_for, Markup
import os

from db_utils.database import session
from db_utils.models import *
from config import PASSWORD


app = Flask(__name__)
app.secret_key = PASSWORD

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


admin = Admin(app, name='Sweeet Dream', template_mode='bootstrap3')
# Add administrative views here
def name_gen_image(model, file_data):
    hash_name =  f"{model.dessert_name}"
    return hash_name


class DessertView(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return ''

        return Markup(
            f'<img src={url_for("static", filename=os.path.join("image/", model.image))} width="100">'
        )

    # url = url_for('static', filename=os.path.join('image/', model.image))
    # if model.image.split('.')[-1] in ['jpg', 'jpeg', 'png', 'svg']:
    #     return Markup(f'<img scr={url} width="100">')

    column_formatters = {
        'image': _list_thumbnail
    }

    form_extra_fields = {
        'image': form.ImageUploadField(
            'Image', base_path='static/image/',
            namegen=name_gen_image)
    }


admin.add_view(ModelView(User, session))
admin.add_view(ModelView(Category, session))
admin.add_view(ModelView(Comment, session))
admin.add_view(ModelView(Order, session))
admin.add_view(DessertView(Dessert, session))
admin.add_view(ModelView(OrderDessert, session))



if __name__ == '__main__':
    app.run(debug=True)
