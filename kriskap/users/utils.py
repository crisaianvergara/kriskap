import os
import secrets
from flask import current_app, abort, url_for
from PIL import Image
from functools import wraps
from flask_login import current_user
from flask_mail import Message
from kriskap import mail


def admin_only(f):
    """Decorator function that restricts access to routes to admin users only."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.user_type != "admin":
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


def save_profile_picture(form_picture):
    """Resizes and saves the user's profile picture."""

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, "static/img", picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    """Send an email to reset the password of a user."""

    token = user.get_reset_token()
    msg = Message(
        "Password Reset Request",
        sender="SuperXaian4Kuruno@yahoo.com",
        recipients=[user.email],
    )
    msg.body = f"""To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
"""
    mail.send(msg)
