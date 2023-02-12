from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required
import stripe

checkout = Blueprint("checkout", __name__)


@checkout.route("/create-checkout-session", methods=["POST"])
@login_required
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": "price_1MahdXGkcotjc1A8liu7i7CO",
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=url_for("checkout.success_checkout", _external=True),
            cancel_url=url_for("checkout.cancel_checkout", _external=True),
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


@checkout.route("/create-checkout-session/success")
@login_required
def success_checkout():
    return render_template("success.html")


@checkout.route("/create-checkout-session/cancel")
@login_required
def cancel_checkout():
    return render_template("cancel.html")
