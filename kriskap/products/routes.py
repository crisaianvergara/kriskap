from flask import Blueprint, render_template, redirect, url_for, flash, request
from sqlalchemy import desc
from flask_login import login_required
from kriskap import db
from kriskap.models import Product, Cart, Wishlist, Order
from kriskap.products.forms import ProductForm, UpdateProductForm
from kriskap.products.utils import save_product_picture
from kriskap.users.utils import admin_only

products = Blueprint("products", __name__)


@products.route("/product")
@login_required
@admin_only
def product():
    """Route for displaying all products with pagination."""

    page = request.args.get("page", 1, type=int)
    products = Product.query.order_by(desc("id")).paginate(page=page, per_page=5)
    return render_template("product.html", title="Products", products=products)


@products.route("/product/search-product", methods=["GET", "POST"])
def search_product():
    """Route for searching for a product."""

    product_name = request.form["search-product"]
    # Filter products by name
    products = Product.query.filter_by(name=product_name).all()
    if not products:
        flash("That product does not exist in Kriskap.", "danger")
        return redirect(url_for("main.home"))
    return render_template("search_product.html", title="Products", products=products)


@products.route("/product/new", methods=["GET", "POST"])
@login_required
@admin_only
def new_product():
    """Route for adding a new product."""
    form = ProductForm()
    if form.validate_on_submit():
        # Save product picture and create a new Product instance
        image_f = save_product_picture(form.image_f.data)
        new_product = Product(
            stripe_price=form.stripe_price.data,
            name=form.name.data,
            stock=form.stock.data,
            price=form.price.data,
            image_file=image_f,
        )
        db.session.add(new_product)
        db.session.commit()
        flash("Product has been added!", "success")
        return redirect(url_for("products.product"))
    return render_template("create_product.html", title="New Product", form=form)


@products.route("/product/<int:product_id>/update", methods=["GET", "POST"])
@login_required
@admin_only
def update_product(product_id):
    """Route for updating a product."""

    product = Product.query.get_or_404(product_id)
    # Fill form fields with product data
    form = UpdateProductForm(
        stripe_price=product.stripe_price,
        name=product.name,
        stock=product.stock,
        price=product.price,
        image_f=product.image_file,
    )
    if form.validate_on_submit():
        if form.name.data != product.name:
            # Check if product name is already taken
            if Product.query.filter_by(name=form.name.data).first():
                flash(
                    "That product name is taken. Please choose different one.", "danger"
                )
                return redirect(url_for("products.product"))
        if form.stripe_price.data != product.stripe_price:
            # Check if stripe price ID is already taken
            if Product.query.filter_by(stripe_price=form.stripe_price.data).first():
                flash("That Price ID is taken. Please choose different one.", "danger")
                return redirect(url_for("products.product"))
        if form.image_f.data != product.image_file:
            image_f = save_product_picture(form.image_f.data)
            product.image_file = image_f
        product.stripe_price = form.stripe_price.data
        product.name = form.name.data
        product.stock = form.stock.data
        product.price = form.price.data
        db.session.commit()
        flash("Product has been updated.", "success")
        return redirect(url_for("products.product"))
    image_file = url_for("static", filename="img/" + product.image_file)
    return render_template(
        "create_product.html",
        title="Update Product",
        product=product,
        form=form,
        image_file=image_file,
        product_id=product_id,
    )


@products.route("/product/<int:product_id>/delete")
@login_required
@admin_only
def delete_product(product_id):
    """Route for deleting a product"""

    product = Product.query.get_or_404(product_id)
    # Check if the product is in a customer's cart, wishlist or order
    cart = Cart.query.filter_by(product_id=product_id).first()
    wishlist = Wishlist.query.filter_by(product_id=product_id).first()
    order = Order.query.filter_by(product_id=product_id).first()
    if cart or wishlist or order:
        flash("You can't delete this product. Product is in customers bag.", "danger")
        return redirect(url_for("products.product"))
    db.session.delete(product)
    db.session.commit()
    flash(f"{product.name} has been deleted!", "success")
    return redirect(url_for("products.product"))
