from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from kriskap.password.forms import ChangePasswordForm
from kriskap.models import User
from kriskap import db
from werkzeug.security import generate_password_hash

password = Blueprint("password", __name__)


@password.route("/password/change", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    user = User.query.get_or_404(current_user.id)
    if form.validate_on_submit():
        hash_and_salted_password = generate_password_hash(
            form.new_password.data, method="pbkdf2:sha256", salt_length=8
        )
        user.password = hash_and_salted_password
        db.session.commit()
        flash("Your password has been changed.", "success")
        return redirect(url_for("password.change_password"))
    return render_template("change_password.html", title="Change Password", form=form)
