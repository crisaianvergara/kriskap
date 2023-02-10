from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from kriskap.models import Cart, Product
from kriskap.carts.forms import CartForm
from kriskap import db

carts = Blueprint("carts", __name__)


@carts.route("/product/<int:product_id>/view-product", methods=["GET", "POST"])
@login_required
def view_product(product_id):
    form = CartForm(quantity="1")
    requested_product = Product.query.get_or_404(product_id)
    if form.validate_on_submit():
        # Edit Cart
        current_user_item = Cart.query.filter_by(buyer_id=current_user.id).all()
        if current_user_item:
            for item in current_user_item:
                if item.product_id == requested_product.id:
                    item.quantity += form.quantity.data
                    db.session.commit()
                    flash("This item has been added to cart!", "success")
                    return redirect(
                        url_for("carts.view_product", product_id=product_id)
                    )
        # Add to Cart
        new_cart = Cart(
            buyer=current_user,
            parent_product=requested_product,
            quantity=form.quantity.data,
        )
        db.session.add(new_cart)
        db.session.commit()
        flash("This item has been added to cart!", "success")
        return redirect(url_for("carts.view_product", product_id=product_id))
    return render_template(
        "view_product.html",
        product=requested_product,
        title=requested_product.name,
        form=form,
    )


@carts.route("/view-cart")
@login_required
def view_cart():
    carts = Cart.query.filter_by(buyer_id=current_user.id)
    return render_template("cart.html", title="View Cart", carts=carts)


@carts.route("/cart/<int:cart_id>/remove")
@login_required
def remove_cart(cart_id):
    cart = Cart.query.get_or_404(cart_id)
    product_name = cart.parent_product.name
    db.session.delete(cart)
    db.session.commit()
    flash(f"{product_name} removed from your cart.", "success")
    return redirect(url_for("carts.view_cart"))


@carts.route("/update", methods=["POST"])
@login_required
def update():
    cart = Cart.query.get_or_404(request.form["cart_id"])
    cart.quantity = request.form["quantity"]
    db.session.commit()
    items = Cart.query.filter_by(buyer_id=current_user.id).all()
    cart_total = sum([item.quantity for item in items])
    cart_subtotal = "₱{:,.2f}".format(
        sum([item.quantity * item.parent_product.price for item in items])
    )
    total = "₱{:,.2f}".format(cart.quantity * cart.parent_product.price)
    return jsonify(
        {
            "total": total,
            "cart_total": cart_total,
            "cart_subtotal": cart_subtotal,
        }
    )
