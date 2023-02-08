from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from kriskap.users.utils import admin_only
from kriskap.models import User
from kriskap import db


admins = Blueprint("admins", __name__)


@admins.route("/admin")
@login_required
@admin_only
def admin():
    users = User.query.all()
    return render_template("admin.html", title="Admin", users=users)


@admins.route("/admin/<int:user_id>/add")
@login_required
@admin_only
def add_admin(user_id):
    user = User.query.get_or_404(user_id)
    user.user_type = "admin"
    db.session.commit()
    flash(f"{user.username} has been add as an admin.", "success")
    return redirect(url_for("admins.admin"))


@admins.route("/admin/<int:user_id>/remove")
@login_required
@admin_only
def remove_admin(user_id):
    user = User.query.get_or_404(user_id)
    user.user_type = "customer"
    db.session.commit()
    flash(f"{user.username} has been remove as an admin.", "success")
    return redirect(url_for("admins.admin"))
