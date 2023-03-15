from flask import Flask, render_template, request, redirect, url_for, flash
from flask_admin import Admin, form
from flask_admin.contrib.sqla import ModelView

from flask import url_for, Markup

from db_utils.database import session
from db_utils.models import *



app = Flask(__name__)
app.secret_key = 'dghnsoi4356tbn4862bt2'

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


admin = Admin(app, name='Sweeet Dream', template_mode='bootstrap3')
# Add administrative views here

class DessertView(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.image_url:
            return ''

        return Markup(
            '<img src="%s">' %
            url_for('static',
                    filename=form.thumbgen_filename(model.image_url))
        )

    column_formatters = {
        'image_url': _list_thumbnail
    }

    form_extra_fields = {
        'image_url': form.ImageUploadField(
            'Image', base_path='image')
    }

admin.add_view(ModelView(User, session))
admin.add_view(ModelView(Category, session))
admin.add_view(ModelView(Comment, session))
admin.add_view(ModelView(Order, session))
admin.add_view(DessertView(Dessert, session))
admin.add_view(ModelView(OrderDessert, session))



if __name__ == '__main__':
    app.run(debug=True)
