import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    abort,
    Markup,
)
from flask_admin import Admin, form
from flask import session as flask_session
from flask_admin.contrib.sqla import ModelView

from db_utils.models import *
from db_utils.database import session as db_session
from config import PASSWORD


app = Flask(__name__)
app.secret_key = PASSWORD

admin = Admin(app, name="Sweeet Dream", template_mode="bootstrap3")


class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in flask_session:
            return True
        else:
            abort(403)


def name_gen_image(model, file_data):
    hash_name = f"{model.image}"
    return hash_name


class DessertView(SecureModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return ""

        return Markup(
            f'<img src={url_for("static", filename=os.path.join("dessert_image/", model.image))} width="100">'
        )

    column_formatters = {"image": _list_thumbnail}

    form_extra_fields = {
        "dessert_image": form.ImageUploadField(
            "Image", base_path="static/dessert_image/", namegen=name_gen_image
        )
    }


admin.add_view(SecureModelView(User, db_session))
admin.add_view(SecureModelView(Category, db_session))
admin.add_view(SecureModelView(Comment, db_session))
admin.add_view(SecureModelView(Order, db_session))
admin.add_view(DessertView(Dessert, db_session))
admin.add_view(SecureModelView(OrderDessert, db_session))
admin.add_view(SecureModelView(AdminUser, db_session))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = (
            db_session.query(AdminUser)
            .filter(AdminUser.username == request.form.get("username"))
            .first()
        )
        if user:
            if bcrypt.checkpw(
                request.form.get("password").encode("utf-8"),
                user.password.encode("utf-8"),
            ):
                print("good")
                flask_session["logged_in"] = True
                return redirect("/admin")
            else:
                return render_template("security/login.html", failed=True)
        else:
            return render_template("security/login.html", failed=True)
    return render_template("security/login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if all([username, password]):
            password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            try:
                new_user = AdminUser(
                    username=username, password=password_hash.decode("utf-8")
                )
                db_session.add(new_user)
                db_session.commit()
                return redirect("/login")
            except Exception as ex:
                return render_template("security/signup.html", failed=True)

    return render_template("security/signup.html")


@app.route("/logout")
def logout():
    flask_session.clear()
    return redirect("/")


@app.route("/")
def index():
    return '<a href="/login">Click me to get to Admin!</a>'


if __name__ == "__main__":
    db_session.commit()
    app.run(debug=True)
