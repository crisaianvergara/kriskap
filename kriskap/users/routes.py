from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from kriskap import db
from kriskap.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from kriskap.users.forms import (
    LoginForm,
    RegistrationForm,
    UpdateAccountForm,
    RequestResetForm,
    ResetPasswordForm,
)
from kriskap.users.utils import save_profile_picture, send_reset_email


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


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            "An email has been sent with instructions to reset your password.", "info"
        )
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hash_and_salted_password = generate_password_hash(
            form.password.data, method="pbkdf2:sha256", salt_length=8
        )
        user.password = hash_and_salted_password
        db.session.commit()
        flash("Your password has been updated! You are now able to log in.", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="Reset Password", form=form)
