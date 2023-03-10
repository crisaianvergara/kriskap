from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
import stripe
from kriskap import db
from kriskap.models import Cart, Order

checkout = Blueprint("checkout", __name__)


@checkout.route("/create-checkout-session", methods=["POST"])
@login_required
def create_checkout_session():
    """Route for creating a checkout session."""

    carts = Cart.query.filter_by(buyer_id=current_user.id).all()
    # Prepare items for checkout
    items = [
        {"price": cart.parent_product.stripe_price, "quantity": cart.quantity}
        for cart in carts
    ]
    try:
        # Create the checkout session
        checkout_session = stripe.checkout.Session.create(
            line_items=items,
            mode="payment",
            success_url=url_for("checkout.success_checkout", _external=True)
            + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=url_for("checkout.cancel_checkout", _external=True),
        )
    except Exception as e:
        # Return error message if session creation failed
        return str(e)

    return redirect(checkout_session.url, code=303)


@checkout.route("/create-checkout-session/success")
@login_required
def success_checkout():
    """Route for handling a successful checkout."""
    carts = Cart.query.filter_by(buyer_id=current_user.id).all()
    for cart in carts:
        # Add cart to order history
        new_order = Order(
            buyer=current_user,
            parent_product=cart.parent_product,
            quantity=cart.quantity,
            order_total=cart.parent_product.price * cart.quantity,
            status="Paid",
        )
        # Update stock of parent product
        cart.parent_product.stock = cart.parent_product.stock - cart.quantity
        db.session.add(new_order)
        db.session.commit()
        db.session.delete(cart)
        db.session.commit()
    flash("Paid successfully. Thank you so much.", "success")
    return redirect(url_for("carts.cart"))


@checkout.route("/create-checkout-session/cancel")
@login_required
def cancel_checkout():
    """Route for handling a cancelled checkout."""

    return redirect(url_for("carts.cart"))
