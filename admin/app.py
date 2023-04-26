from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask import session as flask_session
from flask_admin import Admin, form, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from wtforms import form, fields, validators
import flask_login as login
from flask_admin import helpers, expose
from werkzeug.security import generate_password_hash, check_password_hash


import bcrypt
from flask_security import Security, SQLAlchemySessionUserDatastore
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user, login_required
from db_utils.database import session, db, base

from db_utils.models import *
from config import PASSWORD


app = Flask(__name__)
app.secret_key = PASSWORD

user_datastore = SQLAlchemySessionUserDatastore(session, AdminUser, Role)
security = Security(app, user_datastore)

class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.InputRequired()])
    password = fields.PasswordField(validators=[validators.InputRequired()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return session.query(AdminUser).filter_by(login=self.login.data).first()


class RegistrationForm(form.Form):
    login = fields.StringField(validators=[validators.InputRequired()])
    email = fields.StringField()
    password = fields.PasswordField(validators=[validators.InputRequired()])

    def validate_login(self, field):
        if session.query(AdminUser).filter_by(login=self.login.data).count() > 0:
            raise validators.ValidationError('Duplicate username')

def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return session.query(AdminUser).get(user_id)

class SecureModelView(ModelView):
    # pass
    def is_accessible(self):
        return login.current_user.is_authenticated

class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        # return self.render('admin/index.html', username='admin')
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyHomeView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyHomeView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = AdminUser()

            form.populate_obj(user)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            user.password = generate_password_hash(form.password.data)

            session.add(user)
            session.commit()

            login.login_user(user)
            return redirect(url_for('.index'))
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyHomeView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))

init_login()

admin = Admin(app, name='Sweeet Dream', index_view=MyHomeView(),  template_mode='bootstrap4', endpoint='admin')

def name_gen_image(model, file_data):
    hash_name =  f"{model.dessert_name}"
    return hash_name



# def create_superuser(user_id) ->None:
#     adm_user = session.query(AdminUser).filter(AdminUser.id == user_id).update(
#         {AdminUser.role: 'super_user'}
#     )
#     session.commit()

class AdminUserView(SecureModelView):
    column_hide_backrefs = False
    can_create = False
    can_edit = False


# class DessertView(SecureModelView):
#     def _list_thumbnail(view, context, model, name):
#         if not model.image:
#             return ''
#
#         return Markup(
#             f'<img src={url_for("static", filename=os.path.join("dessert_image/", model.image))} width="100">'
#         )
#
#     # url = url_for('static', filename=os.path.join('dessert_image/', model.dessert_image))
#     # if model.dessert_image.split('.')[-1] in ['jpg', 'jpeg', 'png', 'svg']:
#     #     return Markup(f'<img scr={url} width="100">')
#
#     column_formatters = {
#         'dessert_image': _list_thumbnail
#     }
#
#     form_extra_fields = {
#         'dessert_image': form.ImageUploadField(
#             'Image', base_path='static/dessert_image/',
#             namegen=name_gen_image)
#     }

admin.add_view(SecureModelView(User, session))
admin.add_view(SecureModelView(Category, session))
admin.add_view(SecureModelView(Comment, session))
admin.add_view(SecureModelView(Order, session))
admin.add_view(SecureModelView(Dessert, session))
admin.add_view(SecureModelView(OrderDessert, session))
admin.add_view(AdminUserView(AdminUser, session))
admin.add_view(SecureModelView(Role, session))



if __name__ == '__main__':
    # user_datastore.create_user(email='nastia_admin@gmail.com', password="admin")
    # session.commit()
    app.run(debug=True)
