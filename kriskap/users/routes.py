from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from kriskap import db
from kriskap.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from kriskap.users.forms import LoginForm, RegistrationForm, UpdateAccountForm
from kriskap.users.utils import save_profile_picture


users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_and_salted_password = generate_password_hash(
            form.password.data, method="pbkdf2:sha256", salt_length=8
        )
        if User.query.filter_by(id=1).first():
            user_type = "customer"
        else:
            user_type = "admin"
        new_user = User(
            user_type=user_type,
            username=form.username.data,
            name=form.name.data,
            email=form.email.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in.", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Sign Up", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("Incorrect email or password.", "danger")
            return redirect(url_for("users.login"))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get("next")
        return redirect(next_page) if next_page else redirect(url_for("main.home"))
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image_f.data:
            image_f = save_profile_picture(form.image_f.data)
            current_user.image_file = image_f
        current_user.username = form.username.data
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.name.data = current_user.name
        form.email.data = current_user.email
    image_file = url_for(
        "static", filename="img/profile_pics/" + current_user.image_file
    )
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )
