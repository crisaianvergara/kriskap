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
    """Route that registers a new user."""

    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash and salt the user's password before storing it in the database
        hash_and_salted_password = generate_password_hash(
            form.password.data, method="pbkdf2:sha256", salt_length=8
        )
        # If the first user is being registered, make them an admin. Otherwise, make them a customer.
        if User.query.first():
            user_type = "customer"
        else:
            user_type = "admin"
        # Create a new User object adn add it to the database
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
    """Route that logs in a user."""

    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        # Find the user with the given email address
        user = User.query.filter_by(email=email).first()
        # If the user does not exist or the password is incorrect, display an error message and redirect back to the login page
        if not user or not check_password_hash(user.password, password):
            flash("Incorrect email or password.", "danger")
            return redirect(url_for("users.login"))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get("next")
        return redirect(next_page) if next_page else redirect(url_for("main.home"))
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    """Log out the current user and redirect them to the home page."""

    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """Route for user account page. Allows users to update their account information and profile picture."""

    form = UpdateAccountForm()
    if form.validate_on_submit():
        # Update the user's account information
        current_user.image_file = form.image_f.data
        current_user.username = form.username.data
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("users.account"))
    # Handle GET request to page
    elif request.method == "GET":
        # Prepopulate form fields with user's current information
        form.username.data = current_user.username
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.image_f.data = current_user.image_file
    return render_template("account.html", title="Account", form=form)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    """Route for requesting a password reset. Allows users to enter their email address to receive reset instructions."""

    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        # Find user with matching email and send reset instructions
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            "An email has been sent with instructions to reset your password.", "info"
        )
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    """Route for resetting user password using reset token. Allows user to enter a new password."""

    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    # Verify reset token
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
