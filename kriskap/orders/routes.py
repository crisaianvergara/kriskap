from flask import Blueprint, render_template
from kriskap.models import Order
from flask_login import current_user, login_required
from sqlalchemy import desc

orders = Blueprint("orders", __name__)


@orders.route("/order", methods=["GET"])
@login_required
def order():
    """Route for displaying all orders."""

    orders = Order.query.filter_by(buyer_id=current_user.id).order_by(desc("id")).all()
    return render_template("order.html", orders=orders, title="Orders")
