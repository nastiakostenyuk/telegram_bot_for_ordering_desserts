from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask import session as flask_session
from flask_admin import Admin, form, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask import url_for, Markup
import os
import bcrypt

from db_utils.database import session
from db_utils.models import *
from config import PASSWORD


app = Flask(__name__)
app.secret_key = PASSWORD

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        adm_user = session.query(AdminUser).first()
        return self.render('admin/index.html', username=adm_user.username)


admin = Admin(app, name='Sweeet Dream', index_view=MyHomeView(),  template_mode='bootstrap3', endpoint='admin')

def name_gen_image(model, file_data):
    hash_name =  f"{model.dessert_name}"
    return hash_name

class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in flask_session:
            return True
        else:
            return redirect("/login")



def create_superuser(user_id) ->None:
    adm_user = session.query(AdminUser).filter(AdminUser.id == user_id).update(
        {AdminUser.role: 'super_user'}
    )
    session.commit()

class AdminUserView(SecureModelView):

    column_list = ("username", "first_name", "second_name", "role")
    can_create = False
    can_edit = False


class DessertView(SecureModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return ''

        return Markup(
            f'<img src={url_for("static", filename=os.path.join("dessert_image/", model.image))} width="100">'
        )

    # url = url_for('static', filename=os.path.join('dessert_image/', model.dessert_image))
    # if model.dessert_image.split('.')[-1] in ['jpg', 'jpeg', 'png', 'svg']:
    #     return Markup(f'<img scr={url} width="100">')

    column_formatters = {
        'dessert_image': _list_thumbnail
    }

    form_extra_fields = {
        'dessert_image': form.ImageUploadField(
            'Image', base_path='static/dessert_image/',
            namegen=name_gen_image)
    }

admin.add_view(SecureModelView(User, session))
admin.add_view(SecureModelView(Category, session))
admin.add_view(SecureModelView(Comment, session))
admin.add_view(SecureModelView(Order, session))
admin.add_view(DessertView(Dessert, session))
admin.add_view(SecureModelView(OrderDessert, session))
admin.add_view(AdminUserView(AdminUser, session))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = session.query(AdminUser).filter(AdminUser.username == request.form.get("username")).first()
        if user:
            if bcrypt.checkpw(request.form.get("password").encode('utf-8'), user.password):
                flask_session['logged_in'] = True
                return redirect("/admin")
            else:
                return render_template('login.html', failed=True)
    return render_template('login.html')


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        second_name = request.form.get("second_name")
        username = request.form.get("username")
        password = request.form.get('password')
        if all([first_name, second_name, username, password]):
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            new_user = AdminUser(username=username, first_name=first_name, second_name=second_name, password=hashed)
            session.add(new_user)
            session.commit()
            redirect("/login")
    return render_template('signup.html')


@app.route("/logout")
def logout():
    flask_session.clear()
    return redirect("/")



if __name__ == '__main__':
    app.run(debug=True)
