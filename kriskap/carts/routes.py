from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from kriskap.models import Cart, Product
from kriskap.carts.forms import CartForm
from kriskap import db

carts = Blueprint("carts", __name__)


@carts.route("/cart")
@login_required
def cart():
    """Route for displaying a user's cart."""

    carts = Cart.query.filter_by(buyer_id=current_user.id).all()
    return render_template("cart.html", title="Cart", carts=carts)


@carts.route("/cart/<int:cart_id>/remove")
@login_required
def remove_cart(cart_id):
    """Route for removing a cart item from a user's cart."""

    cart = Cart.query.get_or_404(cart_id)
    product_name = cart.parent_product.name
    db.session.delete(cart)
    db.session.commit()
    flash(f"{product_name} removed from your cart.", "success")
    return redirect(url_for("carts.cart"))


@carts.route("/cart/update", methods=["POST"])
@login_required
def update():
    """Route for updating the quantity of a cart item."""

    cart = Cart.query.get_or_404(request.form["cart_id"])
    stock = cart.parent_product.stock
    # if the requested quantity is greater than the maximum stock, set the quantity to the maximum stock
    if stock < int(request.form["quantity"]):
        cart.quantity = stock
    # otherwise, set the quantity to the requested quantity
    else:
        cart.quantity = request.form["quantity"]
    db.session.commit()
    # get all of the user's carts
    items = Cart.query.filter_by(buyer_id=current_user.id).all()
    # calculate the total quantity and subtotal for the user's cart
    cart_total = sum([item.quantity for item in items])
    cart_subtotal = "₱{:,.2f}".format(
        sum([item.quantity * item.parent_product.price for item in items])
    )
    # calculate the total cost for the updated cart item
    total = "₱{:,.2f}".format(cart.quantity * cart.parent_product.price)
    return jsonify(
        {
            "total": total,
            "cart_total": cart_total,
            "cart_subtotal": cart_subtotal,
            "max": stock,
        }
    )


@carts.route("/cart/<product_id>/need-login")
@login_required
def need_login(product_id):
    """Route for redirecting the user to the login page when attempting to add a product to their cart."""

    return redirect(url_for("carts.view_product", product_id=product_id))


@carts.route("/cart/check-stock", methods=["POST"])
@login_required
def check_stock():
    """Route for checking the stock of a product."""

    product = Product.query.get_or_404(request.form["product_id"])
    current_user_item = Cart.query.filter_by(
        buyer_id=current_user.id, product_id=product.id
    ).first()

    # Calculate the available stock
    if current_user_item:
        available_stock = product.stock - current_user_item.quantity
    else:
        available_stock = product.stock
    return jsonify({"result": "success", "available_stock": available_stock})


@carts.route("/product/<int:product_id>/view", methods=["GET", "POST"])
def view_product(product_id):
    """Route for viewing a product's details."""

    form = CartForm(quantity=1)
    requested_product = Product.query.get_or_404(product_id)
    if current_user.is_authenticated:
        if form.validate_on_submit():
            # Get the current user's cart item for the requested product (if it exists)
            current_user_item = Cart.query.filter_by(
                buyer_id=current_user.id, product_id=requested_product.id
            ).first()

            # If the user already has the maximum quantity of the product in their cart
            if current_user_item:
                if requested_product.stock <= current_user_item.quantity:
                    flash(
                        f"You have reached the maximum quantity available for {requested_product.name}.",
                        "info",
                    )
                    return redirect(
                        url_for("carts.view_product", product_id=product_id)
                    )
                # Otherwise, add the product to the user's cart
                else:
                    current_user_item.quantity += form.quantity.data
                    db.session.commit()
                    flash(
                        f"{requested_product.name} has been added to your cart!",
                        "success",
                    )
                    return redirect(
                        url_for("carts.view_product", product_id=product_id)
                    )
            # Otherwise, create a new cart item
            else:
                new_cart = Cart(
                    buyer=current_user,
                    parent_product=requested_product,
                    quantity=form.quantity.data,
                )
                db.session.add(new_cart)
                db.session.commit()
                flash(
                    f"{requested_product.name} has been added to your cart!", "success"
                )
                return redirect(url_for("carts.view_product", product_id=product_id))
    return render_template(
        "view_product.html",
        product=requested_product,
        title=requested_product.name,
        form=form,
    )
